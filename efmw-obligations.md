# Physical and mathematical obligations beyond the finite certificates

| Obligation | Result | Evidence / next condition |
|---|---|---|
| Coverage of frozen catalogue | Demonstrated computationally | 165 unique blocks, all 585 statements; fail-closed parser |
| Scalar polynomial variation | Demonstrated in finite formal model | 360 kernel-checked magnitude identities; signs separately fail |
| Real polynomial semantics and scalar continuum bridge | Formalized with explicit hypotheses in `continuum/` | Normalizer soundness, real derivatives, flat-spacetime action variation, and stationarity-to-scalar-PDE; see CONTINUUM_BRIDGE.md |
| Literal equivalence of full catalogue | Rejected as an identity claim under C1 conventions | Sign, current and tensor mismatches; degenerate parameter choices may make some discrepancies vanish |
| Free scalar kinetic sign | Correct at canonical free limit | (-+++) kinetic term gives positive time kinetic energy |
| Free scalar dispersion | Correct for nonnegative mass squared | omega^2 = k^2 + m^2 |
| Global potential stability | Not guaranteed by the family | Generic nonzero cubic scalar interactions are unbounded below |
| Effective kinetic and causal stability | Unresolved | Gauge constitutive Hessian and coupled gravity/scalar principal symbol must be checked on specified backgrounds |
| Higher derivative control | Unresolved | R*F^2-type terms introduce higher derivatives in mixed equations; an EFT cutoff, order reduction or a proven degeneracy structure is required |
| Gauge invariance | Demonstrated at action-expression level | Potentials enter only through F=dA and H=dB; gamma and real-scalar current insertions excluded |
| Current matching to original | Rejected / underdefined | 88 incompatible neutral-scalar current expressions, 2 unresolved-current equations |
| Stress conservation | Analytic on-shell identity | Closed covariant action and all field equations; no separately prescribed source hidden in C1 |
| Full curved-space variational proof in Lean | Open | The new scalar bridge uses real analysis and integration by parts on fixed Minkowski spacetime; curved metric/gauge variation remains open |
| Boundary problem / well-posedness | Open | Only compactly supported variation is used; no global PDE existence/uniqueness claim |
| Rotational source P | Underdefined physically | Need local invariant, dimensions, dynamical variables, measurement and backreaction |
| Empirical status | Unestablished | No new experiment or parameter fit is contained in this package |

## Explicit instability example

Restrict to three scalar fields with unit masses, all pair couplings zero and $h_{abc}=1$. Along $\varphi_a=\varphi_b=\varphi_c=t$ in flat spacetime,

$$U(t)=\tfrac32t^2+t^3\longrightarrow-\infty\quad(t\longrightarrow-\infty).$$

Thus positive free kinetic terms and a successful algebraic audit do not imply a bounded interacting Hamiltonian. Setting the cubic coefficients to zero and imposing a positive mass matrix can repair this particular issue. Adding stabilizing quartics changes the frozen C1 ansatz and requires a new version. A restricted EFT domain is another explicitly limited interpretation, not a global stability proof.

## Normalizations are assumptions

An energy-density interpretation of the root source requires [E]=[cP]. If E is measured in J/m^3, then P has units J*s/m^4 and the root field has units kg/m; Z then supplies the action normalization (with units matching G). This dimensional possibility does not identify P with angular velocity or vorticity. Natural-unit normalization of the eight canonical fields does not resolve the physical root-source identification automatically.

## Projection is not a consistent truncation theorem

The audit first deletes couplings naming inactive sectors and then varies the restricted action. This defines a family of submodels. It is not the claim that arbitrary solutions of a retained triplet solve the unrestricted 11-sector theory. In the unrestricted theory a term h_abc*phi_a*phi_b*phi_c can source an omitted phi_c even when phi_c=0. The required coupling deletion is a substantive part of the frozen projection rule.

## Predetermined next tests

1. Choose a background and numerical coefficient domain before a stability calculation. Pass only if the relevant physical kinetic matrix has no negative modes, constraints close and the principal symbol is hyperbolic in that domain. A failed background is retained as a counterexample.
2. Specify the rotational/matter source independently of the desired scalar response. Pass the source audit only if units, transformation law and backreaction are explicit; fitting an undefined P to the observed answer fails.
3. Reproduce the Einstein–Maxwell limit by setting mixed couplings and extra fields to zero. A surviving extra source term fails that limit.
4. Freeze an experimental prediction and comparator before viewing the test data. A mathematical certificate alone never upgrades an empirical status.
