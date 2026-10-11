# R715 kernel, retiming and whole pooling — draft candidate

Exact local candidate on PR463 R715, with 99 kernel pivots, total entrance rank118, 56 target-sharing receivers, 60 single-gate retimings and14 connected-pair retimings. Pool four replicas with every residual wholly on one physical family.

Exact aggregate bit lower =645473756513106438971/500000000000000000000000. With unchanged PR458 complex root, the arithmetic ceiling c/(1+c) is approximately0.001289283116193776. This is a **projection, not an admitted final kappa**. No cross-family residual splitting.

Local exact rational-span/F2 replay and two rational moment engines pass. Local checks do not settle physical address operators. Pending: emitted global ownership/routes, new cancellation-free physical-family prefix and finite invoice, independent operator audit, strict final outer assembly, fresh full-parent replay, and CI.

Run `python -B research/r715-kernel-pool/verify_component.py /absolute/new/output` for the scoped source reconstruction, local replay, exact whole-family packing and moment checks. It deliberately emits a GLOBAL_PENDING status. Pinned parent packages are inherited from PR462; NumPy/SciPy are not needed for frozen selection expansion.
