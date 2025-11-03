"""
QUICK START: Tesseract OCR - Ready to Run!
===========================================

Just update the image_path and run this script to see OCR in action.

Author: Emma Wang
"""

import pytesseract
from PIL import Image, ImageEnhance
import cv2
import numpy as np
import os


def quick_ocr(image_path):
    """
    Simplest possible OCR - one line!
    """
    print("\n1️⃣ QUICK OCR (No preprocessing)")
    print("=" * 60)
    
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        
        print("Extracted text:")
        print(text)
        print(f"\nTotal characters: {len(text)}")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def better_ocr(image_path):
    """
    Improved OCR with basic preprocessing
    """
    print("\n2️⃣ IMPROVED OCR (With preprocessing)")
    print("=" * 60)
    
    try:
        # Load and preprocess
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Extract text
        text = pytesseract.image_to_string(gray)
        
        print("Extracted text:")
        print(text)
        print(f"\nTotal characters: {len(text)}")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def best_ocr(image_path):
    """
    Best quality OCR with full preprocessing pipeline
    """
    print("\n3️⃣ BEST QUALITY OCR (Full preprocessing)")
    print("=" * 60)
    
    try:
        # Load
        img = cv2.imread(image_path)
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Denoise
        denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
        
        # Adaptive threshold
        thresh = cv2.adaptiveThreshold(
            denoised, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2
        )
        
        # OCR with optimal PSM
        config = '--psm 6'  # Single uniform block
        text = pytesseract.image_to_string(thresh, config=config)
        
        print("Extracted text:")
        print(text)
        print(f"\nTotal characters: {len(text)}")
        
        # Save preprocessed image for inspection
        cv2.imwrite('preprocessed_output.png', thresh)
        print("\n✅ Preprocessed image saved: preprocessed_output.png")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def analyze_confidence(image_path):
    """
    Show which words OCR is confident about
    """
    print("\n4️⃣ CONFIDENCE ANALYSIS")
    print("=" * 60)
    
    try:
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Get detailed data
        data = pytesseract.image_to_data(
            gray,
            output_type=pytesseract.Output.DICT
        )
        
        # Analyze
        high_conf = []
        low_conf = []
        
        for i, conf in enumerate(data['conf']):
            if int(conf) > 0:
                text = data['text'][i]
                if text.strip():
                    if int(conf) >= 70:
                        high_conf.append((text, conf))
                    else:
                        low_conf.append((text, conf))
        
        print(f"\n✅ High confidence words (>= 70%): {len(high_conf)}")
        for text, conf in high_conf[:10]:  # Show first 10
            print(f"   '{text}' - {conf}%")
        
        print(f"\n⚠️  Low confidence words (< 70%): {len(low_conf)}")
        for text, conf in low_conf[:10]:  # Show first 10
            print(f"   '{text}' - {conf}%")
        
        # Calculate average
        all_conf = [int(c) for c in data['conf'] if int(c) > 0]
        if all_conf:
            avg = sum(all_conf) / len(all_conf)
            print(f"\n📊 Average confidence: {avg:.1f}%")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def extract_invoice_data(image_path):
    """
    Example: Extract structured data from invoice/receipt
    """
    print("\n5️⃣ STRUCTURED DATA EXTRACTION (Invoice/Receipt)")
    print("=" * 60)
    
    try:
        # Preprocess
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh = cv2.adaptiveThreshold(
            gray, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2
        )
        
        # OCR
        config = '--psm 6'
        text = pytesseract.image_to_string(thresh, config=config)
        
        print("Full text:")
        print(text)
        
        # Extract structured fields
        import re
        
        fields = {}
        
        # Invoice number
        inv_match = re.search(r'Invoice[#\s:]*(\w+)', text, re.IGNORECASE)
        fields['Invoice Number'] = inv_match.group(1) if inv_match else 'Not found'
        
        # Date
        date_match = re.search(r'(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})', text)
        fields['Date'] = date_match.group(1) if date_match else 'Not found'
        
        # Total
        total_match = re.search(r'Total[:\s]*[\$€£]?([\d,]+\.?\d*)', text, re.IGNORECASE)
        fields['Total'] = total_match.group(1) if total_match else 'Not found'
        
        print("\n📋 Extracted structured data:")
        for key, value in fields.items():
            print(f"   {key}: {value}")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """
    Main function - update IMAGE_PATH and run!
    """
    print("\n" + "=" * 80)
    print(" " * 25 + "TESSERACT OCR - QUICK START")
    print("=" * 80)
    
    # ⚠️ UPDATE THIS PATH TO YOUR IMAGE
    IMAGE_PATH = '/home/claude/sample_text.png'
    
    # Check if image exists
    if not os.path.exists(IMAGE_PATH):
        print(f"\n❌ Image not found: {IMAGE_PATH}")
        print("\n💡 To create a test image, run:")
        print("   python tesseract_tutorial.py")
        print("\nOr update IMAGE_PATH to point to your own image.")
        return
    
    print(f"\n📁 Processing image: {IMAGE_PATH}")
    
    # Check Tesseract installation
    try:
        version = pytesseract.get_tesseract_version()
        print(f"✅ Tesseract version: {version}")
    except Exception as e:
        print(f"❌ Tesseract not found: {e}")
        print("\n💡 Install Tesseract:")
        print("   macOS: brew install tesseract")
        print("   Linux: sudo apt-get install tesseract-ocr")
        return
    
    # Run all methods
    quick_ocr(IMAGE_PATH)
    better_ocr(IMAGE_PATH)
    best_ocr(IMAGE_PATH)
    analyze_confidence(IMAGE_PATH)
    extract_invoice_data(IMAGE_PATH)
    
    print("\n" + "=" * 80)
    print("✅ ALL TESTS COMPLETE!")
    print("=" * 80)
    
    print("\n📚 Next Steps:")
    print("   1. Try with your own images (invoices, receipts, documents)")
    print("   2. Experiment with different PSM modes (--psm 3, 4, 6, 7, 11)")
    print("   3. Adjust preprocessing parameters (threshold, denoise)")
    print("   4. Check out the full tutorial: tesseract_tutorial.py")
    print("   5. Read the complete guide: TESSERACT_GUIDE.md")
    
    print("\n💡 Pro Tips:")
    print("   - Higher DPI = better accuracy (min 300 DPI)")
    print("   - Black text on white background works best")
    print("   - Remove shadows, wrinkles, and glare")
    print("   - Use PSM 6 for invoices/receipts")
    print("   - Use PSM 11 for scattered text (signs, posters)")


if __name__ == "__main__":
    main()


"""
===========================================
QUICK REFERENCE CARD
===========================================

PREPROCESSING STEPS:
1. Grayscale:       cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
2. Denoise:         cv2.fastNlMeansDenoising(img, None, 10, 7, 21)
3. Threshold:       cv2.adaptiveThreshold(img, 255, ADAPTIVE_THRESH_GAUSSIAN_C, THRESH_BINARY, 11, 2)

PSM MODES:
--psm 3:  Fully automatic (default)
--psm 4:  Single column
--psm 6:  Single uniform block (BEST for invoices)
--psm 7:  Single text line
--psm 11: Sparse text (signs, labels)

USAGE:
pytesseract.image_to_string(img, config='--psm 6')

LANGUAGES:
pytesseract.image_to_string(img, lang='eng')
pytesseract.image_to_string(img, lang='chi_sim')  # Chinese
pytesseract.image_to_string(img, lang='eng+chi_sim')  # Multiple

CONFIDENCE:
data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
# data['conf'] contains confidence scores (0-100)

===========================================
"""
