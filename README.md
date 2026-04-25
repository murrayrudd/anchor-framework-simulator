# Institutional Anchor Framework

Interactive simulator and Python reproduction code for the institutional-anchor framework for the supply side of time preference, based on Rudd (2026).

## Overview

This repository accompanies a working paper that develops a formal framework in which revealed time preferences emerge from an institutional environment characterized by the supply of durable anchor stocks (biophysical, institutional, and historical), the rate of information velocity, and the deliberative capacity available to engage with anchor material. The framework specifies the structural channels through which compressive technologies erode the conditions for long-horizon deliberation, and the conditions under which deliberative infrastructure can offset compressive pressure.

## Two ways to use this repository

### Interactive simulator (no installation required)

A browser-based simulator with adjustable parameters and five chart views corresponding to the paper's main figures.

**Live tool:** <https://murrayrudd.github.io/anchor-framework-simulator/>

The simulator is intended for readers who want to develop intuition for the framework's behavior — how effective time preference responds to information velocity, where threshold and hysteresis structures emerge, how deliberative capacity can offset (or fail to offset) compressive pressure. All computations run client-side; no data is collected or transmitted. The single-file implementation (`index.html`) has no build step or server dependencies.

### Python reproduction (academic and research use)

A Python module reproducing all figures in the paper and providing the framework's equations as a callable API for extension and sensitivity analysis.

The Python code is in the [`python/`](python/) directory. See [`python/README.md`](python/README.md) for installation, usage, and parameter calibration details.

## What's in this repository

```
anchor-framework-simulator/
├── README.md                       # This file
├── LICENSE                         # MIT License
├── CITATION.cff                    # Citation metadata
├── index.html                      # Interactive simulator (single file)
└── python/
    ├── README.md                   # Python-specific documentation
    ├── requirements.txt            # Dependencies (numpy, scipy, matplotlib)
    ├── anchor_framework.py         # Core framework module
    └── generate_figures.py         # Reproduces all paper figures
```

## Research basis

This repository implements the framework described in:

- **Rudd, M.A. (2026).** An institutional framework for modeling the supply side of time preference. *SSRN preprint*. <https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6630139>

Building on:

- **Rudd, M.A. (2026).** The volitional deficit: institutional economics, Bitcoin governance, and the challenge of algorithmic velocity. *SSRN preprint*. <https://dx.doi.org/10.2139/ssrn.6556019>

## Citation

If you use this code or simulator in research or publications, please cite the underlying paper:

```bibtex
@article{Rudd2026anchor,
  author  = {Rudd, Murray A.},
  title   = {An institutional framework for modeling the supply side of time preference},
  journal = {SSRN preprint},
  year    = {2026}
}
```

For citation of the code itself, see [`CITATION.cff`](CITATION.cff) or click "Cite this repository" on the GitHub page.

## License

MIT License. See [LICENSE](LICENSE) for details.

## Author

**Murray A. Rudd, Ph.D.** — Institutional economist and policy researcher

- Blog: [murrayrudd.pro](https://murrayrudd.pro)
- ORCID: [0000-0001-9533-5070](https://orcid.org/0000-0001-9533-5070)
- Google Scholar: [Profile](https://scholar.google.co.uk/citations?hl=en&user=84qbofEAAAAJ)
