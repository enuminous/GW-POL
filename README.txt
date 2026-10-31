EFMW-GW-POL-002 — extra gravitational-wave polarization check
Executed 2026-10-30 for Matthew Chenoweth Wright.

Open report.html for the self-contained report.

Scope: reproduction of public aggregate evidence, conditional scalar-curvature
mapping, and an idealized synthetic injection check. No new observed strain
analysis, no EFMW parameter fit, no detection, no empirical validation.

Reproduce:
  python -m pip install -r requirements.txt
  python run.py
  python build_report.py

The run regenerates results/results.json, aggregate.csv, the original numerical
LaTeX macros and paper-style plot, and an independently plotted results figure.
32 executable checks passed in this run. The tests are defined in protocol.json.
They establish numerical consistency, not discovery significance.

Original release: https://dcc.ligo.org/LIGO-P2600410-v1/public
Underlying manuscript: https://dcc.ligo.org/LIGO-P2500781-v17/public
The inspected manuscript is dated 21 July 2026; peer-review status was not
established by this run. Original POL.tar.gz and its eight extracted files are
included unchanged. The release contains three aggregate JSON files, no strain,
no per-event likelihoods and no scalar-amplitude posterior samples. The upstream
summary mentions event_diagnostics.py, which is not in this archive.

Evidence interpretation:
  - S means scalar-only; it is not the test for a scalar added to GR.
  - TS means tensor plus scalar. Its B_TS/T = 1.0185246 provides essentially
    no preference. No scalar amplitude bound follows from this number alone.
  - TV has a modest positive result, but its quoted interval accounts only for
    numerical evidence uncertainty; it is not a calibrated discovery significance.
  - Multiplying event evidences assumes independent event-specific integrations.
    This is not a likelihood for one common EFMW coupling across all events.

Simulation assumptions: three fixed randomly oriented ideal Michelsons, equal
sensitivities, known sky direction, one known real temporal template, independent
unit Gaussian detector noise, and no calibration or timing error. NOT HLV geometry
or a sensitivity forecast. Projected scalar SNR is a noise-normalized matched-filter
quantity, not a strain amplitude. Five arms reuse the same 100,000 noise draws.

EFMW mapping is restricted to C1's scalar-curvature sector on a constant scalar,
zero gauge-field background. The frozen C1 action is source-free. A specified
Jordan-frame matter action is an explicit extension needed to interpret a physical
detector or source. Masses, stability, source charges and waveform C_b(f) are still
required. No existing EFMW or Cosmology repository files were changed.

Pinned C1 commit: 83f9d2ec03e055c6cd09aa6359189161ad1571f6.
SHA-256 inputs and pinned URLs: sources.json, pinned-sources.json.
The downloaded source paper itself is not redistributed in this bundle.

Rights: LVK release is CC BY 4.0 unless otherwise specified; retain attribution.
Underlying EFMW sources remain attributed to Matthew Chenoweth Wright; this run
does not choose a new license for those files. See ATTRIBUTION.txt.
