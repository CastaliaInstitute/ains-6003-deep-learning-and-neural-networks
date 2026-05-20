# Module 2 Book Prose

## Gradients, backprop, and computational graphs

Training requires computing gradients of a loss with respect to parameters. Backpropagation applies the chain rule layer by layer; modern frameworks build dynamic computational graphs so practitioners focus on architecture and data.

## Vanishing and Exploding Gradients

Deep stacks amplify gradient products across layers. Architecture (residual connections, normalization), activations, and optimization choices interact to keep training stable.

## Framework Practice

PyTorch and similar libraries implement reverse-mode autodiff. Students should spend less time deriving every partial derivative by hand and more time interpreting gradient flow and debugging training.
