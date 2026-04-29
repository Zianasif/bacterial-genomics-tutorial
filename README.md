# 🧬 Bacterial Genomics Tutorial

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Contributions Welcome](https://img.shields.io/badge/Contributions-Welcome-brightgreen.svg)](CONTRIBUTING.md)

> **A comprehensive pipeline for comparative analysis of bacterial genomes** — designed to make bioinformatics accessible to researchers at all levels.

This repository provides automated shell scripts and Python tools to streamline bacterial genome assembly, annotation, and comparative analysis. Whether you're new to bioinformatics or an experienced researcher, these scripts will help you perform complex analyses without the hassle of manually wrangling individual tools.

**🎥 Learn More:**
- [YouTube Tutorials](https://www.youtube.com/playlist?list=PLe1-kjuYBZ074A06NOuO9rXCTD3ddoOyz)
- [Original Author Channel](https://www.youtube.com/channel/UCOJM9xzqDc6-43j2x_vXqCQ)
- [Support the Project](https://www.buymeacoffee.com/bioinfocoach)

---

## ✨ Features

### 🏗️ Complete Analysis Pipeline
- **Quality Control** - FastQC, QUAST for read and assembly quality assessment
- **Read Trimming** - Sickle and Trimmomatic for sequence quality filtering
- **Assembly** - SPAdes for de novo genome assembly
- **Assembly Polishing** - Pilon for draft genome improvement
- **Genome Annotation** - Prokka for automatic gene annotation
- **Comparative Analysis** - Roary for pangenome analysis, dREP for genome comparison
- **Typing & Resistance** - MLST for sequence typing, ABRicate for AMR gene detection
- **Visualization** - Dendograms, circular genomes, and Venn diagrams

### ✨ Modern Code Quality (NEW!)
- **Type Hints** - Full type annotations for better IDE support
- **Error Handling** - Comprehensive validation and meaningful error messages
- **Logging System** - Structured logging for easier debugging
- **CLI Interface** - Professional command-line argument parsing with help
- **Unit Tests** - Full test coverage with pytest
- **Code Quality Tools** - Black, Flake8, MyPy for code standards
- **Pinned Dependencies** - Reproducible environments with explicit versions

---

## 🚀 Quick Start

### Prerequisites
- Linux/macOS (or WSL on Windows)
- [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/) (Anaconda or Miniconda)
- ~20GB free disk space

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Zianasif/bacterial-genomics-tutorial.git
cd bacterial-genomics-tutorial

conda env create -f environment.yaml

# 3. Activate the environment
conda activate bacterial-genomics-tutorial

# 4. Download pilon (optional but recommended)
# 5. Make scripts executable
chmod +x *.{py,sh,pl}
```

### First Run

```bash
# Download sample data
./download_data.sh

# Run quality control on raw reads
./qc_raw_reads.sh

# That's it! You're ready to go

```

---

## One-Command Pipeline (Profiles)

Use the end-to-end runner in [run_pipeline.sh](run_pipeline.sh) to execute the full workflow in a reproducible run folder. Each profile runs a defined set of steps.

**Profiles:**
- **demo** - Download + QC + trim + assemble
- **small** - demo + polish + reorder + typing + AMR + annotation
- **full** - small + pangenome + summary plots

```bash
# Full workflow in a timestamped run folder
./run_pipeline.sh --profile full

# Shorter run for quick validation
./run_pipeline.sh --profile demo

# Reuse existing data without downloading
./run_pipeline.sh --profile small --skip-download
```

The runner saves raw step outputs in a work folder and then builds a standardized output tree for browsing using [organize_results.sh](organize_results.sh).

---

## 📊 Analysis Pipeline

```
Raw Reads
    ↓
[QC] FastQC ──→ Quality Report
    ↓
[Trim] Sickle/Trimmomatic ──→ Clean Reads
    ↓
[QC] Trimmed Reads
    ↓
[Assemble] SPAdes ──→ Draft Contigs
    ↓
[Polish] Pilon ──→ Polished Genome
    ↓
[QC] QUAST ──→ Assembly Stats
    ↓
[Reorder] RagTag ──→ Reference-aligned
    ↓
[Type] MLST ──→ Sequence Type
    ↓
[Resistance] ABRicate ──→ AMR Genes
    ↓
[Annotate] Prokka ──→ Annotations
    ↓
[Compare] Roary ──→ Pangenome
    ↓
[Visualize] Dendograms, Venn Diagrams
```

---

## 📖 Usage Guide

### Step-by-Step Analysis

#### **Step 1: Quality Control (Raw Reads)**
```bash
./qc_raw_reads.sh
```
Generates FastQC reports for your sequencing reads.

#### **Step 2: Read Trimming**
```bash
./trim_reads.sh
```
Removes low-quality bases and adapters using Sickle.

#### **Step 3: Quality Control (Trimmed Reads)**
```bash
./qc_trimmed_reads.sh
```
Verifies trimming quality.

#### **Step 4: De Novo Assembly**
```bash
./assemble.sh
```
Assembles reads into contigs using SPAdes.

#### **Step 5: Assembly Polishing** (Optional)
```bash
./polish.sh
```
Improves assembly accuracy using Pilon.

#### **Step 6: Assembly Quality Assessment**
```bash
./qc_assembly.sh
```
Evaluates both raw and polished assemblies with QUAST.

#### **Step 7: Contig Reordering**
```bash
./reorder_contigs.sh
```
Aligns and orders contigs against a reference genome.

#### **Step 8: Sequence Typing**
```bash
./mlst.sh
```
Performs MLST analysis for strain identification.

#### **Step 9: Antimicrobial Resistance Screening**
```bash
./amr.sh
```
Identifies known AMR genes using ABRicate.

#### **Step 10: Genome Annotation**
```bash
./annotate.sh
```
Annotates genes and features using Prokka.

#### **Step 11: Annotation Statistics**
```bash
python get_annot_stats_modernized.py -v annotation_dir genome_prefix
```
Extracts gene counts and feature statistics.

#### **Step 12: Genome Dendogram** (Comparative)
```bash
./dendogram.sh
```
Creates phylogenetic trees with dREP.

#### **Step 13: Pangenome Analysis**
```bash
./get_genome_gffs.sh  # Generate GFF files
./get_pangenome.sh    # Run Roary
```
Analyzes shared and unique genes across genomes.

#### **Step 14: Gene Presence/Absence Visualization**
```bash
python gene_count_summary_modernized.py isolate1 isolate2 isolate3 gene_presence_absence.csv
```
Creates Venn diagrams showing gene overlap.

#### **Step 15: Circular Genome Comparison**
Use Proksee or CGView tools with generated GFF files.

---

## 🆕 Modernized Scripts

### Enhanced Python Scripts

All modernized scripts include improved features and full help documentation:

#### `get_annot_stats_modernized.py`
```bash
# Get help
python get_annot_stats_modernized.py -h

# Basic usage with logging
python get_annot_stats_modernized.py annotation_dir genome_prefix

# Verbose output with file save
python get_annot_stats_modernized.py -v -o stats.txt annotation_dir genome_prefix
```

**Features:**
- ✅ Type hints for IDE support
- ✅ Structured logging system
- ✅ Detailed error messages
- ✅ Output to file option
- ✅ Verbose debugging mode

#### `gene_count_summary_modernized.py`
```bash
# Get help
python gene_count_summary_modernized.py -h

# Generate Venn diagram
python gene_count_summary_modernized.py isolate1 isolate2 isolate3 gene_presence_absence.csv

# Custom output and title
python gene_count_summary_modernized.py \
    -o custom_venn.png \
    --title "My Bacterial Comparison" \
    isolate1 isolate2 isolate3 gene_presence_absence.csv
```

**Features:**
- ✅ Input validation with clear errors
- ✅ Statistics summary before visualization
- ✅ Customizable output filename and title
- ✅ Comprehensive error handling

### Enhanced Shell Scripts

#### `assemble_modernized.sh`
```bash
# Get help
./assemble_modernized.sh -h

# Run with custom options
./assemble_modernized.sh -o results -t 8 -v
```

**Features:**
- ✅ Input validation
- ✅ Colored logging output
- ✅ Error trapping with line numbers
- ✅ Configurable threads
- ✅ Output verification

---

## 🧪 Testing

Run the comprehensive test suite to verify installation:

```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=. --cov-report=html
```

---

## 🔍 Code Quality

Check code quality using modern tools:

```bash
# Type checking
mypy *.py

# Code formatting
black --check .

# Linting
flake8 .

# Run all checks
black . && flake8 . && mypy . && pytest tests/ -v
```

---

## 🗂️ Output Structure

Runs created with [run_pipeline.sh](run_pipeline.sh) keep raw step outputs in a dedicated work area, then generate a clean, standardized output tree for browsing and downstream analysis using [organize_results.sh](organize_results.sh).

---

## 📁 Project Structure

```
bacterial-genomics-tutorial/
├── *.sh                          # Pipeline scripts
├── *.py                          # Analysis scripts
├── *_modernized.py              # Enhanced versions with type hints
├── genomes/                      # Sample reference genomes
├── tests/                        # Unit test suite
│   ├── test_annotation_scripts.py
│   └── __init__.py
├── notebooks/                    # Walkthrough notebook
│   └── Walkthrough.ipynb
├── environment.yaml              # Conda dependencies (pinned versions)
├── pip-requirements.txt          # Python pip dependencies
├── requirements-dev.txt          # Development tools
├── run_pipeline.sh               # End-to-end runner with profiles
├── organize_results.sh           # Standardized output organizer
├── README.md                     # This file
├── MODERNIZATION_GUIDE.md        # Detailed modernization info
├── MODERNIZATION_SUMMARY.md      # Modernization overview
└── QUICK_REFERENCE.md            # Quick command reference
```

---

## 🛠️ Dependencies

All major bioinformatics tools are included in `environment.yaml`:

- **Assembly:** SPAdes, Minimap2, RagTag
- **QC:** FastQC, QUAST
- **Annotation:** Prokka
- **Comparison:** Roary, dREP, Mash, Mummer
- **Typing:** MLST
- **Resistance:** ABRicate
- **Utilities:** Samtools, BWA, Mafft, Sickle

Python packages:
- BioPython, Pandas, Matplotlib, NumPy
- Testing: pytest, pytest-cov
- Code Quality: black, flake8, mypy, pylint

---

## 📚 Documentation

- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Command cheat sheet
- **[MODERNIZATION_SUMMARY.md](MODERNIZATION_SUMMARY.md)** - Overview of code improvements
- **[MODERNIZATION_GUIDE.md](MODERNIZATION_GUIDE.md)** - Detailed modernization documentation
- **[notebooks/Walkthrough.ipynb](notebooks/Walkthrough.ipynb)** - Hands-on pipeline walkthrough

---

## 🐛 Troubleshooting

### Common Issues

**"Command not found"**
```bash
# Ensure environment is activated
conda activate bacterial-genomics-tutorial

# Make scripts executable
chmod +x *.{py,sh,pl}
```

**"No module named 'X'"**
```bash
# Reinstall environment
conda env remove -n bacterial-genomics-tutorial
conda env create -f environment.yaml
```

**"Permission denied"**
```bash
chmod +x script_name.sh
```

**Debugging with verbose output:**
```bash
# Use -v flag for modernized scripts
python script_modernized.py -v

# Use -v flag for modernized shell scripts
./script_modernized.sh -v
```

See [MODERNIZATION_GUIDE.md](MODERNIZATION_GUIDE.md#troubleshooting) for more help.

---

## 📊 Example Analysis

Perform a complete comparative analysis of 3 bacterial genomes:

```bash
# Activate environment
conda activate bacterial-genomics-tutorial

# 1. Download and prepare data
./download_data.sh

# 2. Quality control
./qc_raw_reads.sh
./trim_reads.sh
./qc_trimmed_reads.sh

# 3. Assembly
./assemble.sh
./polish.sh
./qc_assembly.sh

# 4. Typing and screening
./mlst.sh
./amr.sh

# 5. Annotation
./annotate.sh
python get_annot_stats_modernized.py -v annotation_dir genome_name

# 6. Comparative analysis
./get_genome_gffs.sh
./get_pangenome.sh
python gene_count_summary_modernized.py genome1 genome2 genome3 pangenome/gene_presence_absence.csv

# 7. Generate report (optional)
./zip_results.sh
```

---

## 🤝 Contributing

Contributions are welcome! Please ensure:

- ✅ Code includes type hints
- ✅ Functions have docstrings
- ✅ Tests are included
- ✅ Code follows PEP 8
- ✅ All tests pass (`pytest tests/ -v`)

---

## 📜 License

MIT License - See [LICENSE](LICENSE) for details.

---

## 🙏 Credits

**Original Creator:** Vincent Appiah  
**Original Repository:** [vappiah/bacterial-genomics-tutorial](https://github.com/vappiah/bacterial-genomics-tutorial)

**Modernization Contributions:**
- Type hints and logging system
- Comprehensive error handling
- Unit tests
- Code quality tools
- Enhanced documentation

---

## 📞 Support & Resources

- **YouTube Tutorials:** [Bacterial Genome Analysis Playlist](https://www.youtube.com/playlist?list=PLe1-kjuYBZ074A06NOuO9rXCTD3ddoOyz)
- **Support Original Author:** [Buy Me a Coffee](https://www.buymeacoffee.com/bioinfocoach)
- **Questions?** Check [MODERNIZATION_GUIDE.md](MODERNIZATION_GUIDE.md) or open an issue

---

## 🎯 Quick Links

| Resource | Link |
|----------|------|
| Quick Reference | [QUICK_REFERENCE.md](QUICK_REFERENCE.md) |
| Modernization Guide | [MODERNIZATION_GUIDE.md](MODERNIZATION_GUIDE.md) |
| Modernization Summary | [MODERNIZATION_SUMMARY.md](MODERNIZATION_SUMMARY.md) |
| Original Repository | [vappiah/bacterial-genomics-tutorial](https://github.com/vappiah/bacterial-genomics-tutorial) |
| YouTube Tutorials | [Playlist](https://www.youtube.com/playlist?list=PLe1-kjuYBZ074A06NOuO9rXCTD3ddoOyz) |

---

<div align="center">

**Made with ❤️ for the bioinformatics community**

⭐ If this project helped you, consider starring it on GitHub!

</div>
```
./reorder_contigs.sh
```
### Step 9: Perform a multi locus sequence typing using MLST software\
```
./mlst.sh
```
### Step 10: Check for antimicrobial resistance genes using abricate\
```
./amr.sh
```
### Step 11: Annotate the draft genome using prokka
```
./annotate.sh
```
### Step 12: Get some statistics on the annotation. 
Features such as genes, CDS will be counted and displayed. The scripts requires you to specify the folder where annotations were saved . i.e. P7741
Python should be used to run that script

``` python get_annot_stats.py P7741_annotation P7741``` 

### Step 13: Generate dendogram using dREP\
``` ./dendogram.sh ```

### Step 14: Perform Pangenome Analysis using Roary. 
Input files are gff (version 3 ) format. It is recommended to use prokka generated gff. So we generate the gffs for the files in the genome folder by reannotating with prokka. We use the get_genome_gffs script \
```./get_genome_gffs.sh ```

Then perform pangenome analysis\
``` 
./get_pangenome.sh
```

### Step 15: Get gene summary for three of the organism. the default is P7741 Agy99 and Liflandii. Feel free to change it. A venn diagram will be generated(gene_count_summary.png)

```python gene_count_summary.py P7741 Agy99 Liflandii pangenome/gene_presence_absence.csv```


If you are working on a cluster you will want to combine the analysis results into a zip file for download and view locally. 
```./zip_results.sh```


### Step 16: Compare your draft genome with the other organisms in the genomes folder by generating circular structures for them . Use the tutorial here to guide you https://youtu.be/pobQgE4z-5Q


### Step 17: Result interpretation
The result interpretation are available on my youtube video tutorial : https://youtu.be/S_sRo_85jhs

Now that you have been able to perform a bacterial comparative genome analysis. Its time to apply your skills on a real world data.
Good luck and see you next time

### Citation
Vincent Appiah, 2020.  Bacterial Genomics Tutorial  https://github.com/vappiah/bacterial-genomics-tutorial

or

Vincent Appiah,2020. Youtube https://youtu.be/S_sRo_85jhs
