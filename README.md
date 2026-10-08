# terra-smoketest

Minimal WDL workflow for testing the full Terra/AnVIL path used by [tf-atlas-pipeline](https://github.com/viramalingam/tf-atlas-pipeline): GitHub tag -> Dockstore (GitHub App, `.dockstore.yml`) -> Terra method config -> data-table input -> Cromwell job -> outputs written back to the table. The task runs `python:3.12-bookworm`, shallow-clones this repo at a pinned tag and runs `scripts/bed_summary.py` on one BED/narrowPeak file (peak count, mean/median width, peaks per chromosome). Created 2026-10-08 by Claude Code for vir (nb project `anvil-terra`).

Dockstore entry: `github.com/viramalingam/terra-smoketest/bed_summary`; one version per branch/tag.

To release a new version:
1. Set the `code_ref` default in `wdl/bed_summary.wdl` to the new tag.
2. Commit, then `git tag vX.Y.Z && git push origin main vX.Y.Z`.
3. Point the Terra method config's `methodVersion` at `vX.Y.Z`.

## Contents

| name | size | modified | notes |
|---|---:|---|---|
| scripts/ | 2.0K | 2026-10-08 | bed_summary.py: BED/narrowPeak summary (n_peaks, widths, per-chrom counts) |
| wdl/ | 1.3K | 2026-10-08 | bed_summary.wdl: workflow bed_summary -> task summarize_bed |

## Log

- 2026-10-08T02:00:09Z: created — WDL bed_summary (python:3.12-bookworm, clones this repo at code_ref) + scripts/bed_summary.py; miniwdl check clean; local test on ENCSR000AHD/ENCSR000BKF peaks_inliers matches zcat|wc -l
- 2026-10-08T02:17:42Z: registered + tested — .dockstore.yml added (GitHub App, publish: true), tag v0.1.0; Dockstore published main and v0.1.0 in 42 s; Terra smoke test in terra-billing-vir/tf-atlas-dev PASS (2/2 workflows, outputs written back)
