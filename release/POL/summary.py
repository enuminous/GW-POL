"""Null stream log Bayes factor analysis: paper figure and LaTeX macros.

This script regenerates the paper figure (pol_logB.pdf) and the LaTeX macros
(pol_macro.tex) from the committed log Bayes factor JSON files. It only depends
on files tracked in git (pre_o4a/o4a/o4b_pol_log_bayes_factor.json and
paper.style), so it can be run anywhere without the large per-event PE result
dataset. The heavy processing that produces o4b_pol_log_bayes_factor.json (and
the per-event / skymap products) lives in event_diagnostics.py.
"""

import json

from matplotlib import style
import matplotlib.pyplot as plt
import numpy as np

style.use("paper.style")

_ORDERED_KEYS = ['S', 'V', 'VS', 'TS', 'TV', 'TVS']


def load_log_bayes_factors():
    """Load and combine the log10 Bayes factors from the committed JSON files.

    pre-O4a + O4a give the GWTC-4.0 totals; adding O4b gives GWTC-5.0.
    """
    with open('pre_o4a_pol_log_bayes_factor.json', 'r') as f:
        pre_o4a_dict = json.load(f)
    with open('o4a_pol_log_bayes_factor.json', 'r') as f:
        o4a_dict = json.load(f)
    with open('o4b_pol_log_bayes_factor.json', 'r') as f:
        o4b_dict = json.load(f)

    log_bayes_factor_pre_o4a = pre_o4a_dict['log_bayes_factor']
    log_bayes_factor_error_pre_o4a = pre_o4a_dict['log_bayes_factor_err']

    log_bayes_factor_o4a = o4a_dict['log_bayes_factor']
    log_bayes_factor_error_o4a = o4a_dict['log_bayes_factor_err']

    log_bayes_factor_o4b = o4b_dict['log_bayes_factor']
    log_bayes_factor_error_o4b = o4b_dict['log_bayes_factor_err']

    log_bayes_factor_gwtc4 = {}
    log_bayes_factor_error_gwtc4 = {}
    for key in log_bayes_factor_o4a:
        log_bayes_factor_gwtc4[key] = log_bayes_factor_pre_o4a[key] + log_bayes_factor_o4a[key]
        log_bayes_factor_error_gwtc4[key] = np.sqrt(log_bayes_factor_error_pre_o4a[key]**2 + log_bayes_factor_error_o4a[key]**2)

    log_bayes_factor_all = {key: log_bayes_factor_gwtc4[key] + log_bayes_factor_o4b[key] for key in log_bayes_factor_gwtc4.keys()}
    log_bayes_factor_error_all = {key: np.sqrt(log_bayes_factor_error_gwtc4[key]**2 + log_bayes_factor_error_o4b[key]**2) for key in log_bayes_factor_gwtc4.keys()}

    return {
        'gwtc4': log_bayes_factor_gwtc4,
        'gwtc4_err': log_bayes_factor_error_gwtc4,
        'o4b': log_bayes_factor_o4b,
        'o4b_err': log_bayes_factor_error_o4b,
        'all': log_bayes_factor_all,
        'all_err': log_bayes_factor_error_all,
    }


def generate_paper_figure(bf):
    """Generate the GWTC-4.0 vs GWTC-5.0 bar chart (pol_logB.pdf)."""
    log_bayes_factor_gwtc4 = bf['gwtc4']
    log_bayes_factor_error_gwtc4 = bf['gwtc4_err']
    log_bayes_factor_all = bf['all']
    log_bayes_factor_error_all = bf['all_err']

    x = np.arange(len(_ORDERED_KEYS))
    width = 0.35

    fig, ax = plt.subplots()
    ax.bar(x - width/2, [log_bayes_factor_gwtc4[k] for k in _ORDERED_KEYS], width, yerr=[log_bayes_factor_error_gwtc4[k] for k in _ORDERED_KEYS], label='GWTC-4.0')
    ax.bar(x + width/2, [log_bayes_factor_all[k] for k in _ORDERED_KEYS], width, yerr=[log_bayes_factor_error_all[k] for k in _ORDERED_KEYS], label='GWTC-5.0')

    ax.set_ylabel(r'$\log_{10}\mathcal{B}^{X}_{\mathrm{T}}$')
    ax.set_xticks(x)
    ax.set_xticklabels(_ORDERED_KEYS)
    ax.legend()

    plt.savefig('pol_logB.pdf', bbox_inches='tight')
    plt.close()


def generate_latex_macros(bf):
    """Generate the LaTeX macros with the numerical results (pol_macro.tex)."""
    log_bayes_factor_gwtc4 = bf['gwtc4']
    log_bayes_factor_error_gwtc4 = bf['gwtc4_err']
    log_bayes_factor_o4b = bf['o4b']
    log_bayes_factor_error_o4b = bf['o4b_err']
    log_bayes_factor_all = bf['all']
    log_bayes_factor_error_all = bf['all_err']

    _gwtc4_fmt     = {key: f"{log_bayes_factor_gwtc4[key]:.2f}" for key in _ORDERED_KEYS}
    _gwtc4_err_fmt = {key: f"{log_bayes_factor_error_gwtc4[key]:.2f}" for key in _ORDERED_KEYS}
    _o4b_fmt       = {key: f"{log_bayes_factor_o4b[key]:.2f}" for key in _ORDERED_KEYS}
    _o4b_err_fmt   = {key: f"{log_bayes_factor_error_o4b[key]:.2f}" for key in _ORDERED_KEYS}

    _imp_vals      = {key: log_bayes_factor_gwtc4[key] - log_bayes_factor_all[key] for key in _ORDERED_KEYS}
    _argmin_imp    = int(np.argmin([_imp_vals[k] for k in _ORDERED_KEYS]))
    _argmax_imp    = int(np.argmax([_imp_vals[k] for k in _ORDERED_KEYS]))

    _imp_fmt      = {key: f"{v:.2f}" for key, v in _imp_vals.items()}
    _imp_err_fmt  = {key: f"{log_bayes_factor_error_o4b[key]:.2f}" for key in _ORDERED_KEYS}
    _bf_fmt       = {key: f"{log_bayes_factor_all[key]:.2f}" for key in _ORDERED_KEYS}
    _bf_err_fmt   = {key: f"{log_bayes_factor_error_all[key]:.2f}" for key in _ORDERED_KEYS}

    _bf_min    = f"{min(log_bayes_factor_all.values()):.2f}"
    _bf_max    = f"{max(log_bayes_factor_all.values()):.2f}"
    _bf_minerr = f"{log_bayes_factor_error_all[_ORDERED_KEYS[int(np.argmin([log_bayes_factor_all[k] for k in _ORDERED_KEYS]))]]:.2f}"
    _bf_maxerr = f"{log_bayes_factor_error_all[_ORDERED_KEYS[int(np.argmax([log_bayes_factor_all[k] for k in _ORDERED_KEYS]))]]:.2f}"
    _imp_min    = f"{min(_imp_vals.values()):.2f}"
    _imp_max    = f"{max(_imp_vals.values()):.2f}"
    _imp_minerr = f"{log_bayes_factor_error_o4b[_ORDERED_KEYS[_argmin_imp]]:.2f}"
    _imp_maxerr = f"{log_bayes_factor_error_o4b[_ORDERED_KEYS[_argmax_imp]]:.2f}"

    pol_macro_string = rf"""\DeclareRobustCommand{{\TGRPOLlogBGWTCFour}}[1]{{\IfEqCase{{#1}}{{
{{S}}{{\unreviewed{{{_gwtc4_fmt["S"]}}}}}
{{Serr}}{{\unreviewed{{{_gwtc4_err_fmt["S"]}}}}}
{{V}}{{\unreviewed{{{_gwtc4_fmt["V"]}}}}}
{{Verr}}{{\unreviewed{{{_gwtc4_err_fmt["V"]}}}}}
{{VS}}{{\unreviewed{{{_gwtc4_fmt["VS"]}}}}}
{{VSerr}}{{\unreviewed{{{_gwtc4_err_fmt["VS"]}}}}}
{{TS}}{{\unreviewed{{{_gwtc4_fmt["TS"]}}}}}
{{TSerr}}{{\unreviewed{{{_gwtc4_err_fmt["TS"]}}}}}
{{TV}}{{\unreviewed{{{_gwtc4_fmt["TV"]}}}}}
{{TVerr}}{{\unreviewed{{{_gwtc4_err_fmt["TV"]}}}}}
{{TVS}}{{\unreviewed{{{_gwtc4_fmt["TVS"]}}}}}
{{TVSerr}}{{\unreviewed{{{_gwtc4_err_fmt["TVS"]}}}}}
}}}}

\DeclareRobustCommand{{\TGRPOLlogBOFourB}}[1]{{\IfEqCase{{#1}}{{
{{S}}{{\unreviewed{{{_o4b_fmt["S"]}}}}}
{{Serr}}{{\unreviewed{{{_o4b_err_fmt["S"]}}}}}
{{V}}{{\unreviewed{{{_o4b_fmt["V"]}}}}}
{{Verr}}{{\unreviewed{{{_o4b_err_fmt["V"]}}}}}
{{VS}}{{\unreviewed{{{_o4b_fmt["VS"]}}}}}
{{VSerr}}{{\unreviewed{{{_o4b_err_fmt["VS"]}}}}}
{{TS}}{{\unreviewed{{{_o4b_fmt["TS"]}}}}}
{{TSerr}}{{\unreviewed{{{_o4b_err_fmt["TS"]}}}}}
{{TV}}{{\unreviewed{{{_o4b_fmt["TV"]}}}}}
{{TVerr}}{{\unreviewed{{{_o4b_err_fmt["TV"]}}}}}
{{TVS}}{{\unreviewed{{{_o4b_fmt["TVS"]}}}}}
{{TVSerr}}{{\unreviewed{{{_o4b_err_fmt["TVS"]}}}}}
}}}}

\DeclareRobustCommand{{\TGRPOLlogBImprovement}}[1]{{\IfEqCase{{#1}}{{
{{S}}{{\unreviewed{{{_imp_fmt["S"]}}}}}
{{Serr}}{{\unreviewed{{{_imp_err_fmt["S"]}}}}}
{{V}}{{\unreviewed{{{_imp_fmt["V"]}}}}}
{{Verr}}{{\unreviewed{{{_imp_err_fmt["V"]}}}}}
{{VS}}{{\unreviewed{{{_imp_fmt["VS"]}}}}}
{{VSerr}}{{\unreviewed{{{_imp_err_fmt["VS"]}}}}}
{{TS}}{{\unreviewed{{{_imp_fmt["TS"]}}}}}
{{TSerr}}{{\unreviewed{{{_imp_err_fmt["TS"]}}}}}
{{TV}}{{\unreviewed{{{_imp_fmt["TV"]}}}}}
{{TVerr}}{{\unreviewed{{{_imp_err_fmt["TV"]}}}}}
{{TVS}}{{\unreviewed{{{_imp_fmt["TVS"]}}}}}
{{TVSerr}}{{\unreviewed{{{_imp_err_fmt["TVS"]}}}}}
{{min}}{{\unreviewed{{{_imp_min}}}}}
{{minerr}}{{\unreviewed{{{_imp_minerr}}}}}
{{max}}{{\unreviewed{{{_imp_max}}}}}
{{maxerr}}{{\unreviewed{{{_imp_maxerr}}}}}
}}}}

\DeclareRobustCommand{{\TGRPOLlogBResults}}[1]{{\IfEqCase{{#1}}{{
{{S}}{{\unreviewed{{{_bf_fmt["S"]}}}}}
{{Serr}}{{\unreviewed{{{_bf_err_fmt["S"]}}}}}
{{V}}{{\unreviewed{{{_bf_fmt["V"]}}}}}
{{Verr}}{{\unreviewed{{{_bf_err_fmt["V"]}}}}}
{{VS}}{{\unreviewed{{{_bf_fmt["VS"]}}}}}
{{VSerr}}{{\unreviewed{{{_bf_err_fmt["VS"]}}}}}
{{TS}}{{\unreviewed{{{_bf_fmt["TS"]}}}}}
{{TSerr}}{{\unreviewed{{{_bf_err_fmt["TS"]}}}}}
{{TV}}{{\unreviewed{{{_bf_fmt["TV"]}}}}}
{{TVerr}}{{\unreviewed{{{_bf_err_fmt["TV"]}}}}}
{{TVS}}{{\unreviewed{{{_bf_fmt["TVS"]}}}}}
{{TVSerr}}{{\unreviewed{{{_bf_err_fmt["TVS"]}}}}}
{{min}}{{\unreviewed{{{_bf_min}}}}}
{{minerr}}{{\unreviewed{{{_bf_minerr}}}}}
{{max}}{{\unreviewed{{{_bf_max}}}}}
{{maxerr}}{{\unreviewed{{{_bf_maxerr}}}}}
}}}}
"""

    with open('pol_macro.tex', 'w') as f:
        f.write(pol_macro_string)


def main():
    bf = load_log_bayes_factors()
    generate_paper_figure(bf)
    generate_latex_macros(bf)


if __name__ == '__main__':
    main()
