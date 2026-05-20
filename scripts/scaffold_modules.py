#!/usr/bin/env python3
"""Scaffold modules 3-8 from module-2 template."""

from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
MODULES = Path(ROOT / "modules")

MODULE_META = {
    3: {
        "theme": "Optimization, loss, and regularization",
        "question": "How do we train deep networks reliably when loss surfaces are non-convex and data are noisy?",
        "lab_title": "Module 3 Lab: SGD vs Adam on a synthetic surface",
        "lab_body": "Compare stochastic gradient descent and Adam on a simple regression task; plot loss curves.",
    },
    4: {
        "theme": "Convolutional neural networks for vision",
        "question": "Why do convolutions, pooling, and translation equivariance matter for image understanding?",
        "lab_title": "Module 4 Lab: CNN feature maps",
        "lab_body": "Inspect convolutional filters and activation maps on a small image dataset.",
    },
    5: {
        "theme": "Sequence models: RNNs and LSTMs",
        "question": "How do recurrent architectures model temporal structure and long-range dependencies?",
        "lab_title": "Module 5 Lab: Sequence prediction",
        "lab_body": "Train a small recurrent model on a character- or token-level sequence task.",
    },
    6: {
        "theme": "Attention and transformers",
        "question": "How does self-attention replace fixed recurrence for language and multimodal tasks?",
        "lab_title": "Module 6 Lab: Attention patterns",
        "lab_body": "Visualize attention weights from a small transformer block on sample inputs.",
    },
    7: {
        "theme": "Generative models and applications",
        "question": "What distinguishes discriminative training from generative modeling in modern AI?",
        "lab_title": "Module 7 Lab: Generative vs discriminative",
        "lab_body": "Contrast a classifier head with a simple generative baseline on the same dataset.",
    },
    8: {
        "theme": "GPU workflows, scale, and deployment",
        "question": "How do practitioners move from notebook experiments to reproducible GPU training pipelines?",
        "lab_title": "Module 8 Lab: GPU profiling checklist",
        "lab_body": "Profile a training step: device placement, batch size, memory, and throughput notes.",
    },
}

MODULE1 = {
    "theme": "From neurons to multilayer networks",
    "question": "How does a stack of differentiable units approximate complex functions from data?",
    "prose_h2": "Perceptrons, MLPs, and representation",
    "prose_lead": "Deep learning begins with simple units composed into layers. A perceptron applies a weighted sum and nonlinearity; multilayer perceptrons stack these transformations to learn hierarchical features.",
    "assign_title": "Designing a baseline MLP",
    "assign_prompt": "Specify an MLP for a tabular or vector classification task: input dimension, hidden layers, activation, and output head. Justify each choice in 600-900 words.",
    "slide_1": "# Neural Units\n\n- Neuron: weighted sum + activation\n- Layers compose representations\n- Depth enables hierarchical features",
    "slide_2": "# Multilayer Perceptrons\n\n- Input → hidden → output\n- Nonlinear activations (ReLU, GELU)\n- Universal approximation in principle; data and optimization matter in practice",
    "lab_title": "Module 1 Lab: Forward pass and activations",
    "lab_body": "Implement a tiny MLP forward pass in NumPy or PyTorch; compare ReLU vs sigmoid on a toy dataset.",
}

MODULE2 = {
    "theme": "Backpropagation and automatic differentiation",
    "question": "How does the chain rule enable efficient learning in deep networks?",
    "prose_h2": "Gradients, backprop, and computational graphs",
    "prose_lead": "Training requires computing gradients of a loss with respect to parameters. Backpropagation applies the chain rule layer by layer; modern frameworks build dynamic computational graphs so practitioners focus on architecture and data.",
    "assign_title": "Tracing gradients through a graph",
    "assign_prompt": "Draw or describe the computational graph for a two-layer network with MSE loss. Identify which intermediate values backprop must store. Submit 600-900 words plus a diagram.",
    "slide_1": "# Computational Graphs\n\n- Nodes: operations and tensors\n- Edges: data dependencies\n- Autograd records operations for reverse-mode AD",
    "slide_2": "# Backpropagation\n\n- Forward pass computes activations\n- Backward pass applies chain rule\n- Vanishing/exploding gradients motivate architecture choices",
    "lab_title": "Module 2 Lab: Manual vs autograd gradients",
    "lab_body": "Verify a hand-derived gradient for a scalar loss against `torch.autograd` on a tiny network.",
}


def patch_file(path: Path, replacements: dict[str, str]) -> None:
    text = path.read_text()
    for old, new in replacements.items():
        text = text.replace(old, new)
    path.write_text(text)


def write_assignment_ipynb(path: Path, n: int, meta: dict) -> None:
    title = meta.get("assign_title", f"Module {n} Assignment")
    prompt = meta.get(
        "assign_prompt",
        f"Apply concepts from Module {n} ({meta['theme']}). Submit a 600–900 word technical memo with code snippets or diagrams as needed.",
    )
    path.write_text(
        f'''{{
 "cells": [
  {{
   "cell_type": "markdown",
   "metadata": {{}},
   "source": [
    "# Module {n} Assignment\\n",
    "\\n",
    "## {title}\\n",
    "\\n",
    "## Prompt\\n",
    "\\n",
    "{prompt}\\n",
    "\\n",
    "## Deliverable\\n",
    "\\n",
    "Submit your memo and any notebook outputs via the course LMS."
   ]
  }},
  {{
   "cell_type": "code",
   "metadata": {{"tags": ["thebe"]}},
   "source": ["# Draft notes\\nnotes = \\"\\"\\nnotes"],
   "execution_count": null,
   "outputs": []
  }}
 ],
 "metadata": {{"kernelspec": {{"display_name": "Python 3", "language": "python", "name": "python3"}}}},
 "nbformat": 4,
 "nbformat_minor": 5
}}
'''
    )


def scaffold_module(n: int, meta: dict) -> None:
    src = MODULES / "module-1"
    dst = MODULES / f"module-{n}"
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    (dst / "assignment.md").unlink(missing_ok=True)

    overview = dst / "overview.md"
    overview.write_text(
        f"""# Module {n} Overview

## Theme

{meta["theme"]}

## Essential Question

{meta["question"]}

## Module Components

- `Book prose`: concepts and methods for this module
- `Assignment`: applied analysis or implementation brief
- `Slides`: presentation sequence for seminar or lecture delivery
- `Narration`: spoken version of the slide flow
- `Instructor notes`: facilitation tips and misconceptions
- `Notebook`: executable lab aligned with the module theme
"""
    )

    prose = dst / "book-prose.md"
    prose.write_text(
        f"""# Module {n} Book Prose

## {meta["theme"]}

{meta["question"]}

This module connects theory to practice: students read the conceptual framing, complete the assignment, use slides and narration for structured delivery, and run the lab notebook to make ideas concrete.

## Why This Module Matters

Deep learning courses fail when students memorize architecture names without understanding the problem each family solves. This module situates **{meta["theme"].lower()}** inside the broader AIN6003 arc: representation → training → architectures → scale.

## Study Questions

1. What problem structure does this module's methods assume?
2. What failure modes appear when data, compute, or objectives mismatch the method?
3. How would you explain this module to a technical stakeholder in two minutes?
"""
    )

    write_assignment_ipynb(dst / "assignment.ipynb", n, meta)

    slides = dst / "slides.ipynb"
    slides.write_text(
        f'''{{
 "cells": [
  {{
   "cell_type": "markdown",
   "metadata": {{"slideshow": {{"slide_type": "slide"}}}},
   "source": ["# Module {n}\\n\\n- {meta['theme']}\\n- Essential question on every slide deck\\n- Link reading to lab"]
  }},
  {{
   "cell_type": "markdown",
   "metadata": {{"slideshow": {{"slide_type": "slide"}}}},
   "source": ["# Key Ideas\\n\\n- Concept 1\\n- Concept 2\\n- Concept 3"]
  }},
  {{
   "cell_type": "markdown",
   "metadata": {{"slideshow": {{"slide_type": "slide"}}}},
   "source": ["# Lab & Assignment\\n\\n- Notebook: hands-on practice\\n- Assignment: synthesis and justification"]
  }}
 ],
 "metadata": {{"kernelspec": {{"display_name": "Python 3", "language": "python", "name": "python3"}}}},
 "nbformat": 4,
 "nbformat_minor": 5
}}
'''
    )

    narration = dst / "narration.md"
    narration.write_text(
        f"""# Module {n} Narration

## Opening

Introduce **{meta["theme"]}** and restate the essential question. Tell students what they will be able to do after the module.

## Middle

Walk through the slide sequence: definitions first, then intuition, then limitations. Pause for one discussion prompt tied to real applications (vision, language, or operations).

## Closing

Connect this module to the next step in the course arc. Remind students to run the lab before drafting the assignment.
"""
    )

    instructor = dst / "instructor-notes.md"
    instructor.write_text(
        f"""# Module {n} Instructor Notes

## Teaching Goal

Students should connect **{meta["theme"].lower()}** to concrete design choices, not only vocabulary.

## Misconceptions

- Treating every deep model as a transformer
- Ignoring data scale and label quality
- Assuming GPU access fixes poor problem framing

## Facilitation

- Start from a failure case, then introduce the method that addresses it.
- Keep one running example (e.g., image or text) across modules when possible.

## Grading Cue

Reward clear reasoning about tradeoffs; do not require state-of-the-art benchmark scores in introductory work.
"""
    )

    nb_dst = ROOT / "notebooks" / f"module-{n}-lab.ipynb"
    nb_dst.write_text(
        f'''{{
 "cells": [
  {{
   "cell_type": "markdown",
   "metadata": {{}},
   "source": ["# {meta["lab_title"]}\\n\\n{meta["lab_body"]}"]
  }},
  {{
   "cell_type": "code",
   "metadata": {{"tags": ["thebe"]}},
   "source": ["# Scaffold: import core libraries\\nimport math\\nprint(\\"Module {n} lab ready\\")"],
   "execution_count": null,
   "outputs": []
  }}
 ],
 "metadata": {{"kernelspec": {{"display_name": "Python 3", "language": "python", "name": "python3"}}}},
 "nbformat": 4,
 "nbformat_minor": 5
}}
'''
    )


def update_module_1_2() -> None:
    m1 = MODULES / "module-1"
    m1.joinpath("overview.md").write_text(
        f"""# Module 1 Overview

## Theme

{MODULE1["theme"]}

## Essential Question

{MODULE1["question"]}

## Module Components

- `Book prose`: perceptrons, MLPs, activations, and representation
- `Assignment`: baseline MLP design brief
- `Slides`: from single units to layered networks
- `Narration`: spoken flow for asynchronous delivery
- `Instructor notes`: facilitation and misconceptions
- `Notebook`: forward pass and activation comparison
"""
    )
    m1.joinpath("book-prose.md").write_text(
        f"""# Module 1 Book Prose

## {MODULE1["prose_h2"]}

{MODULE1["prose_lead"]}

## Depth and Width

Adding hidden layers increases expressive power but also optimization difficulty. Students should understand depth as a modeling choice tied to data complexity, not as a default.

## Activations

ReLU and its variants dominate modern feedforward networks because they mitigate vanishing gradients in many settings. Sigmoid and tanh remain relevant for gating and certain output heads.

## Connection to the Rest of the Course

Module 1 establishes the feedforward picture that backpropagation (Module 2), optimization (Module 3), and specialized architectures (Modules 4–7) extend.
"""
    )

    m2 = MODULES / "module-2"
    m2.joinpath("overview.md").write_text(
        f"""# Module 2 Overview

## Theme

{MODULE2["theme"]}

## Essential Question

{MODULE2["question"]}

## Module Components

- `Book prose`: computational graphs and backpropagation
- `Assignment`: gradient tracing exercise
- `Slides`: forward and backward passes
- `Narration`: asynchronous slide narration
- `Instructor notes`: teaching notes
- `Notebook`: manual vs autograd gradient check
"""
    )
    m2.joinpath("book-prose.md").write_text(
        f"""# Module 2 Book Prose

## {MODULE2["prose_h2"]}

{MODULE2["prose_lead"]}

## Vanishing and Exploding Gradients

Deep stacks amplify gradient products across layers. Architecture (residual connections, normalization), activations, and optimization choices interact to keep training stable.

## Framework Practice

PyTorch and similar libraries implement reverse-mode autodiff. Students should spend less time deriving every partial derivative by hand and more time interpreting gradient flow and debugging training.
"""
    )

    for n, mod in [(1, MODULE1), (2, MODULE2)]:
        slides = MODULES / f"module-{n}" / "slides.ipynb"
        s1 = mod["slide_1"].replace("\n", "\\n")
        s2 = mod["slide_2"].replace("\n", "\\n")
        slides.write_text(
            f'''{{
 "cells": [
  {{"cell_type": "markdown", "metadata": {{"slideshow": {{"slide_type": "slide"}}}}, "source": ["{s1}"]}},
  {{"cell_type": "markdown", "metadata": {{"slideshow": {{"slide_type": "slide"}}}}, "source": ["{s2}"]}}
 ],
 "metadata": {{"kernelspec": {{"display_name": "Python 3", "language": "python", "name": "python3"}}}},
 "nbformat": 4,
 "nbformat_minor": 5
}}
'''
        )
        nb = ROOT / "notebooks" / f"module-{n}-lab.ipynb"
        nb.write_text(
            f'''{{
 "cells": [
  {{"cell_type": "markdown", "metadata": {{}}, "source": ["# {mod["lab_title"]}\\n\\n{mod["lab_body"]}"]}},
  {{"cell_type": "code", "metadata": {{"tags": ["thebe"]}}, "source": ["import math\\nprint(\\"Module {n} lab\\")"], "execution_count": null, "outputs": []}}
 ],
 "metadata": {{"kernelspec": {{"display_name": "Python 3", "language": "python", "name": "python3"}}}},
 "nbformat": 4,
 "nbformat_minor": 5
}}
'''
        )


def write_toc() -> None:
    lines = ["format: jb-book", "root: intro", "chapters:", "  - file: syllabus"]
    for n in range(1, 9):
        lines.append(f"  - file: modules/module-{n}/overview")
        lines.append("    sections:")
        for part in [
            "book-prose",
            "assignment",
            "slides",
            "narration",
            "instructor-notes",
        ]:
            lines.append(f"      - file: modules/module-{n}/{part}")
        lines.append(f"      - file: notebooks/module-{n}-lab")
    (ROOT / "_toc.yml").write_text("\n".join(lines) + "\n")


def main() -> None:
    update_module_1_2()
    write_assignment_ipynb(MODULES / "module-1" / "assignment.ipynb", 1, MODULE1)
    write_assignment_ipynb(MODULES / "module-2" / "assignment.ipynb", 2, MODULE2)
    (MODULES / "module-2" / "assignment.md").unlink(missing_ok=True)
    for n, meta in MODULE_META.items():
        scaffold_module(n, meta)
    write_toc()
    print("Scaffolded modules 1-8 and _toc.yml")


if __name__ == "__main__":
    main()
