from pathlib import Path
import base64,html,json
p=Path(__file__).resolve().parent
r=json.loads((p/'results/results.json').read_text())
names={'S':'Scalar only','V':'Vector only','VS':'Vector + scalar','TS':'Tensor + scalar','TV':'Tensor + vector','TVS':'Tensor + vector + scalar'}
rows=''.join(f'<tr><td>{names[z["hypothesis"]]}</td><td>{z["log10_B_X_over_T"]:.5f} ± {z["half_width_90"]:.5f}</td><td>{z["B_X_over_T"]:.6g}</td></tr>' for z in r['aggregate'] if z['group']=='GWTC-5.0')
sim=''.join(f'<tr><td>{z["null_snr"]}</td><td>{z["detected_fraction"]:.3%}</td><td>{z["analytic_fraction"]:.3%}</td></tr>' for z in r['synthetic']['results'])
checks=''.join(f'<li><b>{"PASS" if z["passed"] else "FAIL"}</b> {html.escape(z["name"])}</li>' for z in r['checks'])
img=base64.b64encode((p/'results/results.png').read_bytes()).decode()
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>EFMW-GW-POL-002 — Results</title>
<style>body{margin:0;background:#edf1f4;color:#152737;font:17px/1.6 system-ui,sans-serif}main{max-width:1040px;margin:35px auto;padding:36px;background:white;border-top:7px solid #176b87}h1{font-size:34px;line-height:1.2}h2{margin-top:38px;font-size:24px}table{border-collapse:collapse;width:100%;font-variant-numeric:tabular-nums}th,td{text-align:left;border-bottom:1px solid #d8e2e8;padding:10px}th{background:#edf4f7}.status{padding:20px;background:#e9f5f3;border-left:5px solid #17775d}small{color:#556}img{width:100%;height:auto}pre{white-space:pre-wrap;background:#f3f6f8;padding:18px;font:14px/1.6 monospace}a{color:#116783}@media(max-width:650px){main{padding:18px;margin:0}body{font-size:15px}th,td{padding:6px;font-size:13px}}</style><main>
<small>MATTHEW CHENOWETH WRIGHT · 30 OCTOBER 2026 · REPRODUCIBLE RESEARCH CHECK</small>
<h1>Extra gravitational-wave polarizations</h1>
<p class="status"><b>Public-results reproduction complete: 32/32 checks passed.</b><br>Tensor-plus-scalar evidence is essentially tied with tensor alone. This run does not establish an extra polarization or constrain an EFMW parameter.</p>
<p>Three distinct tasks were executed: independent recombination of released evidence totals, a conditional scalar-curvature coupling calculation, and synthetic injection tests. The bundle contains code, original public results, pinned EFMW sources, numerical outputs and assumptions.</p>
<h2>1. Published evidence reproduced</h2>
<p>Inputs: <a href="https://dcc.ligo.org/LIGO-P2600410-v1/public">LVK POL release P2600410-v1</a>. Manuscript: <a href="https://dcc.ligo.org/LIGO-P2500781-v17/public">P2500781-v17, 21 July 2026</a>; peer-review status not verified here. The archive contains three aggregate JSON files, plotting code and outputs. It does not contain per-event likelihoods, amplitude samples or strain.</p>
<table><tr><th>Hypothesis versus tensor</th><th>log₁₀ Bayes factor ± 90% half-width</th><th>Bayes factor</th></tr>ROWS</table>
<p>All 36 rounded central values and uncertainty entries across the three Table 6 rows match. Executing the upstream aggregation and macro routines reproduces the original macro file byte-for-byte. Combining totals reproduces an existing result; it is not independent inference from detector strain.</p>
<p>Scalar-only and tensor-plus-scalar are different hypotheses. The TS ratio of 1.0185 does not favor an added scalar appreciably. TV has a modest positive ratio, but the manuscript calls the result inconclusive: the error bars cover numerical evidence estimation, not noise/model systematics. Its method assumes constant complex polarization ratios and GR-selected time–frequency regions; mismatched scalar waveforms can be missed. These are model evidences, not scalar-amplitude upper limits.</p>
<img src="data:image/png;base64,IMAGE" alt="Published aggregate evidence ratios, alongside explicitly synthetic detection efficiencies">
<h2>2. Synthetic injection check</h2>
<p>Three fixed ideal Michelsons, equal sensitivity, known sky and shared temporal template; 100,000 Gaussian noise realizations reused at each of five injected scalar strengths. These are dimensionless projected SNR values, not observed strains or an HLV sensitivity forecast.</p>
<table><tr><th>Scalar SNR in tensor null stream</th><th>Simulated above-threshold fraction</th><th>Analytic fraction</th></tr>SIM</table>
<p>The two-sided threshold has nominal 1% per-template false-alarm probability. All five rates agree with their analytic probabilities within the frozen five-standard-error tolerance. Tensor cancellation error is below 5×10⁻¹⁶. The check also verifies scalar longitudinal/breathing response degeneracy and the loss of an unrestricted tensor null channel with only two independent detectors. It does not model glitches, calibration, unknown sky, template trials or the LVK sampler.</p>
<h2>3. What this establishes for EFMW</h2>
<p>Source: <a href="https://github.com/enuminous/EFMW-Lagrangian/blob/83f9d2ec03e055c6cd09aa6359189161ad1571f6/candidate/CANDIDATE.md">frozen C1 action at commit 83f9d2e</a>. Its scalar-curvature terms can be written F(φ)R/2. In reduced Planck units, on a constant scalar and zero gauge-field background:</p>
<pre>q = ∇F
K = I/F + 3 q qᵀ/(2F²)
α² = qᵀ K⁻¹ q/(4F²) = |q|²/(4F + 6|q|²)
h_b = −δF/F  (linear, massless local limit)</pre>
<p>This is a conditional application of established scalar-tensor mathematics, not a new verified law. The matrix identity passes 1,000 numerical checks (maximum error 5.6×10⁻¹⁷). A finite-difference check independently verifies the curvature gradient. In this limit, q=0 gives no linear conformal breathing strain even if scalar fields propagate.</p>
<p>C1 is source-free. Coupling an actual detector or binary requires an explicit matter extension. To predict a measurable scalar signal, specify the background, coefficients, stable masses, compact-object scalar charges, emitted waveform and propagation. No C_b(f)=h_b(f)/h₊(f) prediction or EFMW likelihood is supplied by the aggregate release. Its event-wise products also cannot replace inference for a common EFMW coupling. Existing cosmology definitions were not changed.</p>
<h2>Evidence audit and next test</h2>
<table><tr><th>Claim</th><th>Status</th></tr><tr><td>Aggregate reproduction and numerical response checks</td><td>Demonstrated computationally</td></tr><tr><td>Conditional C1 scalar-curvature map</td><td>Analytic reasoning with numerical checks; assumptions explicit</td></tr><tr><td>Observed extra mode or physical EFMW validation</td><td>Not established</td></tr><tr><td>EFMW coupling bound from these totals</td><td>Unresolved; missing waveform and likelihood mapping</td></tr></table>
<p>The protocol was written after inspecting the published data and before executing the simulation. It is a reproducibility protocol, not a preregistered discovery test. No Zoo animal operations or Lean verification were claimed.</p>
<ol><li>Freeze a stable C1 submodel, matter coupling and background; derive h_b(f), including compact-object charges. A decoupled q=0 branch predicts no linear breathing signal in the stated limit.</li><li>Test that waveform against independent GR-plus-noise injections, calibration shifts and glitches, with sky/time/template search trials included. Freeze a global false-alarm threshold before unblinding strain.</li><li>Use verified event-level strain, PSDs and data-quality segments for a fresh common-coupling likelihood. Compare to GR and conventional scalar-tensor alternatives with matched priors.</li></ol>
<details><summary>32 executable checks</summary><ul>CHECKS</ul></details>
<details><summary>Full conditional derivation and limitations</summary><pre>DERIVATION</pre></details>
<p><small>LVK data: CC BY 4.0 unless otherwise stated. This analysis is not an LVK result or endorsement. Standard conformal mapping: <a href="https://arxiv.org/abs/1003.1159">D. I. Kaiser (2010)</a>, DOI 10.1103/PhysRevD.81.084044. See ATTRIBUTION.txt and source hashes in the bundle.</small></p></main></html>'''
for key,value in [('ROWS',rows),('SIM',sim),('IMAGE',img),('CHECKS',checks),('DERIVATION',html.escape((p/'DERIVATION.txt').read_text()))]:page=page.replace(key,value)
(p/'report.html').write_text(page)
print(p/'report.html')
