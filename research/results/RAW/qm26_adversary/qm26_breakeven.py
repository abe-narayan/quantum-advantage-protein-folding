import numpy as np
# measured (single core, contended box): c_node = 0.47e-6 s per node-step (Verlet, 2 sparse matvecs)
c_node=0.55e-6; rho=29944/(198.3*254.1*272.5); wmax=4.27; dt=0.2/wmax
# light-cone radius for 1e-6 accuracy: R(t)=R0+v t ; from lightcone test R=100 A at t=18.7 -> use v=4.5 A/unit, R0=15 A
def C(t,v=2.5,R0=40.0,S=1):
    n=rho*4/3*np.pi*(R0+v*t)**3
    return n*(t/dt)*c_node/S, n
# quantum: procedural oracle q Toffolis/query, kappa queries per unit (wmax t), AE reps pi/(2 eps)
def Q(t,q=1e4,kappa=10,eps=1e-2,tT=1e-6):
    return (np.pi/(2*eps))*kappa*wmax*t*q*tT
print('rho nodes/A^3',rho)
for S in (1,8,1000):
  for tT in (1e-6,170e-6):
    ts=np.logspace(0,6,6000)
    c=np.array([C(t,S=S)[0] for t in ts]); qq=Q(ts,tT=tT)
    i=np.argmax(c>qq)
    t=ts[i]; cc,n=C(t,S=S)
    print(f'S={S:5d} tToff={tT:.0e}: break-even t*={t:.3g} units, R={40+2.5*t:.3g} A, lightcone nodes={n:.2e}, cost each side={cc:.3g} s ({cc/3600:.3g} h)')
# explicit-data regime (no procedural oracle): QROAM Toffolis/query ~ 2*sqrt(P*b), P=8N springs, b=80 bits
for N in (1e6,1e8):
    P=8*N; qro=2*np.sqrt(P*80); L=(N/rho)**(1/3); t=L/2.0; steps=t/dt
    Qtot=(np.pi/(2*1e-2))*10*wmax*t*qro
    print(f'N={N:.0e}: extent {L:.0f} A, crossing t={t:.0f}, Verlet steps={steps:.0f}, classical 1 core={N*steps*c_node/3600:.3g} h; quantum Toffolis={Qtot:.2e} -> {Qtot*1e-6/86400:.3g} d @1us, {Qtot*170e-6/3.15e7:.3g} yr @170us; QROAM ancillas~{np.sqrt(P*80):.2e}')
