
NAMD’s implementation of REST2 solute scaling (in versions 2.13, 2.14, and the
master repository) does not apply scaling to Urey-Bradley or NBFIX energy terms,
in disagreement with the formal REST2 implementation in the NAMD user guide.

Solution: 
#########
Urey-Bradley can be scaled by altering line 145 of ComputeAngles.C
(https://charm.cs.illinois.edu/gerrit/plugins/gitiles/namd/+/refs/heads/master/src/ComputeAngles.C#145)
where “BigReal k_ub = value->k_ub;” becomes “BigReal k_ub = value->k_ub *
scale;” as coded in Jo & Jiang’s original 2015 patch that ported REST2 to NAMD
2.10
(https://github.com/sunhwan/NAMD-REST/blob/master/src/ComputeAngles.C#L123).

NBFIX can be scaled by altering LJTable.C. The problem there is that atoms with
solute scaling “overwrite” the NBFIX Lennard-Jones parameters, so only the
NONBONDED LJ parameters are applied and not the NBFIX parameters. I propose a
fix in the attached version of LJTable.C. In short, this fix pulls the NBFIX
parameters A and B when solute scaling is applied instead of the NONBONDED LJ
parameters.

Testing:
########

To demonstrate this issue, I propose two cases. First, asparagine features an
Urey-Bradley term. Second, a simple system of one sodium and one chloride ion
can be used to test NBFIX. For simplicity, both systems are studied in vacuo.

In the NAMD user guide and elsewhere in literature, the scaled energy U is, U =
beta * U_{1} + sqrt(beta) * U_{01} + U_{0}

The test sets beta = 0.5 with all atoms participating in REST2 scaling, i.e., U
= beta * U_{1}, with bonded and angle scaling turned on. Therefore, we would
expect that the unscaled energy U (when beta = 1) should be twice larger than
the scaled energy.

When running this test, NAMD 2.14 shows that bonded, dihedral, and electrostatic
energy terms have U_{scaled} / U_{unscaled} = beta = 0.5 as expected. However,
this is untrue for angle and van der Waals terms. These observed betas are:
beta_{obs, angle} = 0.76404  # for the asparagine system 
beta_{obs, vdw} = 0.424655  # for the sodium-chlordie system

The proposed fix brings beta_{obs, angle} = beta_{obs, vdw} = beta = 0.5 as
expected.

Additional Remarks:
###################
Note that this issue was raised in Feb 2019 by Jeff Comer on the NAMD mailing list (https://www.ks.uiuc.edu/Research/namd/mailing_list/namd-l.2019-2020/0160.html), and it doesn't seem like there was a resolution.


