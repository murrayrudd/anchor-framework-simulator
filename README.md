# Institutional Anchor Framework

Python reproduction and extension code for the "Keeping the future visible: institutional anchors and time preference in ecosystem service valuation" working paper from Rudd (2026).

## Overview

This repository accompanies a paper that develops a formal framework in which revealed time preferences emerge from an institutional environment characterized by the supply of durable anchor stocks (biophysical, institutional, and historical), the rate of information velocity, and the deliberative capacity available to engage with anchor material. The biophysical anchor is split into a physical natural capital stock and the legible reference that monitoring and discovery produce from it, distinguishing the physical state of an ecosystem from the institutional capacity to keep that state visible. The framework specifies the structural channels through which compressive technologies erode the conditions for long-horizon deliberation and the conditions under which deliberative infrastructure can offset compressive pressure.

The code reproduces all figures in the paper and exposes the framework's equations as a callable API for extension and sensitivity analysis. The default parameters are illustrative rather than empirically estimated; the framework is diagnostic, and its structural parameters are intended to be calibrated against evidence for the system under study.

## Usage

The code is in the [`python/`](python/) directory and requires Python 3.8 or later.

```bash
cd python
pip install -r requirements.txt
python generate_figures.py        # regenerates Figures 1-7 (PNG + SVG)
```

To use the framework programmatically:

```python
from anchor_framework import FrameworkParameters, rho_star, baseline_stocks, simulate_dynamics

p = FrameworkParameters()                 # default (illustrative) calibration
rho = rho_star(v=2.0, D=1.5, p=p)         # steady-state effective time preference
N0, B0, I0, H0 = baseline_stocks(1.0, 1.0, p)
```

See [`python/README.md`](python/README.md) for the model structure, the full API, and parameter-calibration details.

## What's in this repository

```
anchor-framework-simulator/
├── README.md                       # This file
├── LICENSE                         # MIT License
├── CITATION.cff                    # Citation metadata
└── python/
    ├── README.md                   # Model structure, API, and calibration
    ├── requirements.txt            # Dependencies (numpy, scipy, matplotlib)
    ├── anchor_framework.py         # Core framework module (four-stock N/B model)
    └── generate_figures.py         # Reproduces all paper figures
```

## Research basis

This repository implements the framework described in:

- **Rudd, M.A. (2026).** Keeping the future visible: institutional anchors and time preference in ecosystem service valuation. *SSRN preprint*. *[URL to follow]*

Building on:

- **Rudd, M.A. (2026a).** The temporal architecture of deliberation under emerging technologies. *SSRN preprint*. <https://dx.doi.org/10.2139/ssrn.6630139>

## Citation

If you use this code in research or publications, please cite the underlying paper:

```bibtex
@article{Rudd2026anchor,
  author  = {Rudd, Murray A.},
  title   = {Keeping the future visible: institutional anchors and time preference in ecosystem service valuation},
  journal = {SSRN preprint},
  year    = {2026},
  note    = {URL to follow}
}
```

For citation of the code itself, see [`CITATION.cff`](CITATION.cff) or click "Cite this repository" on the GitHub page.

## License

MIT License. See [LICENSE](LICENSE) for details.

## Author

**Murray A. Rudd, Ph.D.** — Institutional economist and policy researcher

- ORCID: [0000-0001-9533-5070](https://orcid.org/0000-0001-9533-5070)
- SSRN: [SSRN profile](https://papers.ssrn.com/sol3/cf_dev/AbsByAuth.cfm?per_id=5958022)
- Google Scholar: [Profile](https://scholar.google.co.uk/citations?hl=en&user=84qbofEAAAAJ)
