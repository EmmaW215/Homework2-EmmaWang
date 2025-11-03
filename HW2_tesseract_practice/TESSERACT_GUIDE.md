# 🎓 Tesseract OCR - Complete Learning Guide

**Author:** Emma Wang  
**Level:** Beginner to Advanced  
**Duration:** 2-3 hours  
**Prerequisites:** Python 3.x, Basic image processing knowledge

---

## 📚 Table of Contents

1. [Installation & Setup](#installation--setup)
2. [Understanding Tesseract](#understanding-tesseract)
3. [The 4 Best Practices](#the-4-best-practices)
4. [Step-by-Step Tutorials](#step-by-step-tutorials)
5. [Real-World Projects](#real-world-projects)
6. [Troubleshooting](#troubleshooting)
7. [Advanced Topics](#advanced-topics)

---

## 1. Installation & Setup

### Step 1.1: Install Tesseract Engine

**macOS:**
```bash
brew install tesseract
```

**Ubuntu/Linux:**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

**Verify installation:**
```bash
tesseract --version
# Should show: tesseract 5.x.x
```

### Step 1.2: Install Python Dependencies

```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install pytesseract pillow opencv-python numpy matplotlib
```

### Step 1.3: Test Installation

```python
import pytesseract
from PIL import Image

# Should not raise errors
print(pytesseract.get_tesseract_version())
```

✅ **Checkpoint:** You should see the Tesseract version printed

---

## 2. Understanding Tesseract

### 2.1 What is Tesseract?

Tesseract is an **Optical Character Recognition (OCR)** engine that:
- Converts images of text into machine-readable text
- Supports 100+ languages
- Developed by Google (originally by HP)
- Open-source and free

### 2.2 OCR Pipeline

```
Input Image → Preprocessing → Tesseract → Text Output
     ↓
  [Your job]
```

**Your role:** Prepare the image for optimal OCR accuracy

### 2.3 Key Concepts

#### **Page Segmentation Mode (PSM)**
Tells Tesseract how to interpret the layout:

| PSM | Description | Use Case |
|-----|-------------|----------|
| 0 | Orientation detection only | Check text orientation |
| 3 | Fully automatic (default) | General documents |
| 4 | Single column | Articles, letters |
| 6 | Single uniform block | Invoices, receipts |
| 7 | Single line | Headers, titles |
| 11 | Sparse text | Signs, labels |
| 13 | Raw line (no layout analysis) | Very clean single line |

#### **OCR Engine Mode (OEM)**
Tells Tesseract which recognition engine to use:

| OEM | Description | Speed | Accuracy |
|-----|-------------|-------|----------|
| 0 | Legacy engine | Fast | Medium |
| 1 | Neural nets (LSTM) | Slow | High |
| 2 | Legacy + LSTM | Medium | High |
| 3 | Default (based on availability) | Varies | Varies |

---

## 3. The 4 Best Practices

### 🎯 Best Practice #1: Preprocess Images

**Why?** Tesseract works best with high-contrast, noise-free images.

#### Technique 1: Convert to Grayscale
```python
import cv2

img = cv2.imread('image.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
```

**Impact:** 
- ✅ Reduces data size (3x smaller)
- ✅ Simplifies processing
- ✅ Removes color noise

#### Technique 2: Adjust Brightness/Contrast
```python
from PIL import Image, ImageEnhance

img = Image.open('image.png')

# Increase contrast
enhancer = ImageEnhance.Contrast(img)
img = enhancer.enhance(2.0)  # 2x contrast

# Increase brightness if too dark
enhancer = ImageEnhance.Brightness(img)
img = enhancer.enhance(1.2)  # 1.2x brightness
```

**Impact:**
- ✅ Makes text stand out
- ✅ Improves edge detection
- ⚠️ Don't over-enhance (causes artifacts)

#### Technique 3: Thresholding
```python
# Simple threshold
_, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# Adaptive threshold (BETTER)
thresh = cv2.adaptiveThreshold(
    gray, 255, 
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
    cv2.THRESH_BINARY, 
    11, 2
)
```

**Impact:**
- ✅ Converts to pure black/white
- ✅ Removes gray areas (confusion)
- ✅ Adaptive handles varying lighting

#### Technique 4: Noise Removal
```python
# Denoise
denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)

# Morphological operations (remove dots/specks)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
clean = cv2.morphologyEx(denoised, cv2.MORPH_CLOSE, kernel)
```

**Impact:**
- ✅ Removes scanner artifacts
- ✅ Fills small gaps in text
- ✅ Smooths jagged edges

#### 📊 Preprocessing Comparison

| Method | Accuracy Gain | Speed | Complexity |
|--------|--------------|-------|------------|
| None | Baseline | Fast | Easy |
| Grayscale | +5% | Fast | Easy |
| Threshold | +15% | Fast | Easy |
| Denoise | +10% | Slow | Medium |
| All combined | +25-30% | Slow | Medium |

---

### 🎯 Best Practice #2: Use Correct PSM

**Why?** Wrong PSM = wrong layout interpretation = garbage output

#### Decision Tree

```
Is your document...
├─ A full page? → PSM 3 (default)
├─ A single column article? → PSM 4
├─ An invoice/receipt (structured)? → PSM 6
├─ A single line (header/title)? → PSM 7
├─ A single word? → PSM 8
├─ A single character? → PSM 10
└─ Scattered text (sign, poster)? → PSM 11
```

#### Example: Invoice Processing

```python
# WRONG
text = pytesseract.image_to_string(img)  # Uses PSM 3
# Result: Text order may be scrambled

# RIGHT
config = '--psm 6'  # Single uniform block
text = pytesseract.image_to_string(img, config=config)
# Result: Preserves invoice structure
```

#### Experimentation Script

```python
for psm in [3, 4, 6, 7, 11]:
    config = f'--psm {psm}'
    text = pytesseract.image_to_string(img, config=config)
    print(f"PSM {psm}: {len(text)} chars, {text[:50]}...")
```

---

### 🎯 Best Practice #3: Choose the Right Language

**Why?** Tesseract uses language-specific models for better accuracy

#### Check Available Languages
```bash
tesseract --list-langs
```

#### Install More Languages
```bash
# macOS
brew install tesseract-lang

# Linux
sudo apt-get install tesseract-ocr-chi-sim  # Chinese Simplified
sudo apt-get install tesseract-ocr-spa      # Spanish
sudo apt-get install tesseract-ocr-fra      # French
```

#### Use in Python
```python
# English (default)
text = pytesseract.image_to_string(img, lang='eng')

# Chinese Simplified
text = pytesseract.image_to_string(img, lang='chi_sim')

# Multiple languages
text = pytesseract.image_to_string(img, lang='eng+chi_sim')
```

#### Common Language Codes

| Language | Code | Install Command |
|----------|------|-----------------|
| English | `eng` | Pre-installed |
| Chinese (Simplified) | `chi_sim` | `brew install tesseract-lang` |
| Spanish | `spa` | Same as above |
| French | `fra` | Same as above |
| German | `deu` | Same as above |
| Japanese | `jpn` | Same as above |

---

### 🎯 Best Practice #4: Custom Training (Advanced)

**Why?** For specialized fonts, handwriting, or domain-specific text

⚠️ **Note:** This is advanced - skip if you're just starting

#### When to Consider Custom Training

- [ ] Default Tesseract < 70% accuracy
- [ ] Specialized fonts (old typewriters, stylized)
- [ ] Handwritten text
- [ ] Domain-specific vocabulary
- [ ] Unusual layouts

#### Training Process Overview

```
1. Collect training images (100+ samples)
2. Create ground truth (manually label text)
3. Generate box files
4. Train model with Tesseract tools
5. Test and iterate
```

**Resources:**
- [Official Training Guide](https://tesseract-ocr.github.io/tessdoc/Training-Tesseract.html)
- Use tools like `jTessBoxEditor` for labeling

**Alternative:** Use modern deep learning OCR:
- EasyOCR (better for handwriting)
- PaddleOCR (multilingual)
- TrOCR (transformer-based)

---

## 4. Step-by-Step Tutorials

### Tutorial 1: Basic OCR (5 minutes)

**Goal:** Extract text from a clean image

```python
import pytesseract
from PIL import Image

# Load image
img = Image.open('document.png')

# Extract text
text = pytesseract.image_to_string(img)

print(text)
```

**Expected Output:** Readable text from the image

---

### Tutorial 2: Preprocessing Pipeline (10 minutes)

**Goal:** Build a robust preprocessing pipeline

```python
import cv2
import pytesseract

def preprocess(image_path):
    # Load
    img = cv2.imread(image_path)
    
    # Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Denoise
    denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
    
    # Threshold
    thresh = cv2.adaptiveThreshold(
        denoised, 255, 
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 11, 2
    )
    
    return thresh

# Use it
processed = preprocess('noisy_image.png')
text = pytesseract.image_to_string(processed)
print(text)
```

---

### Tutorial 3: Confidence Analysis (15 minutes)

**Goal:** Understand OCR reliability

```python
import pytesseract
import cv2

img = cv2.imread('document.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Get detailed data
data = pytesseract.image_to_data(
    gray, 
    output_type=pytesseract.Output.DICT
)

# Analyze
for i, conf in enumerate(data['conf']):
    if int(conf) > 0:  # Valid detection
        text = data['text'][i]
        confidence = int(conf)
        
        if confidence < 60:
            print(f"⚠️ Low confidence: '{text}' ({confidence}%)")
        else:
            print(f"✅ High confidence: '{text}' ({confidence}%)")
```

**Action:** Re-process low-confidence areas with different PSM

---

### Tutorial 4: Structured Data Extraction (20 minutes)

**Goal:** Extract invoice fields automatically

```python
import pytesseract
import cv2
import re

def extract_invoice_data(image_path):
    # Preprocess
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(
        gray, 255, 
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 11, 2
    )
    
    # OCR with invoice-optimized settings
    config = '--psm 6'
    text = pytesseract.image_to_string(thresh, config=config)
    
    # Extract fields
    invoice_data = {}
    
    # Invoice number
    inv_match = re.search(r'Invoice[#\s:]*(\w+)', text, re.I)
    invoice_data['invoice_number'] = inv_match.group(1) if inv_match else None
    
    # Date
    date_match = re.search(r'(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})', text)
    invoice_data['date'] = date_match.group(1) if date_match else None
    
    # Total
    total_match = re.search(r'Total[:\s]*[\$€£]?([\d,]+\.?\d*)', text, re.I)
    invoice_data['total'] = total_match.group(1) if total_match else None
    
    return invoice_data

# Use it
data = extract_invoice_data('invoice.png')
print(data)
# {'invoice_number': '12345', 'date': '11/02/2025', 'total': '1,234.56'}
```

---

## 5. Real-World Projects

### Project 1: Receipt Scanner App 📱

**Features:**
- Take photo of receipt
- Extract total, date, merchant
- Save to database

**Skills Used:**
- Image preprocessing
- PSM 6 (receipt layout)
- Regex pattern matching

**Starter Code:** See `tesseract_practice.py` - Exercise 5

---

### Project 2: Business Card Digitizer 💼

**Features:**
- Scan business card
- Extract name, phone, email
- Export to contacts

**Skills Used:**
- PSM 11 (sparse text)
- Multiple language support
- Contact format parsing

---

### Project 3: PDF Document Digitizer 📄

**Features:**
- Convert scanned PDFs to searchable text
- Preserve formatting
- Batch processing

**Skills Used:**
- PDF to image conversion
- PSM 3 (full page)
- Performance optimization

---

## 6. Troubleshooting

### Common Issues & Solutions

#### Issue 1: "TesseractNotFoundError"

**Cause:** Tesseract not installed or not in PATH

**Solution:**
```bash
# macOS
brew install tesseract

# Linux
sudo apt-get install tesseract-ocr

# Set path manually (if needed)
pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'
```

---

#### Issue 2: Poor Accuracy (< 70%)

**Debugging Checklist:**
- [ ] Try grayscale preprocessing
- [ ] Try thresholding
- [ ] Test different PSM modes
- [ ] Check image resolution (min 300 DPI)
- [ ] Verify correct language
- [ ] Check confidence scores

**Solution Template:**
```python
# Debug pipeline
img = cv2.imread('problem_image.png')

# Try different preprocessing
methods = ['original', 'grayscale', 'threshold', 'denoise']

for method in methods:
    processed = preprocess(img, method)
    text = pytesseract.image_to_string(processed)
    print(f"{method}: {len(text)} chars")
```

---

#### Issue 3: Wrong Text Order

**Cause:** Incorrect PSM mode

**Solution:** Use PSM 6 for structured documents, PSM 4 for columns

---

#### Issue 4: Slow Performance

**Optimization Checklist:**
- [ ] Resize large images (max 1920x1080)
- [ ] Use grayscale
- [ ] Choose faster PSM (e.g., 7 for single lines)
- [ ] Process in batches
- [ ] Use multiprocessing for multiple images

---

## 7. Advanced Topics

### Topic 1: Bounding Box Detection

Extract word positions for highlighting:

```python
data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)

for i in range(len(data['text'])):
    if int(data['conf'][i]) > 60:
        x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
        # Draw rectangle at (x, y, w, h)
```

### Topic 2: Table Extraction

Use `--psm 6` with `preserve_interword_spaces`:

```python
config = '--psm 6 preserve_interword_spaces=1'
text = pytesseract.image_to_string(img, config=config)
```

### Topic 3: Orientation Detection

Automatically rotate skewed images:

```python
osd = pytesseract.image_to_osd(img)
angle = int(re.search('(?<=Rotate: )\d+', osd).group(0))

# Rotate image by angle
```

---

## 📝 Practice Roadmap

### Week 1: Fundamentals
- ✅ Install and setup
- ✅ Run basic OCR on 10 different images
- ✅ Experiment with all PSM modes
- ✅ Compare preprocessing techniques

### Week 2: Practical Applications
- ✅ Build receipt scanner
- ✅ Extract invoice data
- ✅ Process business cards
- ✅ Handle multilingual documents

### Week 3: Advanced Techniques
- ✅ Optimize performance
- ✅ Handle edge cases (skewed, noisy)
- ✅ Extract tables and structured data
- ✅ Build end-to-end pipeline

---

## 🎯 Final Checklist

Before you consider yourself proficient:

- [ ] Can preprocess images effectively
- [ ] Understand when to use each PSM mode
- [ ] Can handle multiple languages
- [ ] Know how to debug poor accuracy
- [ ] Built at least 1 real-world project
- [ ] Can extract structured data with regex
- [ ] Understand confidence scores
- [ ] Can optimize for performance

---

## 📚 Resources

### Official Documentation
- [Tesseract Documentation](https://tesseract-ocr.github.io/)
- [pytesseract GitHub](https://github.com/madmaze/pytesseract)

### Tutorials & Articles
- [Tesseract Best Practices](https://tesseract-ocr.github.io/tessdoc/ImproveQuality.html)
- [OpenCV Preprocessing Guide](https://docs.opencv.org/master/d7/d4d/tutorial_py_thresholding.html)

### Alternative OCR Tools
- [EasyOCR](https://github.com/JaidedAI/EasyOCR) (Deep learning-based)
- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) (Multilingual)
- [TrOCR](https://huggingface.co/docs/transformers/model_doc/trocr) (Transformer-based)

---

**Good luck with your Tesseract learning journey! 🚀**

*Questions? Run the provided scripts and experiment!*
