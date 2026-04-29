# Quick Reference - Modernization Changes

## 🆕 New Modernized Scripts

### Python Scripts
```bash
python get_annot_stats_modernized.py     # Better annotation stats
python gene_count_summary_modernized.py  # Improved Venn diagrams
```

### Shell Scripts
```bash
./assemble_modernized.sh  # Template with best practices
```

---

## 📚 New Documentation Files

- **MODERNIZATION_GUIDE.md** - Comprehensive guide (read first!)
- **MODERNIZATION_SUMMARY.md** - Executive summary
- **requirements-dev.txt** - Development tools

---

## 🔧 New Features

### Python Scripts Now Have:
- ✅ Help: `python script.py -h`
- ✅ Verbose logging: `python script.py -v`
- ✅ Better error messages
- ✅ Type hints for IDE support
- ✅ Logging for debugging

### Shell Scripts Now Have:
- ✅ Help: `./script.sh -h`
- ✅ Error trapping
- ✅ Input validation
- ✅ Colored output
- ✅ Progress messages

---

## 🚀 Quick Start

### 1. Setup Environment
```bash
conda env create -f environment.yaml
conda activate bacterial-genomics-tutorial
```

### 2. Try New Scripts
```bash
# Get annotation stats
python get_annot_stats_modernized.py -v annotation_dir P7741

# Generate Venn diagram
python gene_count_summary_modernized.py P7741 Agy99 Liflandii data.csv
```

### 3. Run Tests
```bash
pip install -r requirements-dev.txt
pytest tests/ -v
```

---

## 🧭 One-Command Runner

Use the end-to-end runner to execute the pipeline in a reproducible run folder:

```bash
# Full workflow
./run_pipeline.sh --profile full

# Quick validation
./run_pipeline.sh --profile demo

# Reuse existing data
./run_pipeline.sh --profile small --skip-download
```

Profiles:
- demo - Download + QC + trim + assemble
- small - demo + polish + reorder + typing + AMR + annotation
- full - small + pangenome + summary plots

---

## 📋 Updated Dependencies

### Key Changes:
- Python 3.11 (was unspecified)
- All packages now have versions
- Added testing tools (pytest)
- Added code quality tools (black, flake8, mypy)

### Install:
```bash
conda env create -f environment.yaml
```

---

## ✅ Verification Commands

```bash
# Check types
mypy get_annot_stats_modernized.py

# Format code
black .

# Lint code
flake8 .

# Run tests
pytest tests/ -v
```

---

## 📖 Learning Resources

**Start Here:**
1. Read: `MODERNIZATION_SUMMARY.md` (5 min)
2. Read: `MODERNIZATION_GUIDE.md` (20 min)
3. Try: `python get_annot_stats_modernized.py -h`
4. Run: `pytest tests/ -v`

**For Each Script:**
```bash
python script_name.py -h  # Always works!
```

---

## 📓 Notebook Walkthrough

Start the hands-on walkthrough in [notebooks/Walkthrough.ipynb](notebooks/Walkthrough.ipynb).

---

## 🔄 Migration

### Old Way (Still Works!)
```bash
python get_annot_stats.py annotation_dir P7741
```

### New Way (Recommended)
```bash
python get_annot_stats_modernized.py annotation_dir P7741
python get_annot_stats_modernized.py -v -o stats.txt annotation_dir P7741
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Module not found | `pip install -r requirements-dev.txt` |
| Permission denied | `chmod +x script.sh` |
| Command not found | Activate conda: `conda activate bacterial-genomics-tutorial` |
| Tests fail | Run: `pytest tests/ -v` to see details |

---

## 📁 File Structure

```
bacterial-genomics-tutorial/
├── get_annot_stats_modernized.py       ✨ NEW
├── gene_count_summary_modernized.py    ✨ NEW
├── assemble_modernized.sh              ✨ NEW
├── tests/                              ✨ NEW
│   ├── __init__.py
│   └── test_annotation_scripts.py
├── MODERNIZATION_GUIDE.md              ✨ NEW
├── MODERNIZATION_SUMMARY.md            ✨ NEW
├── requirements-dev.txt                ✨ NEW
├── environment.yaml                    ✏️ UPDATED
├── pip-requirements.txt                ✏️ UPDATED
├── get_annot_stats.py                  (original - still works)
├── gene_count_summary.py               (original - still works)
└── ... (other original files)
```

---

## 💡 Pro Tips

### For Debugging
```bash
# Enable verbose logging
python script.py -v

# Run specific test
pytest tests/test_annotation_scripts.py::TestGetAnnotStatsModernized -v
```

### For Development
```bash
# Format code
black .

# Check types while coding
mypy --watch .

# Run tests automatically
pytest tests/ --watch
```

### For Production
```bash
# Run all checks
black . && flake8 . && mypy . && pytest tests/ -v
```

---

## 🎯 Next Steps

1. ✅ Read `MODERNIZATION_SUMMARY.md`
2. ✅ Try `python get_annot_stats_modernized.py -h`
3. ✅ Run `pytest tests/ -v`
4. ✅ Update your workflows
5. ✅ Share feedback!

---

## 📞 Questions?

- Check the help: `python script.py -h`
- Read the guides: `MODERNIZATION_*.md`
- Review tests: `tests/test_annotation_scripts.py`
- Check logging output: Use `-v` flag

---

**Last Updated:** April 29, 2026  
**Version:** 1.0.0  
**Status:** Ready for Production ✅
