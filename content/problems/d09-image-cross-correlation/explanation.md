# Slide a Filter over an Image

A local filter shares the same weights across positions. Cross-correlation takes a weighted sum of each local image window, making the operation sensitive to spatial patterns.

The kernel stays in its supplied orientation. Many neural-network convolution layers use this cross-correlation convention; mathematical convolution would reverse the kernel.

Try the kernel [1, -1] on a constant row and on a step. Explain why the response is zero in flat regions and changes sign when you reverse the edge.

Concept reference: https://d2l.ai/chapter_convolutional-neural-networks/conv-layer.html
