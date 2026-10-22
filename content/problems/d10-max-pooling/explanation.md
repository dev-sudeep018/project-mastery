# Downsample Local Activations

Max pooling keeps a local extreme while discarding precise within-window position. This changes the representation and spatial resolution without learning a kernel.

Output positions begin at zero and advance by stride while the complete window fits. Initializing a maximum to zero would incorrectly erase all-negative windows.

Move the largest pixel within a non-overlapping window and compare outputs. Then move it across a window boundary to identify the limit of this local invariance.

Concept reference: https://d2l.ai/chapter_convolutional-neural-networks/pooling.html
