#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
PROFILE="full"
RUN_ID="$(date +%Y%m%d_%H%M%S)"
RESULTS_ROOT="${SCRIPT_DIR}/results"
SKIP_DOWNLOAD=false
ORGANIZE_RESULTS=true

usage() {
    cat <<'EOF'
Usage: ./run_pipeline.sh [options]

Profiles:
    demo   Download + QC + trim + assemble
  small  demo + polish + reorder + typing + AMR + annotation
  full   small + pangenome + summary plots

Options:
  -p, --profile <name>     Profile to run (demo, small, full)
  --run-id <id>            Override timestamp for run folder
  --results-root <path>    Root directory for results (default: ./results)
    --skip-download          Skip sample data download step
    --no-organize            Do not build the standardized outputs tree
  -h, --help               Show this help message
EOF
}

log() {
    printf "[%s] %s\n" "$(date '+%Y-%m-%d %H:%M:%S')" "$*"
}

run_step() {
    local name="$1"
    shift
    local log_file="${LOG_DIR}/${name}.log"
    log "START ${name}"
    (cd "$WORK_DIR" && "$@") 2>&1 | tee "$log_file"
    log "DONE  ${name}"
}

link_or_copy() {
    local src="$1"
    local dest="$2"

    if [[ -e "$dest" ]]; then
        return
    fi

    if ln -s "$src" "$dest" 2>/dev/null; then
        return
    fi

    if [[ -d "$src" ]]; then
        cp -R "$src" "$dest"
    else
        cp "$src" "$dest"
    fi
}

prepare_workdir() {
    mkdir -p "$WORK_DIR"
    link_or_copy "$SCRIPT_DIR/genomes" "$WORK_DIR/genomes"

    for helper in extract_reordered.py roary_plots.py get_pseudo.pl; do
        if [[ -f "$SCRIPT_DIR/$helper" ]]; then
            link_or_copy "$SCRIPT_DIR/$helper" "$WORK_DIR/$helper"
        fi
    done

    if [[ "$SKIP_DOWNLOAD" == "true" ]]; then
        if [[ -d "$SCRIPT_DIR/data" ]]; then
            link_or_copy "$SCRIPT_DIR/data" "$WORK_DIR/data"
        fi
        if [[ -d "$SCRIPT_DIR/apps" ]]; then
            link_or_copy "$SCRIPT_DIR/apps" "$WORK_DIR/apps"
        fi
        if [[ -f "$SCRIPT_DIR/TruSeq3-PE.fa" ]]; then
            link_or_copy "$SCRIPT_DIR/TruSeq3-PE.fa" "$WORK_DIR/TruSeq3-PE.fa"
        fi
    fi
}

validate_inputs() {
    if [[ "$SKIP_DOWNLOAD" != "true" ]]; then
        return
    fi

    if [[ ! -f "$WORK_DIR/data/P7741_R1.fastq.gz" ]] || [[ ! -f "$WORK_DIR/data/P7741_R2.fastq.gz" ]]; then
        echo "Missing input reads in ${WORK_DIR}/data. Use --skip-download only if data exists." >&2
        exit 1
    fi

    if [[ ! -f "$WORK_DIR/TruSeq3-PE.fa" ]]; then
        echo "Missing TruSeq3-PE.fa in ${WORK_DIR}. Use --skip-download only if the file exists." >&2
        exit 1
    fi

    if [[ "$PROFILE" == "small" || "$PROFILE" == "full" ]]; then
        if [[ ! -f "$WORK_DIR/apps/pilon.jar" ]]; then
            echo "Missing apps/pilon.jar in ${WORK_DIR}." >&2
            exit 1
        fi
    fi
}

step_download() {
    if [[ "$SKIP_DOWNLOAD" == "true" ]]; then
        log "Skipping download step"
        return
    fi

    local need=false
    [[ -f "${WORK_DIR}/data/P7741_R1.fastq.gz" ]] || need=true
    [[ -f "${WORK_DIR}/data/P7741_R2.fastq.gz" ]] || need=true
    [[ -f "${WORK_DIR}/TruSeq3-PE.fa" ]] || need=true
    [[ -f "${WORK_DIR}/apps/pilon.jar" ]] || need=true

    if [[ "$need" == "true" ]]; then
        run_step "download_data" bash "$SCRIPT_DIR/download_data.sh"
    else
        log "Sample data already present"
    fi
}

step_qc_raw() { run_step "qc_raw_reads" bash "$SCRIPT_DIR/qc_raw_reads.sh"; }
step_trim() { run_step "trim_reads" bash "$SCRIPT_DIR/trim_reads.sh"; }
step_qc_trimmed() { run_step "qc_trimmed_reads" bash "$SCRIPT_DIR/qc_trimmed_reads.sh"; }
step_assemble() { run_step "assemble" bash "$SCRIPT_DIR/assemble.sh"; }
step_polish() { run_step "polish" bash "$SCRIPT_DIR/polish.sh"; }
step_qc_assembly() { run_step "qc_assembly" bash "$SCRIPT_DIR/qc_assembly.sh"; }
step_reorder() { run_step "reorder_contigs" bash "$SCRIPT_DIR/reorder_contigs.sh"; }
step_mlst() { run_step "mlst" bash "$SCRIPT_DIR/mlst.sh"; }
step_amr() { run_step "amr" bash "$SCRIPT_DIR/amr.sh"; }
step_annotate() { run_step "annotate" bash "$SCRIPT_DIR/annotate.sh"; }
step_annot_stats() {
    run_step "annot_stats" python "$SCRIPT_DIR/get_annot_stats_modernized.py" \
        -v "P7741_annotation" "P7741" \
        -o "P7741_annotation/annotation_stats.txt"
}
step_genome_gffs() { run_step "genome_gffs" bash "$SCRIPT_DIR/get_genome_gffs.sh"; }
step_pangenome() { run_step "pangenome" bash "$SCRIPT_DIR/get_pangenome.sh"; }
step_gene_summary() {
    run_step "gene_summary" python "$SCRIPT_DIR/gene_count_summary_modernized.py" \
        "P7741" "Agy99" "Liflandii" "pangenome/gene_presence_absence.csv" \
        -o "pangenome/venn.png" \
        --title "P7741 vs Agy99 vs Liflandii"
}
step_dendogram() { run_step "dendogram" bash "$SCRIPT_DIR/dendogram.sh"; }

parse_args() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -p|--profile)
                PROFILE="$2"
                shift 2
                ;;
            --run-id)
                RUN_ID="$2"
                shift 2
                ;;
            --results-root)
                RESULTS_ROOT="$2"
                shift 2
                ;;
            --skip-download)
                SKIP_DOWNLOAD=true
                shift
                ;;
            --no-organize)
                ORGANIZE_RESULTS=false
                shift
                ;;
            -h|--help)
                usage
                exit 0
                ;;
            *)
                echo "Unknown option: $1" >&2
                usage
                exit 1
                ;;
        esac
    done
}

run_profile() {
    case "$PROFILE" in
        demo)
            steps=(download qc_raw trim qc_trimmed assemble)
            ;;
        small)
            steps=(download qc_raw trim qc_trimmed assemble polish qc_assembly reorder mlst amr annotate annot_stats)
            ;;
        full)
            steps=(download qc_raw trim qc_trimmed assemble polish qc_assembly reorder mlst amr annotate annot_stats genome_gffs pangenome gene_summary dendogram)
            ;;
        *)
            echo "Unknown profile: $PROFILE" >&2
            usage
            exit 1
            ;;
    esac

    for step in "${steps[@]}"; do
        "step_${step}"
    done
}

parse_args "$@"

RUN_DIR="${RESULTS_ROOT}/run_${RUN_ID}"
WORK_DIR="${RUN_DIR}/work"
LOG_DIR="${RUN_DIR}/logs"

if [[ -e "$RUN_DIR" ]]; then
    echo "Run directory already exists: ${RUN_DIR}. Choose a new --run-id." >&2
    exit 1
fi

mkdir -p "$LOG_DIR"

GIT_COMMIT=$(git -C "$SCRIPT_DIR" rev-parse HEAD 2>/dev/null || echo "unknown")
START_TIME_UTC=$(date -u '+%Y-%m-%dT%H:%M:%SZ')

cat > "${RUN_DIR}/run_info.txt" <<EOF
profile=${PROFILE}
run_id=${RUN_ID}
started=$(date '+%Y-%m-%d %H:%M:%S')
EOF

log "Profile: ${PROFILE}"
log "Run directory: ${RUN_DIR}"

prepare_workdir
validate_inputs

run_profile

END_TIME_UTC=$(date -u '+%Y-%m-%dT%H:%M:%SZ')

cat > "${RUN_DIR}/run_manifest.json" <<EOF
{
    "run_id": "${RUN_ID}",
    "profile": "${PROFILE}",
    "started_utc": "${START_TIME_UTC}",
    "ended_utc": "${END_TIME_UTC}",
    "repo_root": "${SCRIPT_DIR}",
    "work_dir": "${WORK_DIR}",
    "outputs_dir": "${RUN_DIR}/outputs",
    "logs_dir": "${LOG_DIR}",
    "git_commit": "${GIT_COMMIT}"
}
EOF

if [[ "$ORGANIZE_RESULTS" == "true" ]]; then
    run_step "organize_results" bash "$SCRIPT_DIR/organize_results.sh" "$RUN_DIR"
fi

log "Pipeline complete"
