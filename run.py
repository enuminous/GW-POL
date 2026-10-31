"""Reproduce aggregate POL results and run explicitly synthetic response checks."""
from pathlib import Path
import csv, hashlib, importlib.util, json, math, os, platform, sys
import numpy as np
import scipy
from scipy.stats import norm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'results'
OUT.mkdir(exist_ok=True)
P = json.loads((ROOT / 'protocol.json').read_text())
KEYS = P['hypotheses']
checks = []

def check(name, passed, detail):
    checks.append(dict(name=name, passed=bool(passed), detail=detail))

def aggregate():
    release = ROOT / 'release' / 'POL'
    ds = [json.loads((release / (s+'_pol_log_bayes_factor.json')).read_text())
          for s in ['pre_o4a', 'o4a', 'o4b']]
    rows = []
    expected = {
        'GWTC-4.0': ([-14.72,-5.33,-5.21,-.20,.10,-.31], [.59,.58,.58,.57,.57,.57]),
        'new': ([-4.78,-1.06,-.82,.21,.82,.66], [.44,.43,.43,.43,.43,.43]),
        'GWTC-5.0': ([-19.50,-6.39,-6.03,.01,.91,.35], [.73,.72,.72,.71,.71,.71])}
    for group, ix in [('GWTC-4.0',[0,1]), ('new',[2]), ('GWTC-5.0',[0,1,2])]:
        for j,k in enumerate(KEYS):
            logb = math.fsum(ds[i]['log_bayes_factor'][k] for i in ix)
            err = math.sqrt(math.fsum(ds[i]['log_bayes_factor_err'][k]**2 for i in ix))
            rows.append(dict(group=group,hypothesis=k,log10_B_X_over_T=logb,
                             half_width_90=err,B_X_over_T=10**logb,
                             B_lower_90=10**(logb-err),B_upper_90=10**(logb+err)))
            check('Table6 '+group+' '+k, f'{logb:.2f}'==f'{expected[group][0][j]:.2f}' and
                  f'{err:.2f}'==f'{expected[group][1][j]:.2f}', 'central value and 90% numerical-evidence half width')
    # Execute upstream combining and macro routines, keeping supplied files unchanged.
    old = Path.cwd()
    os.chdir(release)
    spec=importlib.util.spec_from_file_location('upstream_summary',release/'summary.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    upstream=module.load_log_bayes_factors()
    os.chdir(OUT)
    module.generate_latex_macros(upstream)
    check('upstream macro byte equality',(OUT/'pol_macro.tex').read_bytes()==(release/'pol_macro.tex').read_bytes(), 'all original macro groups')
    module.generate_paper_figure(upstream)
    os.chdir(old)
    check('independent aggregate vs upstream',max(abs(r['log10_B_X_over_T']-upstream['all'][r['hypothesis']]) for r in rows if r['group']=='GWTC-5.0')<1e-12,'independent math.fsum implementation')
    return rows

def detector_response(rng):
    """Three ideal equal-noise Michelsons; random fixed rotations, NOT HLV geometry."""
    tensors=[]; arms=[]
    for _ in range(3):
        Q,R=np.linalg.qr(rng.normal(size=(3,3)))
        Q=Q@np.diag(np.sign(np.diag(R)))
        if np.linalg.det(Q)<0:Q[:,2]*=-1
        u,v=Q[:,0],Q[:,1]
        tensors.append(.5*(np.outer(u,u)-np.outer(v,v)))
        arms.append(dict(u=u.tolist(),v=v.tolist()))
    theta,phi=1.1,.7
    n=np.array([np.sin(theta)*np.cos(phi),np.sin(theta)*np.sin(phi),np.cos(theta)])
    m=np.array([np.cos(theta)*np.cos(phi),np.cos(theta)*np.sin(phi),-np.sin(theta)])
    l=np.array([-np.sin(phi),np.cos(phi),0.])
    pols=[np.outer(m,m)-np.outer(l,l),np.outer(m,l)+np.outer(l,m),
          np.outer(m,m)+np.outer(l,l),np.sqrt(2)*np.outer(n,n)]
    F=np.array([[np.sum(d*e) for e in pols] for d in tensors])
    return F,arms

def injection_test():
    rng=np.random.default_rng(P['seed'])
    F,arms=detector_response(rng)
    FT,b=F[:,:2],F[:,2]
    projector=np.eye(3)-FT@np.linalg.pinv(FT)
    leakage=np.linalg.norm(projector@FT)
    check('projector algebra',max(np.linalg.norm(projector-projector.T),np.linalg.norm(projector@projector-projector),leakage)<1e-12,'tensor response removal')
    check('scalar longitudinal degeneracy',np.linalg.norm(F[:,3]+np.sqrt(2)*b)<1e-12,'e_longitudinal=sqrt(2) nn and trace-free Michelson response')
    projected_b=projector@b; norm_b=np.linalg.norm(projected_b)
    check('synthetic scalar identifiable',norm_b>1e-4,'nonzero scalar projection for this fixed synthetic geometry')
    q=projected_b/norm_b
    ntrial=P['synthetic_trials_per_arm'];threshold=norm.isf(P['two_sided_per_template_false_alarm_probability']/2)
    noise=rng.normal(size=(ntrial,3))
    tensor=FT@np.array([8.,5.])
    noise_stat=(noise+tensor)@q
    arms_results=[]
    for rho in P['null_projected_snr']:
        # Full detector signal b * rho / |P b|, projected onto the unit null vector.
        z=noise_stat+(b*(rho/norm_b))@q
        count=int(np.count_nonzero(np.abs(z)>threshold)); rate=count/ntrial
        theory=float(norm.sf(threshold-rho)+norm.cdf(-threshold-rho))
        se=math.sqrt(theory*(1-theory)/ntrial)
        check('injection rho='+str(rho),abs(rate-theory)<5*se,dict(empirical=rate,analytic=theory,binomial_se=se))
        arms_results.append(dict(null_snr=rho,n=ntrial,detections=count,detected_fraction=rate,analytic_fraction=theory,binomial_se=se))
    P2=np.eye(2)-FT[:2]@np.linalg.pinv(FT[:2])
    check('two detector tensor saturation',np.linalg.norm(P2)<1e-12,'two independent tensor amplitudes exhaust two detector channels')
    return dict(label='SYNTHETIC / NOT OBSERVED STRAIN / NOT AN HLV FORECAST',
                arms=arms,sky_theta=1.1,sky_phi=.7,response=F.tolist(),
                tensor_rank=int(np.linalg.matrix_rank(FT)),tensor_condition=float(np.linalg.cond(FT)),
                scalar_null_response=float(norm_b),tensor_leakage=float(leakage),
                threshold=float(threshold),results=arms_results,
                note='Known sky and shared real temporal template, independent unit Gaussian detector noise, equal sensitivities. Same noise across arms. No sky/time/template trials, glitches, calibration or waveform uncertainties.')

def coupling_check():
    # C1 restricted to scalar-curvature sector, in reduced Planck units.
    # F=Mpl^2-2 U_R, q=gradient F. K=I/F+3 qq^T/(2F^2).
    rng=np.random.default_rng(P['seed']+1);errors=[];mineig=1e100;graderrors=[]
    for _ in range(1000):
        f=float(rng.uniform(.5,2));q=rng.normal(0,.4,8)
        K=np.eye(8)/f+1.5*np.outer(q,q)/f**2
        a2=float(q@np.linalg.solve(K,q)/(4*f**2))
        closed=float((q@q)/(4*f+6*(q@q)))
        errors.append(abs(a2-closed));mineig=min(mineig,float(np.linalg.eigvalsh(K).min()))
        # Independent finite-difference check of q from curvature coefficient.
        x=rng.normal(0,.1,8);xi=rng.normal(0,.1,8);g=rng.normal(0,.1,8)
        h=np.triu(rng.normal(0,.1,(8,8)),1);h=h+h.T
        def coeff(y):return 1-np.dot(xi,y*y)-2*np.dot(g,y)-y@h@y
        analytic=-2*xi*x-2*g-2*h@x
        eps=1e-5
        numeric=np.array([(coeff(x+eps*e)-coeff(x-eps*e))/(2*eps) for e in np.eye(8)])
        graderrors.append(float(np.max(np.abs(analytic-numeric))))
    check('Einstein frame coupling identity',max(errors)<1e-12,dict(samples=1000,max_abs_error=max(errors)))
    check('curvature gradient',max(graderrors)<1e-8,dict(samples=1000,max_abs_error=max(graderrors)))
    check('positive kinetic matrix sampled',mineig>0,dict(min_eigenvalue=mineig,domain='F in [0.5,2], canonical scalar kinetic matrix'))
    return dict(samples=1000,max_identity_error=max(errors),max_gradient_error=max(graderrors),min_kinetic_eigenvalue=mineig,
                formulas={'F':'1 - sum(xi_a*x_a^2) - 2 sum(g_Ea*x_a) - 2 sum(a<b,h_Eab*x_a*x_b)',
                          'q':'gradient(F)', 'K':'I/F + 3 q q^T/(2 F^2)',
                          'alpha_squared':'q^T inverse(K) q/(4 F^2) = |q|^2/(4 F+6 |q|^2)',
                          'linear_breathing_strain':'h_b = -q dot delta_x/F (massless/local flat background limit)'},
                caveat='Classical conditional scalar-tensor map; ordinary Jordan-frame matter added explicitly, absent from source-free C1. Does not determine compact-object scalar charges or C_b(f), and is not a measured bound. Assumes F>0, zero gauge backgrounds, constant scalar background, stable potential Hessian and valid EFT.')

def make_figure(rows, inj):
    plt.rcdefaults()
    fig,axs=plt.subplots(1,2,figsize=(12,4.8),layout='constrained')
    r=[x for x in rows if x['group']=='GWTC-5.0']
    axs[0].errorbar(np.arange(6),[x['log10_B_X_over_T'] for x in r],yerr=[x['half_width_90'] for x in r],fmt='o',color='#176b87',capsize=5)
    axs[0].axhline(0,color='gray',ls='--');axs[0].set_xticks(range(6),KEYS)
    axs[0].set_ylabel('log10 evidence ratio: alternative / tensor')
    axs[0].set_title('Observed-data products: aggregate reproduction')
    axs[0].text(.03,.1,'Error bars: 90% numerical evidence uncertainty\nNo strain reanalysis; no EFMW amplitude limit',transform=axs[0].transAxes,fontsize=9)
    x=np.linspace(0,5,200);t=inj['threshold']
    axs[1].plot(x,norm.sf(t-x)+norm.cdf(-t-x),label='Analytic Gaussian prediction',color='#176b87')
    a=inj['results'];axs[1].errorbar([z['null_snr'] for z in a],[z['detected_fraction'] for z in a],yerr=[1.96*z['binomial_se'] for z in a],fmt='o',color='#bb572d',label='100,000 synthetic trials per arm')
    axs[1].set(xlabel='Scalar SNR projected into tensor null stream',ylabel='Fraction above threshold',ylim=(-.03,1.04),title='Synthetic response test: idealized network')
    axs[1].legend(fontsize=8,loc='lower right')
    fig.suptitle('EFMW-GW-POL-002 | Published evidence and simulation kept separate',fontsize=13)
    fig.savefig(OUT/'results.png',dpi=170);fig.savefig(OUT/'results.svg');plt.close(fig)

def main():
    rows=aggregate();inj=injection_test();coupling=coupling_check();make_figure(rows,inj)
    result=dict(study=P['study'],aggregate=rows,synthetic=inj,conditional_coupling=coupling,checks=checks,
                all_checks_pass=all(c['passed'] for c in checks),
                environment=dict(python=sys.version,numpy=np.__version__,scipy=scipy.__version__,matplotlib=matplotlib.__version__,platform=platform.platform()),
                protocol_sha256=hashlib.sha256((ROOT/'protocol.json').read_bytes()).hexdigest())
    (OUT/'results.json').write_text(json.dumps(result,indent=2))
    with (OUT/'aggregate.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
    print(json.dumps(dict(checks_passed=sum(c['passed'] for c in checks),checks_total=len(checks),
                         all_checks_pass=result['all_checks_pass'],aggregate=[r for r in rows if r['group']=='GWTC-5.0'],
                         synthetic=inj['results'],coupling=coupling),indent=2))
    if not result['all_checks_pass']:raise SystemExit(1)

if __name__=='__main__':main()
