#!/usr/bin/env python3
"""
Gene Count Summary and Venn Diagram Generator

This module generates Venn diagrams showing gene presence/absence patterns
across multiple bacterial genomes using pangenome analysis data.
"""

import sys
import logging
import argparse
from pathlib import Path
from typing import Dict, List
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib_venn import venn3, venn3_circles, venn3_unweighted

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments.
    
    Returns:
        argparse.Namespace: Parsed command-line arguments
    """
    parser = argparse.ArgumentParser(
        description='Generate Venn diagram from gene presence/absence data',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python gene_count_summary_modernized.py P7741 Agy99 Liflandii pangenome/gene_presence_absence.csv
  python gene_count_summary_modernized.py -o custom_output.png P7741 Agy99 Liflandii data.csv
        '''
    )
    parser.add_argument(
        'isolates',
        nargs=3,
        help='Names of three isolates to compare'
    )
    parser.add_argument(
        'csv_file',
        type=str,
        help='Path to gene presence/absence CSV file from Roary'
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='gene_count_summary.png',
        help='Output filename for Venn diagram (default: gene_count_summary.png)'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output (DEBUG level logging)'
    )
    parser.add_argument(
        '--title',
        type=str,
        default='Gene Count',
        help='Title for the Venn diagram'
    )
    
    return parser.parse_args()


def validate_input_file(filepath: str) -> Path:
    """Validate that the input file exists and is readable.
    
    Args:
        filepath: Path to input CSV file
        
    Returns:
        Path object if valid
        
    Raises:
        FileNotFoundError: If file doesn't exist
    """
    file_path = Path(filepath)
    if not file_path.exists():
        raise FileNotFoundError(f"CSV file not found: {filepath}")
    if not file_path.is_file():
        raise ValueError(f"Path is not a file: {filepath}")
    logger.info(f"Input file validated: {filepath}")
    return file_path


def load_gene_data(csv_file: Path) -> pd.DataFrame:
    """Load gene presence/absence data from CSV.
    
    Args:
        csv_file: Path to gene presence/absence CSV file
        
    Returns:
        DataFrame with gene data
        
    Raises:
        ValueError: If required columns are missing
    """
    try:
        df = pd.read_csv(csv_file)
        logger.info(f"Loaded data from {csv_file}: {df.shape[0]} genes")
        
        if 'Gene' not in df.columns:
            raise ValueError("'Gene' column not found in CSV file")
        
        logger.debug(f"Columns in CSV: {list(df.columns)}")
        return df
    except pd.errors.ParserError as e:
        logger.error(f"Failed to parse CSV file: {e}")
        raise ValueError(f"Failed to parse CSV file: {e}") from e
    except Exception as e:
        logger.error(f"Unexpected error loading CSV: {e}")
        raise


def validate_isolates(df: pd.DataFrame, isolates: List[str]) -> None:
    """Validate that all specified isolates exist in the dataframe.
    
    Args:
        df: Gene presence/absence DataFrame
        isolates: List of isolate names
        
    Raises:
        ValueError: If any isolate is not found in the data
    """
    missing = [iso for iso in isolates if iso not in df.columns]
    if missing:
        available = [col for col in df.columns if col not in ['Gene', 'No. isolates']]
        raise ValueError(
            f"Isolates not found in CSV: {missing}\n"
            f"Available isolates: {available}"
        )
    logger.info(f"Validated isolates: {isolates}")


def calculate_venn_values(
    df: pd.DataFrame,
    isolates: List[str]
) -> tuple[Dict[str, int], Dict[str, str]]:
    """Calculate values for Venn diagram based on gene presence/absence.
    
    Args:
        df: Gene presence/absence DataFrame
        isolates: List of three isolate names
        
    Returns:
        Tuple of (subset_counts, group_labels)
    """
    if len(isolates) != 3:
        raise ValueError("Exactly 3 isolates are required")
    
    # Create mapping for isolates
    group = {'A': isolates[0], 'B': isolates[1], 'C': isolates[2]}
    subset = {}
    
    # Genes common to all three isolates
    all_isolates = df[df['No. isolates'] == 3][isolates]
    all_isolates = all_isolates.dropna()
    subset['ABC'] = all_isolates.shape[0]
    logger.debug(f"Genes in all three isolates: {subset['ABC']}")
    
    # Genes unique to each isolate
    for key, isolate in group.items():
        unique = df[(df['No. isolates'] == 1) & (df[isolate].notnull())]
        subset[key] = unique.shape[0]
        logger.debug(f"Unique genes in {isolate}: {subset[key]}")
    
    # Genes common to pairs of isolates
    subgroup_pairs = [('A', 'B'), ('A', 'C'), ('B', 'C')]
    for pair in subgroup_pairs:
        subgroup_key = ''.join(pair)
        member1 = group[pair[0]]
        member2 = group[pair[1]]
        
        common = df[(df['No. isolates'] == 2)][[member1, member2]]
        common = common.dropna()
        subset[subgroup_key] = common.shape[0]
        logger.debug(f"Common genes in {member1}-{member2}: {subset[subgroup_key]}")
    
    return subset, group


def draw_venn_diagram(
    subset: Dict[str, int],
    group: Dict[str, str],
    output_file: str,
    title: str
) -> None:
    """Draw and save Venn diagram.
    
    Args:
        subset: Dictionary of subset counts
        group: Dictionary of group labels
        output_file: Output filename
        title: Title for the diagram
        
    Raises:
        IOError: If unable to save figure
    """
    try:
        # Prepare values in required order: A, B, AB, C, AC, BC, ABC
        venn_values = [
            subset['A'],
            subset['B'],
            subset['AB'],
            subset['C'],
            subset['AC'],
            subset['BC'],
            subset['ABC']
        ]
        
        # Create figure
        plt.figure(figsize=(10, 8))
        venn3_unweighted(
            subsets=venn_values,
            set_labels=(group['A'], group['B'], group['C']),
            alpha=0.7
        )
        plt.title(title, fontsize=14, fontweight='bold')
        
        # Save figure
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        logger.info(f"Venn diagram saved to {output_file}")
        print(f"Venn diagram saved to {output_file}")
        
    except Exception as e:
        logger.error(f"Failed to save Venn diagram: {e}")
        raise IOError(f"Failed to save figure to {output_file}: {e}") from e
    finally:
        plt.close()


def print_statistics(subset: Dict[str, int], group: Dict[str, str]) -> None:
    """Print summary statistics.
    
    Args:
        subset: Dictionary of subset counts
        group: Dictionary of group labels
    """
    print("\nGene Count Summary:")
    print("=" * 50)
    print(f"Genes unique to {group['A']}: {subset['A']}")
    print(f"Genes unique to {group['B']}: {subset['B']}")
    print(f"Genes unique to {group['C']}: {subset['C']}")
    print(f"Genes shared by {group['A']}-{group['B']}: {subset['AB']}")
    print(f"Genes shared by {group['A']}-{group['C']}: {subset['AC']}")
    print(f"Genes shared by {group['B']}-{group['C']}: {subset['BC']}")
    print(f"Genes common to all three: {subset['ABC']}")
    print("=" * 50)


def main() -> int:
    """Main entry point."""
    try:
        args = parse_arguments()
        
        # Configure logging
        if args.verbose:
            logger.setLevel(logging.DEBUG)
        
        logger.info("Starting gene count summary generation")
        
        # Validate input file
        csv_file = validate_input_file(args.csv_file)
        
        # Load data
        df = load_gene_data(csv_file)
        
        # Validate isolates
        validate_isolates(df, args.isolates)
        
        # Calculate Venn diagram values
        subset, group = calculate_venn_values(df, args.isolates)
        
        # Print statistics
        print_statistics(subset, group)
        
        # Draw and save Venn diagram
        draw_venn_diagram(subset, group, args.output, args.title)
        
        logger.info("Gene count summary generation completed successfully")
        return 0
        
    except (FileNotFoundError, ValueError) as e:
        logger.error(f"Input error: {e}")
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
