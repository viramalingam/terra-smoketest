"""Summarize a BED / narrowPeak file (plain or gzipped): peak count, width stats, peaks per chromosome.

Writes <out-dir>/n_peaks.txt and <out-dir>/mean_width.txt (scalars read by the WDL) and a
two-column (metric, value) TSV with the full summary.
"""
import argparse
import collections
import gzip
import os
import statistics


def open_any(path):
    with open(path, "rb") as f:
        magic = f.read(2)
    return gzip.open(path, "rt") if magic == b"\x1f\x8b" else open(path)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--experiment", required=True)
    ap.add_argument("--bed", required=True)
    ap.add_argument("--out-tsv", required=True)
    ap.add_argument("--out-dir", default=".")
    a = ap.parse_args()

    widths, per_chrom = [], collections.Counter()
    with open_any(a.bed) as f:
        for line in f:
            if not line.strip() or line.startswith(("#", "track", "browser")):
                continue
            chrom, start, end = line.split("\t")[:3]
            widths.append(int(end) - int(start))
            per_chrom[chrom] += 1
    if not widths:
        raise SystemExit("no intervals in %s" % a.bed)

    mean_width = statistics.mean(widths)
    rows = [("experiment", a.experiment), ("source", os.path.basename(a.bed)),
            ("n_peaks", len(widths)), ("mean_width", "%.3f" % mean_width),
            ("median_width", statistics.median(widths)), ("min_width", min(widths)),
            ("max_width", max(widths))]
    rows += [("n_peaks_" + c, n) for c, n in sorted(per_chrom.items())]
    with open(a.out_tsv, "w") as f:
        f.write("metric\tvalue\n")
        f.writelines("%s\t%s\n" % r for r in rows)
    with open(os.path.join(a.out_dir, "n_peaks.txt"), "w") as f:
        f.write("%d\n" % len(widths))
    with open(os.path.join(a.out_dir, "mean_width.txt"), "w") as f:
        f.write("%.3f\n" % mean_width)
    print("%s: %d peaks, mean width %.1f" % (a.experiment, len(widths), mean_width))


if __name__ == "__main__":
    main()
