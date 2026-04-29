#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
    echo "Usage: organize_results.sh <run_dir>" >&2
    exit 1
fi

RUN_DIR="$1"
WORK_DIR="${RUN_DIR}/work"
OUT_DIR="${RUN_DIR}/outputs"

if [[ ! -d "$WORK_DIR" ]]; then
    echo "Work directory not found: ${WORK_DIR}" >&2
    exit 1
fi

copy_dir_contents() {
    local src="$1"
    local dest="$2"

    if [[ -d "$src" ]]; then
        mkdir -p "$dest"
        cp -R "$src"/. "$dest"/
    fi
}

copy_file() {
    local src="$1"
    local dest="$2"

    if [[ -f "$src" ]]; then
        mkdir -p "$(dirname "$dest")"
        cp "$src" "$dest"
    fi
}

mkdir -p "$OUT_DIR"

# QC outputs
copy_dir_contents "$WORK_DIR/QC_RAW_READS" "$OUT_DIR/qc/raw_reads"
copy_dir_contents "$WORK_DIR/QC_TRIMMED_READS" "$OUT_DIR/qc/trimmed_reads"

# Reads
copy_dir_contents "$WORK_DIR/trimmed_reads" "$OUT_DIR/reads/trimmed"

# Assembly
copy_dir_contents "$WORK_DIR/P7741_SPADES_OUT" "$OUT_DIR/assembly/spades"
copy_dir_contents "$WORK_DIR/QC_ASSEMBLY" "$OUT_DIR/assembly/qc"
copy_dir_contents "$WORK_DIR/polished_assembly" "$OUT_DIR/assembly/polish/polished_assembly"
copy_dir_contents "$WORK_DIR/polishing_process" "$OUT_DIR/assembly/polish/polishing_process"
copy_file "$WORK_DIR/P7741.polished.fasta" "$OUT_DIR/assembly/polish/P7741.polished.fasta"

# Reorder and typing
copy_dir_contents "$WORK_DIR/P7741_reordered" "$OUT_DIR/reorder/P7741_reordered"
copy_file "$WORK_DIR/P7741.reordered.fasta" "$OUT_DIR/reorder/P7741.reordered.fasta"
copy_file "$WORK_DIR/mlst.csv" "$OUT_DIR/typing/mlst.csv"

# AMR
copy_file "$WORK_DIR/amr.summary.tab" "$OUT_DIR/resistance/amr.summary.tab"

# Annotation
copy_dir_contents "$WORK_DIR/P7741_annotation" "$OUT_DIR/annotation"
copy_file "$WORK_DIR/P7741_annotation/annotation_stats.txt" "$OUT_DIR/summaries/annotation_stats.txt"

# Pangenome
copy_dir_contents "$WORK_DIR/gffs" "$OUT_DIR/pangenome/gffs"
copy_dir_contents "$WORK_DIR/pangenome" "$OUT_DIR/pangenome/roary"
copy_file "$WORK_DIR/pangenome/venn.png" "$OUT_DIR/summaries/venn.png"

echo "Organized outputs saved to: ${OUT_DIR}"
