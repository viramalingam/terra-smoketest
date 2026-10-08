version 1.0

# Smoke test for the Terra/AnVIL path used by tf-atlas-pipeline:
# docker image -> shallow clone of this repo at a pinned tag -> run a script -> outputs written back to the data table.

workflow bed_summary {
	input {
		String experiment
		File peaks
		# tag of this repo whose scripts/ are run; bump it together with the release tag
		String code_ref = "v0.1.0"
	}

	call summarize_bed {
		input:
			experiment = experiment,
			peaks = peaks,
			code_ref = code_ref
	}

	output {
		Int n_peaks = summarize_bed.n_peaks
		Float mean_width = summarize_bed.mean_width
		File summary_tsv = summarize_bed.summary_tsv
	}
}

task summarize_bed {
	input {
		String experiment
		File peaks
		String code_ref
		Int mem_gb = 2
	}

	command <<<
		set -euo pipefail
		git clone --depth 1 --branch ~{code_ref} https://github.com/viramalingam/terra-smoketest.git /tmp/terra-smoketest
		python3 /tmp/terra-smoketest/scripts/bed_summary.py \
			--experiment ~{experiment} \
			--bed ~{peaks} \
			--out-tsv ~{experiment}_bed_summary.tsv \
			--out-dir .
	>>>

	output {
		Int n_peaks = read_int("n_peaks.txt")
		Float mean_width = read_float("mean_width.txt")
		File summary_tsv = "~{experiment}_bed_summary.tsv"
	}

	runtime {
		docker: "python:3.12-bookworm"
		memory: "~{mem_gb} GB"
		cpu: 1
		disks: "local-disk 10 HDD"
		preemptible: 1
		maxRetries: 0
	}
}
