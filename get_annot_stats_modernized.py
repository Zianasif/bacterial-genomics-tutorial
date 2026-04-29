#!/usr/bin/env python3
"""
Annotation Statistics Extractor

This module extracts and summarizes annotation statistics from GenBank files,
including feature counts, insertion sequences, and pseudogenes.
"""

import sys
import logging
import argparse
from pathlib import Path
from typing import Dict, List, Tuple
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

DEFAULT_FEATURES = ['CDS', 'gene', 'tRNA', 'tmRNA', 'rRNA']


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments.
    
    Returns:
        argparse.Namespace: Parsed command-line arguments
    """
    parser = argparse.ArgumentParser(
        description='Extract annotation statistics from GenBank files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python get_annot_stats_modernized.py annotation_dir genome_prefix
  python get_annot_stats_modernized.py -v annotation_dir genome_prefix
        '''
    )
    parser.add_argument(
        'directory',
        type=str,
        help='Directory containing GenBank annotation files'
    )
    parser.add_argument(
        'prefix',
        type=str,
        help='Prefix of the annotation files (e.g., P7741)'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output (DEBUG level logging)'
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        default=None,
        help='Output file for statistics (default: stdout)'
    )
    
    return parser.parse_args()


def load_genbank_file(filepath: Path) -> SeqRecord:
    """Load a GenBank file and return the first sequence record.
    
    Args:
        filepath: Path to GenBank file
        
    Returns:
        SeqRecord: First sequence from GenBank file
        
    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If no records found in file
    """
    if not filepath.exists():
        raise FileNotFoundError(f"GenBank file not found: {filepath}")
    
    try:
        records = list(SeqIO.parse(filepath, "gb"))
        if not records:
            raise ValueError(f"No records found in {filepath}")
        logger.debug(f"Loaded GenBank file with {len(records)} record(s)")
        return records[0]
    except Exception as e:
        logger.error(f"Failed to parse GenBank file {filepath}: {e}")
        raise


def count_features(record: SeqRecord, feature_types: List[str]) -> Dict[str, int]:
    """Count occurrences of specified feature types in a sequence record.
    
    Args:
        record: SeqRecord to analyze
        feature_types: List of feature types to count
        
    Returns:
        Dictionary mapping feature types to their counts
    """
    counts = {}
    for feature_type in feature_types:
        count = len([f for f in record.features if f.type == feature_type])
        counts[feature_type] = count
        logger.debug(f"Found {count} {feature_type} features")
    return counts


def extract_insertion_sequences(record: SeqRecord) -> Tuple[List[str], Dict[str, int]]:
    """Extract insertion sequences from CDS features.
    
    Args:
        record: SeqRecord to analyze
        
    Returns:
        Tuple of (list of IS names, count of IS types)
    """
    cds_features = [f for f in record.features if f.type == 'CDS']
    
    insertion_sequences = []
    for cds in cds_features:
        if 'product' in cds.qualifiers:
            product = cds.qualifiers['product'][0]
            if product.startswith('IS'):
                insertion_sequences.append(product)
    
    # Count unique IS types
    is_counts = {}
    if insertion_sequences:
        for is_name in set(insertion_sequences):
            is_counts[is_name] = insertion_sequences.count(is_name)
        logger.debug(f"Found {len(insertion_sequences)} insertion sequences "
                    f"of {len(is_counts)} unique types")
    
    return insertion_sequences, is_counts


def count_pseudogenes(pseudo_file: Path) -> int:
    """Count pseudogenes from pseudogene file.
    
    Args:
        pseudo_file: Path to pseudogene file
        
    Returns:
        Number of pseudogenes
        
    Raises:
        FileNotFoundError: If pseudogene file not found
    """
    if not pseudo_file.exists():
        logger.warning(f"Pseudogene file not found: {pseudo_file}")
        return 0
    
    try:
        with open(pseudo_file, 'r') as f:
            count = len([line for line in f if line.strip()])
        logger.debug(f"Found {count} pseudogenes")
        return count
    except Exception as e:
        logger.error(f"Failed to read pseudogene file {pseudo_file}: {e}")
        return 0


def get_stats(directory: str, prefix: str) -> Dict[str, int]:
    """Extract annotation statistics from GenBank file.
    
    Args:
        directory: Directory containing annotation files
        prefix: Prefix of annotation files
        
    Returns:
        Dictionary of feature counts
        
    Raises:
        FileNotFoundError: If required files not found
    """
    dir_path = Path(directory)
    if not dir_path.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")
    
    logger.info(f"Processing annotation files in {directory}")
    
    # Load GenBank file
    gbk_file = dir_path / f"{prefix}.gbk"
    record = load_genbank_file(gbk_file)
    logger.info(f"Loaded GenBank file: {gbk_file}")
    
    # Count standard features
    stats = count_features(record, DEFAULT_FEATURES)
    
    # Extract insertion sequences
    insertion_sequences, is_counts = extract_insertion_sequences(record)
    stats['Total_Insertion_Sequences'] = len(insertion_sequences)
    stats.update(is_counts)
    
    # Count pseudogenes
    pseudo_file = dir_path / f"{prefix}.pseudo.txt"
    stats['Pseudogenes'] = count_pseudogenes(pseudo_file)
    
    return stats


def format_output(stats: Dict[str, int]) -> str:
    """Format statistics for display.
    
    Args:
        stats: Dictionary of statistics
        
    Returns:
        Formatted string representation
    """
    output = []
    output.append("Counting Annotated Features" + "." * 25)
    
    # Sort keys for consistent output
    for key in sorted(stats.keys()):
        output.append(f"{key}: {stats[key]}")
    
    return "\n".join(output)


def main() -> int:
    """Main entry point."""
    try:
        args = parse_arguments()
        
        # Configure logging level
        if args.verbose:
            logger.setLevel(logging.DEBUG)
        
        logger.info("Starting annotation statistics extraction")
        
        # Extract statistics
        stats = get_stats(args.directory, args.prefix)
        
        # Format and output results
        output = format_output(stats)
        
        if args.output:
            output_file = Path(args.output)
            output_file.write_text(output + "\n")
            logger.info(f"Statistics written to {args.output}")
            print(f"Statistics written to {args.output}")
        else:
            print(output)
        
        logger.info("Annotation statistics extraction completed successfully")
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
