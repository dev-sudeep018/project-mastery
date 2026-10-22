# Expand a Linear Model’s Features

A linear model is linear in its coefficients, not necessarily in the original input. The feature map [1, x, x²] lets a weighted sum describe a parabola.

Column order matters because every coefficient is attached to a particular power. An ascending Vandermonde matrix makes that convention explicit.

Compare the magnitudes of x and x⁵ for a large input. Richer features can make optimization poorly conditioned; adding powers is a modeling choice, not a guarantee of better generalization.

Concept reference: https://numpy.org/doc/stable/reference/generated/numpy.vander.html
