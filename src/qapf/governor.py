"""Resource governor: run a queue of independent jobs under a hard CPU/RAM ceiling.

Policy (CLAUDE.md compute policy): target ~94-95% machine CPU and RAM, NEVER intentionally exceed 95%.

Mechanics
---------
* Jobs are shell commands (one per line in a JSONL queue: {"name": ..., "cmd": ..., "ram_gb": est, "threads": n}).
* A job is launched only if (projected RAM after launch) <= RAM_LAUNCH_CAP and the recent CPU mean leaves room.
* Every SAMPLE_S seconds:
    - RAM > RAM_SUSPEND  -> suspend the youngest running job (psutil suspend) and stop launching;
    - RAM > RAM_KILL     -> terminate the youngest running job and requeue it (at most MAX_REQUEUE times);
    - CPU (10 s mean) > CPU_SUSPEND -> suspend the youngest job; resumes when CPU < CPU_RESUME and RAM < RAM_RESUME.
* Each job gets OMP/MKL/OPENBLAS/NUMEXPR threads = its "threads" field (default 1) so the total thread count is known.
* Everything is logged to a JSONL log (one sample per line) so utilisation can be reported afterwards.

This module has no project-specific logic; experiment scripts must write their own incremental results.
"""
from __future__ import annotations

import json
import os
import shlex
import subprocess
import sys
import time
from collections import deque
from dataclasses import dataclass, field

import psutil

RAM_LAUNCH_CAP = 0.90     # projected fraction after launching a new job
RAM_SUSPEND = 0.935
RAM_RESUME = 0.90
RAM_KILL = 0.95
CPU_LAUNCH_MAX = 0.88     # launch only if 10 s CPU mean below this
CPU_SUSPEND = 0.97
CPU_RESUME = 0.90
SAMPLE_S = 2.0
MAX_REQUEUE = 3


def machine_state():
    vm = psutil.virtual_memory()
    return dict(ram_frac=vm.percent / 100.0, ram_used_gb=(vm.total - vm.available) / 2**30,
                ram_total_gb=vm.total / 2**30, cpu_frac=psutil.cpu_percent(interval=None) / 100.0)


@dataclass
class Job:
    name: str
    cmd: str
    ram_gb: float = 0.5
    threads: int = 1
    cwd: str | None = None
    requeues: int = 0
    proc: subprocess.Popen | None = None
    started: float = 0.0
    suspended: bool = False
    log_path: str | None = None


@dataclass
class Governor:
    log_file: str
    max_workers: int = max(1, (os.cpu_count() or 2) - 1)
    queue: deque = field(default_factory=deque)
    running: list = field(default_factory=list)
    done: list = field(default_factory=list)
    failed: list = field(default_factory=list)
    cpu_hist: deque = field(default_factory=lambda: deque(maxlen=5))

    def add(self, job: Job):
        self.queue.append(job)

    def _log(self, **kw):
        kw["t"] = time.time()
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(kw) + "\n")

    def _launch(self, job: Job):
        env = dict(os.environ)
        for v in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
            env[v] = str(job.threads)
        env["PYTHONUNBUFFERED"] = "1"
        logdir = os.path.join(os.path.dirname(self.log_file), "joblogs")
        os.makedirs(logdir, exist_ok=True)
        job.log_path = os.path.join(logdir, f"{job.name}.log")
        fh = open(job.log_path, "a", encoding="utf-8")
        job.proc = subprocess.Popen(job.cmd, shell=True, cwd=job.cwd, env=env, stdout=fh, stderr=subprocess.STDOUT)
        job.started = time.time()
        job.suspended = False
        self.running.append(job)
        self._log(ev="launch", job=job.name, pid=job.proc.pid, cmd=job.cmd)

    def _ps(self, job):
        try:
            return psutil.Process(job.proc.pid)
        except Exception:
            return None

    def _tree(self, job):
        p = self._ps(job)
        if p is None:
            return []
        try:
            return [p] + p.children(recursive=True)
        except Exception:
            return [p]

    def _suspend(self, job):
        for p in self._tree(job):
            try:
                p.suspend()
            except Exception:
                pass
        job.suspended = True
        self._log(ev="suspend", job=job.name)

    def _resume(self, job):
        for p in self._tree(job):
            try:
                p.resume()
            except Exception:
                pass
        job.suspended = False
        self._log(ev="resume", job=job.name)

    def _kill(self, job):
        for p in reversed(self._tree(job)):
            try:
                p.kill()
            except Exception:
                pass
        self._log(ev="kill", job=job.name)

    def step(self):
        st = machine_state()
        self.cpu_hist.append(st["cpu_frac"])
        cpu_mean = sum(self.cpu_hist) / len(self.cpu_hist)
        # reap
        for job in list(self.running):
            rc = job.proc.poll()
            if rc is not None:
                self.running.remove(job)
                (self.done if rc == 0 else self.failed).append(job)
                self._log(ev="exit", job=job.name, rc=rc, secs=round(time.time() - job.started, 1))
        active = [j for j in self.running if not j.suspended]
        suspended = [j for j in self.running if j.suspended]
        # RAM emergencies
        if st["ram_frac"] > RAM_KILL and self.running:
            victim = max(self.running, key=lambda j: j.started)
            self._kill(victim)
            self.running.remove(victim)
            if victim.requeues < MAX_REQUEUE:
                victim.requeues += 1
                victim.proc = None
                self.queue.appendleft(victim)
            else:
                self.failed.append(victim)
        elif (st["ram_frac"] > RAM_SUSPEND or cpu_mean > CPU_SUSPEND) and len(active) > 1:
            self._suspend(max(active, key=lambda j: j.started))
        elif suspended and st["ram_frac"] < RAM_RESUME and cpu_mean < CPU_RESUME:
            self._resume(min(suspended, key=lambda j: j.started))
        elif (self.queue and not suspended and len(self.running) < self.max_workers
              and cpu_mean < CPU_LAUNCH_MAX):
            job = self.queue[0]
            proj = (st["ram_used_gb"] + job.ram_gb) / st["ram_total_gb"]
            if proj <= RAM_LAUNCH_CAP:
                self.queue.popleft()
                self._launch(job)
        self._log(ev="sample", ram=round(st["ram_frac"], 4), cpu=round(st["cpu_frac"], 4),
                  cpu_mean=round(cpu_mean, 4), running=len(self.running),
                  suspended=len(suspended), queued=len(self.queue))

    def run(self):
        psutil.cpu_percent(interval=None)
        while self.queue or self.running:
            self.step()
            time.sleep(SAMPLE_S)
        self._log(ev="finished", done=[j.name for j in self.done], failed=[j.name for j in self.failed])
        return self.done, self.failed


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(description="Run a JSONL job queue under the 95% CPU/RAM ceiling.")
    ap.add_argument("queue", help="JSONL file: one {name, cmd, ram_gb?, threads?, cwd?} per line")
    ap.add_argument("--log", required=True)
    ap.add_argument("--max-workers", type=int, default=max(1, (os.cpu_count() or 2) - 1))
    a = ap.parse_args(argv)
    g = Governor(log_file=a.log, max_workers=a.max_workers)
    with open(a.queue, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                d = json.loads(line)
                g.add(Job(**{k: d[k] for k in d if k in ("name", "cmd", "ram_gb", "threads", "cwd")}))
    done, failed = g.run()
    print(json.dumps(dict(done=[j.name for j in done], failed=[j.name for j in failed])))
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
