# Trace a Gradient Through ReLU

The chain rule multiplies the local derivative by the upstream derivative. A positive x opens the gate; it does not force the incoming gradient to be positive.

At a negative x, a small change leaves the forward output unchanged, so the local derivative is zero. At a positive x, the local derivative is one.

At exactly zero, the two one-sided slopes disagree. This activity chooses zero for the backward pass. Check finite differences away from that boundary, where a derivative exists.

Change only the sign of an upstream entry attached to a positive activation. The returned gradient should change sign too. Explain what learning signal would be lost by applying ReLU to upstream itself.
