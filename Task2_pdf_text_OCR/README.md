# Task #2: Batch OCR for arXiv PDFs

## 🎯 Project Overview

Professional **PDF to Text OCR converter** that processes 200 arXiv papers from Task #1 using **pdf2image + Tesseract OCR**.

**Status:** ✅ Production ready

---

## 🚀 Quick Start (< 10 minutes)

```bash
# 1. Install system dependencies
brew install tesseract poppler  # macOS
# sudo apt-get install tesseract-ocr poppler-utils  # Linux

# 2. Setup Python environment
cd task2_pdf_ocr
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Test with 3 papers
python test_quick.py

# 4. Full run (200 papers, 2-4 hours)
python pdf_to_text_ocr.py
```

**Output:** `pdf_ocr/` folder with ~200 TXT files

---

## 📁 Project Structure

```
task2_pdf_ocr/
├── pdf_to_text_ocr.py     # Main OCR script ⭐
├── test_quick.py          # Quick test (3 papers)
├── requirements.txt       # Python dependencies
├── START_HERE.md          # 📍 Comprehensive guide
├── README.md              # This file
│
├── notebooks/
│   └── task2_demo.ipynb   # Jupyter demo
│
├── pdfs/                  # Downloaded PDFs
├── pdf_ocr/              # ⭐ OUTPUT: TXT files (deliverable)
└── logs/                  # Execution logs
    ├── pdf_ocr.log
    └── task2_report.json
```

---

## 🏗️ How It Works

### Complete Pipeline

```
Task #1 JSON (arxiv_clean.json)
    ↓
Extract PDF URLs (pdf_url field)
    ↓
Download PDFs → pdfs/
    ↓
Convert to Images (pdf2image @ 300 DPI)
    ↓
OCR with Tesseract (layout-preserving PSM mode 1)
    ↓
Save TXT files → pdf_ocr/
```

### Key Features

✅ **Automatic PDF download** from arXiv  
✅ **High-quality conversion** (300 DPI default)  
✅ **Layout preservation** (PSM mode 1)  
✅ **Resume capability** (skips processed files)  
✅ **Progress tracking** [X/200]  
✅ **Comprehensive logging**  
✅ **Batch processing** (handles hundreds of papers)  
✅ **Error handling** (continues on failures)  

---

## 📊 Expected Performance

| Metric | Value |
|--------|-------|
| **Total time** | 2-4 hours (200 papers) |
| **Per paper** | 40-100 seconds average |
| **Success rate** | 95-98% |
| **Disk space** | 2-5 GB (PDFs + temp images) |
| **Output files** | ~200 TXT files |

### Timing Breakdown

- PDF download: 5-10 sec
- PDF to images: 10-30 sec
- OCR processing: 20-60 sec
- **Total per paper:** 40-100 sec

---

## ⚙️ Configuration

### Process Fewer Papers

```python
# Edit pdf_to_text_ocr.py, line ~314
MAX_PAPERS = 10  # Instead of None
```

### Adjust OCR Quality

```python
# Edit pdf_to_text_ocr.py, line ~317
DPI = 200  # Fast, lower quality
DPI = 300  # Recommended (default)
DPI = 400  # Slow, higher quality
```

### Change Layout Mode

```python
# Edit pdf_to_text_ocr.py, line ~316
PRESERVE_LAYOUT = False  # Faster, simple text
PRESERVE_LAYOUT = True   # Layout-preserving (default)
```

---

## 📄 Output Format

Each TXT file contains:

```
arXiv ID: 2411.00123
Title: Enhancing Large Language Models with RAG
PDF URL: https://arxiv.org/pdf/2411.00123
Date Processed: 2025-11-03T12:00:00
Total Pages: 12
Total Characters: 28492

================================================================================
EXTRACTED TEXT
================================================================================

================================================================================
PAGE 1
================================================================================

Enhancing Large Language Models with 
Retrieval-Augmented Generation

John Doe, Jane Smith
University of AI Research

Abstract
We present a novel approach...

================================================================================
PAGE 2
================================================================================

1. Introduction
Large language models have shown...

[... rest of paper ...]
```

---

## 🐛 Common Issues & Solutions

### Issue 1: Tesseract not found

```bash
# Install Tesseract
brew install tesseract  # macOS
sudo apt-get install tesseract-ocr  # Linux

# Verify
tesseract --version
```

### Issue 2: Poppler not found

```bash
# Install Poppler (required for pdf2image)
brew install poppler  # macOS
sudo apt-get install poppler-utils  # Linux

# Verify
pdfinfo -v
```

### Issue 3: Task #1 JSON not found

```python
# Update path in pdf_to_text_ocr.py
TASK1_JSON = "/path/to/arxiv_clean.json"
```

### Issue 4: Out of disk space

```bash
# Check space
df -h

# Process in batches
MAX_PAPERS = 50  # Process 50 at a time
```

---

## ✅ Validation

### Quick Checks

```bash
# Count output files
ls pdf_ocr/*.txt | wc -l  # ~200

# Check sizes
du -sh pdf_ocr/

# View sample
head -100 pdf_ocr/arxiv_*.txt | head -100

# Check stats
cat logs/task2_report.json | jq '.statistics'
```

### Quality Check

```bash
# Pick random file
cat pdf_ocr/arxiv_2411.00123.txt

# Should contain:
# ✅ Metadata header
# ✅ Page separators
# ✅ Readable extracted text
# ✅ Proper layout (paragraphs, sections)
```

---

## 📦 Deliverables

For submission:

1. ✅ **pdf_ocr/** folder - ~200 TXT files
2. ✅ **pdf_to_text_ocr.py** - Main script
3. ✅ **logs/task2_report.json** - Processing stats
4. ✅ **notebooks/task2_demo.ipynb** - Demo notebook (optional)

**Package command:**
```bash
tar -czf task2_submission.tar.gz pdf_ocr/ pdf_to_text_ocr.py logs/
```

---

## 🔗 Integration

### Task #1 Dependency

Requires `arxiv_clean.json` from Task #1 with:
- `pdf_url` field (for downloading PDFs)
- `arxiv_id` field (for file naming)
- `title` field (for metadata)

### Task #4 Integration

Task #4 will merge:
- **Task #1:** Abstracts (arxiv_clean.json)
- **Task #2:** Full papers (pdf_ocr/*.txt) ← This task
- **Task #3:** Talks (talks_transcripts.jsonl)

---

## 🎓 Learning Outcomes

✅ PDF processing with pdf2image  
✅ High-quality OCR with Tesseract  
✅ Layout preservation techniques  
✅ Batch document processing  
✅ Error handling and resume logic  
✅ Resource management (disk, memory)  
✅ Progress tracking and logging  

---

## 📚 Documentation

- **START_HERE.md** - Comprehensive setup guide
- **TASK2_GUIDE.md** - Implementation details (coming)
- **logs/pdf_ocr.log** - Detailed execution log
- **logs/task2_report.json** - Statistics

---

## 💡 Pro Tips

1. **Test first:** Run `test_quick.py` before full processing
2. **Monitor progress:** `tail -f logs/pdf_ocr.log`
3. **Resume friendly:** Skips already processed papers
4. **Batch if needed:** Set MAX_PAPERS for smaller batches
5. **Check disk space:** PDFs + images = 2-5 GB

---

## 🔧 Advanced Options

### Custom Tesseract Config

```python
# In ocr_image() method
config = '--psm 1 --oem 3'  # OEM 3 = LSTM + legacy
config = '--psm 3'          # Faster, less layout
config = '--psm 6'          # Single block of text
```

### Parallel Processing

```python
# For advanced users: Add multiprocessing
from multiprocessing import Pool

# Process multiple papers simultaneously
# (Requires code modifications)
```

---

## 🎯 Next Steps

After completing Task #2:

1. ✅ Validate output (check 3-5 TXT files)
2. ✅ Review logs/task2_report.json
3. → **Task #3:** Whisper ASR for conference talks
4. → **Task #4:** Merge & clean all datasets

---

## 📞 Quick Commands

```bash
# Setup
pip install -r requirements.txt

# Test
python test_quick.py

# Full run
python pdf_to_text_ocr.py

# Monitor
tail -f logs/pdf_ocr.log

# Validate
ls pdf_ocr/*.txt | wc -l
du -sh pdf_ocr/
```

---

**Ready to convert PDFs? Run:** `python test_quick.py`

**Questions?** Check **START_HERE.md** for detailed guide!

---

**Status:** ✅ Production ready  
**Dependencies:** Tesseract, Poppler, Python packages  
**Estimated time:** 2-4 hours for 200 papers  
**Output:** pdf_ocr/ folder with ~200 TXT files
