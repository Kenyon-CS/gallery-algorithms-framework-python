# Gallery Algorithms Framework (Python)

A Python version of the gallery layout starter project for experimenting with algorithms that place artworks into gallery zones.

This mirrors the structure and behavior of the C++ starter, but uses a small pure-Python codebase so students can read and modify it easily.

## What it does

- reads a simplified YAML-like gallery file
- reads a simplified YAML-like show file
- reads an optional scoring configuration file
- builds internal Python data structures
- runs one of two baseline algorithms:
  - `greedy`
  - `random`
- evaluates the resulting layout
- prints a score breakdown and placement summary

## Why the parser is only "YAML-like"

To keep the starter simple and dependency-free, this version uses a tiny handwritten parser for a restricted subset of YAML.

That means:

- indentation is for readability only
- the files should follow the examples in `data/`
- advanced YAML features are not supported

This is deliberate. One early assignment can be to improve or replace the parser.

## Project layout

```text
gallery-algorithms-framework-python/
├─ README.md
├─ requirements.txt
├─ run.py
├─ data/
│  ├─ gallery.yaml
│  ├─ show.yaml
│  └─ scoring.yaml
└─ gallery/
   ├─ __init__.py
   ├─ types.py
   ├─ models.py
   ├─ util.py
   ├─ parser.py
   ├─ evaluator.py
   ├─ algorithm.py
   └─ algorithms/
      ├─ __init__.py
      ├─ greedy.py
      └─ random_algorithm.py
```

## Requirements

- Python 3.10 or newer recommended
- No external packages required

## Run

From the project root:

```bash
python3 run.py data/gallery.yaml data/show.yaml greedy data/scoring.yaml
```

Or without an explicit scoring file:

```bash
python3 run.py data/gallery.yaml data/show.yaml greedy data/scoring.yaml
```

You can also use the random baseline:

```bash
python3 run.py data/gallery.yaml data/show.yaml random data/scoring.yaml
```

## Sample output

```text
Gallery Planner
===============
Gallery:   Kenyon Teaching Gallery
Show:      Light, Motion, and Structure
Algorithm: greedy

Score Breakdown
---------------
Compatibility:   75.00
Capacity:        0.00
Lighting:        -5.00
Room Preference: 40.00
Unplaced:        0.00
Duplicate Use:   0.00
TOTAL:           110.00
```

## Use

This Python version is a good base for goals such as:

- add new scoring features
- implement backtracking or hill climbing
- track wall width instead of one-artwork-per-zone capacity
- support placement constraints
- replace the handwritten parser with real YAML
- compare algorithm performance across many random shows
