# Repair Global Gradient Clipping

Global norm clipping changes the update's length while preserving its direction. It multiplies every coordinate of every gradient tensor by the same nonnegative factor.

Clipping each tensor separately changes the relative contribution of different parameter groups. Clipping individual coordinates can also rotate the update; neither operation is this lesson's contract.

Returning the norm before clipping lets an experiment record when clipping activated. A small returned clipped norm alone would hide how large the original gradient was.

Run the flawed starter on the first example and compare coordinate ratios before and after. Clipping can limit a single step, but it does not repair an incorrect derivative or guarantee stable training.

## Further reading

- Global norm definition: https://docs.pytorch.org/docs/stable/generated/torch.nn.utils.clip_grad_norm_.html
