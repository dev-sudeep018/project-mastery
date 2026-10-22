# Keep Classes in Both Data Splits

Stratification allocates examples within classes so a small class is not accidentally absent from evaluation. Clipping the allocation leaves at least one row of each observed class on each side.

Split indices before fitting transforms, then fit preprocessing on training rows only. The returned indices preserve original order for transparent inspection.

This deterministic policy is an exercise in allocation, not a universal sampling strategy. If rows are time-ordered or grouped by person, explain why random or stratified row splitting can still produce misleading evaluation.

Concept reference: https://scikit-learn.org/stable/modules/cross_validation.html#stratification
