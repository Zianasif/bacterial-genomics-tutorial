# Code Modernization Guide

This document outlines the modernization improvements made to the bacterial-genomics-tutorial repository.

## Overview

The codebase has been modernized to meet current software engineering best practices, including:
- Type hints and static type checking
- Comprehensive error handling
- Structured logging
- Command-line argument parsing
- Unit testing framework
- Updated dependencies with pinned versions
- Improved shell script robustness

## Table of Contents

1. [Python Scripts](#python-scripts)
2. [Shell Scripts](#shell-scripts)
3. [Dependencies](#dependencies)
4. [Testing](#testing)
5. [Migration Guide](#migration-guide)

---

## Python Scripts

### Modernization Features

All modernized Python scripts include:

#### 1. **Type Hints**
```python
def count_features(record: SeqRecord, feature_types: List[str]) -> Dict[str, int]:
    """Count occurrences of specified feature types."""
```
- Improves code readability and IDE support
- Enables static type checking with `mypy`
- Better documentation of function contracts

#### 2. **Logging System**
```python
import logging
logger = logging.getLogger(__name__)
logger.info("Starting annotation statistics extraction")
logger.debug("Found 5 CDS features")
```
- Replaces scattered `print()` statements
- Multiple log levels: DEBUG, INFO, WARNING, ERROR
- Easily configurable output
- Better debugging capability

#### 3. **Argument Parsing**
```python
parser = argparse.ArgumentParser(description='Extract annotation statistics')
parser.add_argument('directory', type=str, help='Directory with annotations')
parser.add_argument('-v', '--verbose', action='store_true', help='Enable debug output')
```
- Professional command-line interface
- Built-in help messages (`-h`)
- Type validation for arguments
- Better error messages

#### 4. **Error Handling**
```python
try:
    record = load_genbank_file(gbk_file)
except FileNotFoundError as e:
    logger.error(f"File error: {e}")
    return 1
```
- Graceful error handling with meaningful messages
- Proper exit codes for scripting
- Specific exception handling

### Modernized Scripts

#### `get_annot_stats_modernized.py`

**Features:**
- Type hints for all functions
- Comprehensive logging
- Full argument parsing with help
- Better file handling with `pathlib`
- Modular functions for easy testing

**Usage:**
```bash
# Basic usage
python get_annot_stats_modernized.py annotation_dir P7741

# With verbose output
python get_annot_stats_modernized.py -v annotation_dir P7741

# Save output to file
python get_annot_stats_modernized.py -o stats.txt annotation_dir P7741

# Get help
python get_annot_stats_modernized.py -h
```

**Key Improvements:**
- Proper file existence checking
- Clear error messages
- Structured output
- Logging for debugging
- Optional output file saving

#### `gene_count_summary_modernized.py`

**Features:**
- Type hints throughout
- Comprehensive input validation
- Better error messages for missing columns/isolates
- Structured logging
- Customizable output title and filename
- Statistics printing before visualization

**Usage:**
```bash
# Basic usage
python gene_count_summary_modernized.py P7741 Agy99 Liflandii pangenome/gene_presence_absence.csv

# Custom output
python gene_count_summary_modernized.py \
    -o custom_venn.png \
    --title "My Comparison" \
    P7741 Agy99 Liflandii data.csv

# Verbose debugging
python gene_count_summary_modernized.py -v P7741 Agy99 Liflandii data.csv
```

**Key Improvements:**
- Clear error messages if isolates not found
- Input file validation before processing
- Summary statistics printed to console
- Configurable output filename and title
- Better error handling for CSV parsing

---

## Shell Scripts

### Modernization Features

All modernized shell scripts include:

#### 1. **Strict Mode**
```bash
set -euo pipefail
```
- Exit on errors (`-e`)
- Exit on undefined variables (`-u`)
- Exit on pipe failures (`-o pipefail`)
- Prevents silent failures

#### 2. **Logging Functions**
```bash
log_info()   # Green [INFO] messages
log_warn()   # Yellow [WARNING] messages
log_error()  # Red [ERROR] messages
```

#### 3. **Error Handling**
```bash
trap 'log_error "Script failed at line $LINENO"; exit 1' ERR
```
- Trap errors with line numbers
- Graceful error messages
- Proper exit codes

#### 4. **Input Validation**
```bash
check_file_exists() { ... }
check_directory_exists() { ... }
validate_inputs() { ... }
```

#### 5. **Argument Parsing**
```bash
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help) usage ;;
        -v|--verbose) VERBOSE=true ;;
        ...
    esac
done
```

#### 6. **Usage Documentation**
```bash
usage() {
    cat << EOF
Usage: $SCRIPT_NAME [OPTIONS]
...
```

### Modernized Scripts

#### `assemble_modernized.sh`

**Features:**
- Proper error handling and exit traps
- Input validation for required files
- Tool availability checks
- Structured logging with colors
- Configurable output directory and threads
- Output verification

**Usage:**
```bash
# Basic usage with defaults
./assemble_modernized.sh

# Custom output and threads
./assemble_modernized.sh -o results -t 8

# Verbose output
./assemble_modernized.sh -v

# Help
./assemble_modernized.sh -h
```

**Advantages Over Original:**
- Checks if input files exist before running
- Verifies tools are installed
- Better error messages
- Color-coded output
- Configurable number of threads
- Output directory creation and verification

---

## Dependencies

### Updates to `environment.yaml`

**Key Changes:**

1. **Python Version Pinned**
   ```yaml
   python=3.11  # Previously: python=3
   ```

2. **Package Versioning**
   ```yaml
   biopython>=1.81        # Previously: no version
   numpy>=1.24.0          # Previously: no version
   pandas>=2.0.0          # Previously: no version
   ```

3. **New Development Tools**
   ```yaml
   pytest>=7.4.0          # Unit testing
   black>=23.7.0          # Code formatting
   flake8>=6.0.0          # Linting
   mypy>=1.4.0            # Type checking
   pylint>=2.17.0         # Code analysis
   ```

4. **Tool Versions Specified**
   ```yaml
   fastqc>=0.12.1
   quast>=5.2.0
   spades>=3.15.5
   # ... all tools now have explicit versions
   ```

### Updated `pip-requirements.txt`

Now includes version specifications and development tools:
```
numpy>=1.24.0
pandas>=2.0.0
matplotlib>=3.7.0
pytest>=7.4.0
black>=23.7.0
flake8>=6.0.0
mypy>=1.4.0
```

**Benefits:**
- Reproducible environments
- Explicit dependencies
- No surprise version changes
- Better compatibility tracking

---

## Testing

### New Test Suite

Location: `tests/test_annotation_scripts.py`

**Test Classes:**
- `TestAnnotationDataGeneration` - Fixtures for test data
- `TestGetAnnotStatsModernized` - Tests for annotation stats
- `TestGeneCountSummaryModernized` - Tests for Venn diagrams
- `TestErrorHandling` - Error scenario testing
- `TestInputValidation` - Input validation tests

**Running Tests:**
```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=.

# Run specific test class
pytest tests/test_annotation_scripts.py::TestGetAnnotStatsModernized -v

# Run specific test
pytest tests/test_annotation_scripts.py::TestGetAnnotStatsModernized::test_feature_counting -v
```

**Test Coverage:**
- File loading and error handling
- Feature counting
- CSV parsing
- Input validation
- Error conditions

---

## Code Quality Tools

### Static Type Checking

```bash
# Check for type errors
mypy get_annot_stats_modernized.py

# Check entire project
mypy .
```

### Code Formatting

```bash
# Format code with Black
black get_annot_stats_modernized.py

# Check formatting without changes
black --check get_annot_stats_modernized.py
```

### Linting

```bash
# Check with Flake8
flake8 get_annot_stats_modernized.py

# Check with Pylint
pylint get_annot_stats_modernized.py
```

---

## Migration Guide

### Updating Existing Scripts

To update your workflow with modernized scripts:

#### Step 1: Update Environment
```bash
# Remove old environment
conda env remove -n bacterial-genomics-tutorial

# Create new environment with updated dependencies
conda env create -f environment.yaml

# Activate environment
conda activate bacterial-genomics-tutorial
```

#### Step 2: Install Development Tools (Optional but Recommended)
```bash
pip install -r requirements-dev.txt
```

#### Step 3: Use New Scripts

**Old Workflow:**
```bash
python get_annot_stats.py annotation_dir P7741
```

**New Workflow:**
```bash
python get_annot_stats_modernized.py annotation_dir P7741
```

**With Advanced Features:**
```bash
# Verbose logging and output to file
python get_annot_stats_modernized.py -v -o stats.txt annotation_dir P7741
```

#### Step 4: Run Tests
```bash
pytest tests/
```

### Original vs. Modernized Comparison

| Feature | Original | Modernized |
|---------|----------|-----------|
| Type Hints | ❌ | ✅ |
| Logging | `print()` | Structured logging |
| Argument Parsing | sys.argv | argparse |
| Error Handling | Basic | Comprehensive |
| File Handling | String paths | pathlib |
| Help Messages | ❌ | ✅ |
| Unit Tests | ❌ | ✅ |
| Exit Codes | Inconsistent | Proper codes |
| Documentation | Minimal | Comprehensive |

---

## Best Practices Applied

### Python Best Practices
- ✅ PEP 8 compliance
- ✅ Type hints (PEP 484)
- ✅ Docstrings for all functions
- ✅ Proper exception handling
- ✅ Logging instead of print()
- ✅ Pathlib for file operations
- ✅ Argparse for CLI

### Shell Script Best Practices
- ✅ Proper error handling
- ✅ Input validation
- ✅ Clear logging/output
- ✅ Tool availability checking
- ✅ Meaningful exit codes
- ✅ Usage documentation
- ✅ Variable quoting

### General Software Engineering
- ✅ DRY (Don't Repeat Yourself)
- ✅ SOLID principles
- ✅ Comprehensive testing
- ✅ Version pinning
- ✅ Documentation
- ✅ Error messages
- ✅ Backwards compatibility

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'pytest'"
```bash
pip install pytest pytest-cov
# or
conda install pytest pytest-cov
```

### "Type checking failed with mypy"
```bash
# Check specific file
mypy --show-error-codes script.py

# See full error details
mypy script.py --show-traceback
```

### Shell script errors

**"command not found"**
```bash
# Check if tools are installed
command -v spades.py  # should show path or nothing

# Activate conda environment
conda activate bacterial-genomics-tutorial
```

**"Permission denied"**
```bash
# Make script executable
chmod +x assemble_modernized.sh

# Run it
./assemble_modernized.sh
```

---

## Next Steps

1. ✅ **Test the modernized scripts** with your data
2. ✅ **Run the unit tests** to ensure compatibility
3. ✅ **Update your workflows** to use new scripts
4. ✅ **Review logging output** for better debugging
5. ✅ **Use code quality tools** for future development

## Contributing

When contributing to modernized scripts, please:
1. Add type hints to all functions
2. Use logging instead of print()
3. Add error handling for edge cases
4. Write unit tests for new functionality
5. Follow PEP 8 style guide
6. Document your changes

---

## References

- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Type Hints (PEP 484)](https://www.python.org/dev/peps/pep-0484/)
- [Python Logging Documentation](https://docs.python.org/3/library/logging.html)
- [Bash Best Practices](https://mywiki.wooledge.org/BashGuide)
- [Pytest Documentation](https://docs.pytest.org/)

