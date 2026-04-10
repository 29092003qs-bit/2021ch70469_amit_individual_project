# Self-Organized Criticality in the Bak-Tang-Wiesenfeld Sandpile Model

## Overview
This repository contains all materials for the individual complexity science project
(April 2026) demonstrating **Self-Organized Criticality (SOC)** using the
**Bak-Tang-Wiesenfeld (BTW) Sandpile Model**.

## Files
| File | Description |
|------|-------------|
| `code.py` | Python simulation (main code) |
| `project_report.tex` | LaTeX source for the journal-style report |
| `project_report.pdf` | Compiled PDF report |
| `figures/` | All generated plots (auto-created by simulation) |

## Requirements
```bash
pip install numpy matplotlib scipy
```

## How to Run
```bash
python code.py
```
This generates all figures in the `figures/` directory.

## To Compile the LaTeX Report
```bash
pdflatex project_report.tex
pdflatex project_report.tex   # run twice for cross-references
```

## Model Description
The Bak-Tang-Wiesenfeld (BTW) sandpile model is a cellular automaton on an L×L grid.

**Rules (applied synchronously each step):**
1. Add a grain to a random site.
2. If site height exceeds a threshold ($z_c$), it topples, distributing $z_c$ grains to its neighbors.
3. Grains falling off the edge are removed from the system.

**Parameters:**
- L = 50
- 25,000 steps total; 5,000 step burn-in
- Both 4-neighbor (von Neumann, $z_c=4$) and 8-neighbor (Moore, $z_c=8$) topologies tested

## Key Results
| Connectivity | Power-law exponent τ | Max avalanche |
|:---:|:---:|:---:|
| 4 (von Neumann) | 0.99 | 6833 |
| 8 (Moore) | 1.31 | 5978 |
