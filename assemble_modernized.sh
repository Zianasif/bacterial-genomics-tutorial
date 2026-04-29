#!/bin/bash
#
# Modernized Shell Script Template with Error Handling
# This script provides best practices for bacterial genomics pipeline scripts
#

set -euo pipefail  # Exit on error, undefined vars, and pipe failures

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_NAME="$(basename "$0")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $*" >&2
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $*" >&2
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $*" >&2
}

# Error handling
error_exit() {
    log_error "$1"
    exit "${2:-1}"
}

# Trap errors
trap 'log_error "Script failed at line $LINENO"; exit 1' ERR

# Help message
usage() {
    cat << EOF
Usage: $SCRIPT_NAME [OPTIONS]

OPTIONS:
    -h, --help          Show this help message
    -v, --verbose       Enable verbose output
    -o, --output DIR    Output directory (default: output)
    -t, --threads N     Number of threads (default: 4)

EXAMPLES:
    $SCRIPT_NAME -o results -t 8
    $SCRIPT_NAME --verbose --output my_output

EOF
    exit 0
}

# Parse arguments
VERBOSE=false
OUTPUT_DIR="output"
THREADS=4

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            usage
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -o|--output)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        -t|--threads)
            THREADS="$2"
            shift 2
            ;;
        *)
            error_exit "Unknown option: $1"
            ;;
    esac
done

# Validate inputs
validate_inputs() {
    # Check if required tools are installed
    local required_tools=("spades.py" "samtools" "bwa")
    
    for tool in "${required_tools[@]}"; do
        if ! command -v "$tool" &> /dev/null; then
            error_exit "Required tool not found: $tool"
        fi
    done
    
    log_info "All required tools found"
}

# Check if directory exists
check_directory_exists() {
    local dir="$1"
    local name="$2"
    
    if [[ ! -d "$dir" ]]; then
        error_exit "$name directory not found: $dir"
    fi
    log_info "$name directory found: $dir"
}

# Check if file exists
check_file_exists() {
    local file="$1"
    local name="$2"
    
    if [[ ! -f "$file" ]]; then
        error_exit "$name file not found: $file"
    fi
    log_info "$name file found: $file"
}

# Main function
main() {
    log_info "Starting analysis pipeline"
    log_info "Output directory: $OUTPUT_DIR"
    log_info "Number of threads: $THREADS"
    [[ "$VERBOSE" == "true" ]] && log_info "Verbose mode enabled"
    
    # Create output directory
    mkdir -p "$OUTPUT_DIR" || error_exit "Failed to create output directory: $OUTPUT_DIR"
    log_info "Created output directory: $OUTPUT_DIR"
    
    # Validate inputs
    validate_inputs
    
    # Check for required directories/files
    check_directory_exists "trimmed_reads" "Trimmed reads"
    check_file_exists "trimmed_reads/P7741_R1.fastq.gz" "Paired-end read 1"
    check_file_exists "trimmed_reads/P7741_R2.fastq.gz" "Paired-end read 2"
    
    # Run SPAdes assembly
    log_info "Starting SPAdes assembly..."
    if spades.py \
        --careful \
        -o "$OUTPUT_DIR/P7741_SPADES_OUT" \
        -1 "trimmed_reads/P7741_R1.fastq.gz" \
        -2 "trimmed_reads/P7741_R2.fastq.gz" \
        -t "$THREADS"; then
        log_info "SPAdes assembly completed successfully"
    else
        error_exit "SPAdes assembly failed with exit code $?"
    fi
    
    # Verify output
    if [[ ! -f "$OUTPUT_DIR/P7741_SPADES_OUT/contigs.fasta" ]]; then
        error_exit "SPAdes output file not found: $OUTPUT_DIR/P7741_SPADES_OUT/contigs.fasta"
    fi
    log_info "SPAdes output verified"
    
    log_info "Pipeline completed successfully!"
}

# Run main function
main "$@"
