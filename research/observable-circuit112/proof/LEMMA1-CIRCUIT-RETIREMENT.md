# Lemma 1: closed response-circuit retirement with exact paid accounting

## Sufficient statement

Fix a reversible linear scalar body on source, target and dirty helper registers
over a field K. Background writes read only background registers, and their
inverse sequence restores the background after the body. Let C_h denote the
target response to helper h. Consider disjoint kernel classes. A class has a
common entrance E of dimension e, independent donor response columns C_d for
d in D, and pivots P disjoint from D satisfying

    C_p = sum_(d in D) q_(d,p) C_d.

Assume E is contained in the first frame F_h of each participating helper.
The response construction prepends the invertible donor shears
d := d - q_(d,p)*p at E, admits the pivot at E, pays each donor's entrance
climb, and rebuilds compensation and inverse cleanup. Retire subsets D0 of D
and P0 of P such that every retained pivot has zero coefficient on every donor
in D0, and every retained donor is used by a retained pivot. Leave all other
classes, gauges, scalar body and frame labels unchanged. Rebuild this response
construction with D minus D0 and P minus P0. Then:

1. The exact target map and restoration of every arbitrary dirty helper are
   preserved after the rebuilt compensation and cleanup.
2. With f_h = dim F_h, the change in the local child-rank histogram is

       sum_(h in D0 union P0) ([f_h] - [f_h-e]) - |D0| [e].

   Here [r] means one rank-r child and [0] means no child. Changes from disjoint
   classes add as histograms, not as independently priced exponent gains.
3. Total local child-rank mass increases by e*|P0|. Exactly the same number of
   residual helper axes must be physically supplied. A gain follows only if an
   actual new physical allocation and its entire paid profile pass the recurrence
   and outer assembly inequalities.

The last item is an explicit construction requirement, not a claim that those
axes are free. Lemma 4 and the literal owner map supply them in this artifact.

## Proof of correctness

The donor and pivot sets are disjoint. Each donor shear reads an unchanged pivot
and writes a distinct donor, so these shears are invertible. Their combined
effect on the pivot response is C_p - sum_d q_(d,p) C_d = 0. Donor responses
are unchanged. Thus the admitted entrance for each retained pivot is justified
by the same exact response identity as before. The zero coefficients on retired
donors prove that no retained cancellation depended on a deleted shear.
Independence of the donor columns makes the coefficients unique, so this
condition can be checked against the old relations without a basis ambiguity.

Retired pivots simply return to their ordinary full first-frame entrance. Their
registers are not deleted or identified with other dirty registers. Retired
donors return to their ordinary entrance as well. Consequently every first-frame
transition remains a legal nested-frame transition. Recompute the actual dirty
response of the modified program and prepend its negative compensation using
the same admitted response-construction interface. This is a concrete finite
linear map obtained from the emitted body; it is not an assumed new oracle.
The compensation cancels that response on every helper column. The source-to-
target operator is unchanged because these entrance shears only change helper
coordinates and their compensated response. Finally, reversing the actual
background-writing sequence restores every background coordinate. The closed
background condition ensures that omitting target writes from cleanup is sound.
These facts prove equality on arbitrary initial states. The finite application
independently checks all columns and the inverse-transpose orientation as well.

## Proof of the histogram and stock identity

For a participating helper h the common entrance cuts the original first climb
of rank f_h into a rank-(f_h-e) climb. A donor additionally pays one rank-e
entrance child. An admitted pivot at E has residual width h-e, where h is the
ambient frame dimension; retiring it restores width h and consumes e additional
physical axes. Retiring a donor therefore replaces children
[e]+[f_h-e] by [f_h]. Retiring a pivot replaces [f_h-e] by [f_h]. All later
frames and their transitions are unchanged. Summing these replacements proves
the histogram formula, including zero-rank cases.

Taking rank mass gives e per retired participant minus e per retired donor,
hence e*|P0|. The donor complement width is unchanged; each retired pivot's
width grows by e. Thus total complement-width growth equals the rank-mass
growth. A valid hosting map consumes those axes from actual remaining physical
slots. Its leftover recursive children must be counted afresh. This proves the
accounting identity and explains why choosing the largest possible number of
kernel pivots need not minimize the complete recurrence moment.

## Checked application in this package

The frozen 99-pivot rank-sector source is rebuilt from the packaged ancestry.
Two disjoint closed components are retired:

- E=[6]: donors 9,11,12,508,509,511; pivots 8,13,14,184,185,510.
- E=[480]: donors 272,273,298; pivot 299.

Both entrances have dimension one. The constructor solves old and retained
relations exactly over Q, checks support closure and donor use, rebuilds every
compensation and cleanup event, and compares the predicted histogram with the
actual emitted word. All coefficients meet the inherited dyadic contract.

The resulting 92-pivot local histogram on 120 ports is

    {1:2459,2:182,3:522,4:88,5:238,6:128,7:1,8:17}.

The exact delta is {1:-15,3:+6,5:-4,6:+4}, of rank mass seven. Seven helpers
widen from eight to nine axes in each of 72 invocations: 504 additional axes
are supplied and subtracted from actual physical remainders by Lemma 4.
The width inventory becomes {7:18,8:154,9:388}; all 560 helpers are retained.
After Lemma 2's profile-preserving slicing and Lemma 3's isolated restriction,
the 112-port local histogram is

    {1:2451,2:182,3:522,4:88,5:238,6:128,7:1,8:1}.

The authoritative global profile and exact exponent are in EXPECTED.json. The
constructor is code/build_circuit_retirement.py; the generated receipt is
source120/base/retired/RETIREMENT.json inside the chosen replay directory.
This is a mathematical lemma with exact finite checks, not a new Lean theorem
or a claim that the inherited response-kernel identity is globally novel.
