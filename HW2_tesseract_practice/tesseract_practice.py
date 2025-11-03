"""
TESSERACT OCR - QUICK START PRACTICE GUIDE
==========================================

Author: Emma Wang
Purpose: Hands-on exercises to master Tesseract OCR

SETUP CHECKLIST:
✅ Install Tesseract: brew install tesseract
✅ Install Python packages: pip install pytesseract pillow opencv-python
✅ Verify: tesseract --version

==========================================
EXERCISE 1: BASIC OCR (5 minutes)
==========================================
"""

import pytesseract
from PIL import Image
import cv2

def exercise_1_basic_ocr():
    """
    Exercise 1: Extract text from a simple image
    
    Learning objective: Understand basic OCR workflow
    """
    print("EXERCISE 1: BASIC OCR")
    print("=" * 60)
    
    # TODO: Replace with your image path
    image_path = '/Users/emmawang/AI_Projects/VicEdu_ML/HW2_DataCollectionExtraction/tesseract_practice/sample_text.png'
    
    try:
        # Method 1: Using PIL
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        
        print("Extracted text:")
        print(text)
        
        # CHALLENGE: How many words were extracted?
        word_count = len(text.split())
        print(f"\nTotal words: {word_count}")
        
    except FileNotFoundError:
        print("❌ Image not found. Please update 'image_path'")
        print("Create a test image with: python tesseract_tutorial.py")


"""
==========================================
EXERCISE 2: PREPROCESSING COMPARISON (10 minutes)
==========================================
"""

def exercise_2_preprocessing():
    """
    Exercise 2: Compare different preprocessing techniques
    
    Learning objective: Understand how preprocessing affects accuracy
    """
    print("\nEXERCISE 2: PREPROCESSING")
    print("=" * 60)
    
    image_path = '/Users/emmawang/AI_Projects/VicEdu_ML/HW2_DataCollectionExtraction/tesseract_practice/sample_text.png'
    
    try:
        # Original (no preprocessing)
        img_original = cv2.imread(image_path)
        text_original = pytesseract.image_to_string(img_original)
        
        # Grayscale
        img_gray = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)
        text_gray = pytesseract.image_to_string(img_gray)
        
        # Grayscale + Threshold
        _, img_thresh = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)
        text_thresh = pytesseract.image_to_string(img_thresh)
        
        # Compare results
        print(f"Original:    {len(text_original)} chars")
        print(f"Grayscale:   {len(text_gray)} chars")
        print(f"Threshold:   {len(text_thresh)} chars")
        
        # CHALLENGE: Which preprocessing gave the best result?
        # Hint: Compare the actual text content
        
    except Exception as e:
        print(f"❌ Error: {e}")


"""
==========================================
EXERCISE 3: PSM MODES (15 minutes)
==========================================
"""

def exercise_3_psm_modes():
    """
    Exercise 3: Test different Page Segmentation Modes
    
    Learning objective: Choose the right PSM for your use case
    """
    print("\nEXERCISE 3: PSM MODES")
    print("=" * 60)
    
    image_path = '/Users/emmawang/AI_Projects/VicEdu_ML/HW2_DataCollectionExtraction/tesseract_practice/sample_text.png'
    
    # PSM modes to test
    test_cases = {
        'Invoice/Receipt': 6,      # Single uniform block
        'Single line': 7,          # One line of text
        'Paragraph': 3,            # Automatic (default)
        'Scattered text': 11,      # Sparse text
    }
    
    try:
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        for use_case, psm in test_cases.items():
            config = f'--psm {psm}'
            text = pytesseract.image_to_string(img, config=config)
            
            print(f"\n{use_case} (PSM {psm}):")
            print(f"  Characters: {len(text)}")
            print(f"  Preview: {text[:50]}...")
        
        # CHALLENGE: Which PSM works best for your image type?
        # Try creating different image types to test
        
    except Exception as e:
        print(f"❌ Error: {e}")


"""
==========================================
EXERCISE 4: CONFIDENCE SCORES (10 minutes)
==========================================
"""

def exercise_4_confidence():
    """
    Exercise 4: Analyze OCR confidence scores
    
    Learning objective: Understand OCR accuracy and reliability
    """
    print("\nEXERCISE 4: CONFIDENCE SCORES")
    print("=" * 60)
    
    image_path = '/Users/emmawang/AI_Projects/VicEdu_ML/HW2_DataCollectionExtraction/tesseract_practice/sample_text.png'
    
    try:
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Get detailed data with confidence scores
        data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
        
        # Analyze confidence
        confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
        
        if confidences:
            avg_confidence = sum(confidences) / len(confidences)
            
            print(f"Total detections: {len(confidences)}")
            print(f"Average confidence: {avg_confidence:.1f}%")
            print(f"Min confidence: {min(confidences)}%")
            print(f"Max confidence: {max(confidences)}%")
            
            # Show low confidence words (potential errors)
            print("\n⚠️  Low confidence detections (< 70%):")
            for i, conf in enumerate(data['conf']):
                if 0 < int(conf) < 70:
                    text = data['text'][i]
                    if text.strip():
                        print(f"  '{text}' - {conf}%")
        
        # CHALLENGE: How can you improve low-confidence detections?
        # Hint: Try different preprocessing or PSM modes
        
    except Exception as e:
        print(f"❌ Error: {e}")


"""
==========================================
EXERCISE 5: REAL-WORLD APPLICATION (20 minutes)
==========================================
"""

def exercise_5_invoice_extraction():
    """
    Exercise 5: Extract structured data from an invoice
    
    Learning objective: Apply OCR to solve real-world problems
    """
    print("\nEXERCISE 5: INVOICE DATA EXTRACTION")
    print("=" * 60)
    
    image_path = '/Users/emmawang/AI_Projects/VicEdu_ML/HW2_DataCollectionExtraction/tesseract_practice/sample_text.png'  # Use an invoice image
    
    try:
        # Preprocess for invoices
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                     cv2.THRESH_BINARY, 11, 2)
        
        # Best PSM for invoices
        config = '--psm 6'
        text = pytesseract.image_to_string(img, config=config)
        
        print("Full extracted text:")
        print(text)
        
        # Extract specific fields using regex
        import re
        
        # TODO: Customize these patterns for your invoice
        patterns = {
            'Invoice Number': r'Invoice[#\s:]*(\w+)',
            'Date': r'Date[:\s]*(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})',
            'Total': r'Total[:\s]*[\$€£]?([\d,]+\.?\d*)',
            'Tax': r'Tax[:\s]*[\$€£]?([\d,]+\.?\d*)',
        }
        
        extracted = {}
        for field, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            extracted[field] = match.group(1) if match else 'Not found'
        
        print("\n📊 Extracted structured data:")
        for field, value in extracted.items():
            print(f"  {field}: {value}")
        
        # CHALLENGE: Add more patterns to extract:
        # - Company name
        # - Items and quantities
        # - Subtotal
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Tip: Create a sample invoice image or use a real one")


"""
==========================================
EXERCISE 6: MULTILINGUAL OCR (15 minutes)
==========================================
"""

def exercise_6_multilingual():
    """
    Exercise 6: Work with multiple languages
    
    Learning objective: Configure Tesseract for different languages
    """
    print("\nEXERCISE 6: MULTILINGUAL OCR")
    print("=" * 60)
    
    # Check available languages
    try:
        langs = pytesseract.get_languages()
        print(f"Installed languages: {', '.join(langs)}")
        
        # Test with different languages
        image_path = '/Users/emmawang/AI_Projects/VicEdu_ML/HW2_DataCollectionExtraction/tesseract_practice/sample_text.png'
        img = cv2.imread(image_path)
        
        if img is not None:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Test English
            text_eng = pytesseract.image_to_string(img, lang='eng')
            print(f"\nEnglish result: {len(text_eng)} chars")
            
            # CHALLENGE: Test with other languages
            # To install: brew install tesseract-lang
            # Examples: chi_sim (Chinese), spa (Spanish), fra (French)
            
            # Uncomment and test:
            # text_chi = pytesseract.image_to_string(img, lang='chi_sim')
            # print(f"Chinese result: {len(text_chi)} chars")
        
    except Exception as e:
        print(f"❌ Error: {e}")


"""
==========================================
BONUS EXERCISE: PERFORMANCE OPTIMIZATION
==========================================
"""

def bonus_performance_test():
    """
    Bonus: Measure and optimize OCR performance
    
    Learning objective: Understand speed vs accuracy tradeoffs
    """
    print("\nBONUS: PERFORMANCE OPTIMIZATION")
    print("=" * 60)
    
    import time
    
    image_path = '/Users/emmawang/AI_Projects/VicEdu_ML/HW2_DataCollectionExtraction/tesseract_practice/sample_text.png'
    
    try:
        img = cv2.imread(image_path)
        
        # Test configurations
        configs = [
            ('Default', ''),
            ('Fast (PSM 7)', '--psm 7'),
            ('Accurate (PSM 6 + OEM 1)', '--psm 6 --oem 1'),
        ]
        
        results = []
        
        for name, config in configs:
            start = time.time()
            text = pytesseract.image_to_string(img, config=config)
            elapsed = time.time() - start
            
            results.append({
                'name': name,
                'time': elapsed,
                'chars': len(text)
            })
            
            print(f"\n{name}:")
            print(f"  Time: {elapsed:.3f}s")
            print(f"  Output: {len(text)} chars")
        
        # Find fastest
        fastest = min(results, key=lambda x: x['time'])
        print(f"\n⚡ Fastest: {fastest['name']} ({fastest['time']:.3f}s)")
        
    except Exception as e:
        print(f"❌ Error: {e}")


"""
==========================================
MAIN PRACTICE RUNNER
==========================================
"""

def main():
    """
    Run all exercises sequentially
    """
    print("\n" + "=" * 80)
    print(" " * 20 + "TESSERACT OCR PRACTICE EXERCISES")
    print("=" * 80)
    
    exercises = [
        ("Exercise 1: Basic OCR", exercise_1_basic_ocr),
        ("Exercise 2: Preprocessing", exercise_2_preprocessing),
        ("Exercise 3: PSM Modes", exercise_3_psm_modes),
        ("Exercise 4: Confidence Scores", exercise_4_confidence),
        ("Exercise 5: Invoice Extraction", exercise_5_invoice_extraction),
        ("Exercise 6: Multilingual", exercise_6_multilingual),
        ("Bonus: Performance", bonus_performance_test),
    ]
    
    print("\nAvailable exercises:")
    for i, (name, _) in enumerate(exercises, 1):
        print(f"  {i}. {name}")
    
    print("\nRunning all exercises...")
    print("(Update image paths in each function before running)\n")
    
    for name, func in exercises:
        print("\n" + "=" * 80)
        try:
            func()
        except Exception as e:
            print(f"❌ Exercise failed: {e}")
    
    print("\n" + "=" * 80)
    print("✅ ALL EXERCISES COMPLETE!")
    print("=" * 80)
    
    print("\n📚 Next Steps:")
    print("  1. Download sample images from Google (invoices, receipts, documents)")
    print("  2. Run each exercise with different images")
    print("  3. Experiment with preprocessing parameters")
    print("  4. Compare PSM modes for your specific use case")
    print("  5. Build a mini-project: Receipt scanner or Document digitizer")
    
    print("\n💡 Tips:")
    print("  - Higher contrast = better OCR")
    print("  - Remove noise and blur for accuracy")
    print("  - Choose PSM based on document layout")
    print("  - Test multiple preprocessing combinations")
    print("  - Always check confidence scores")


if __name__ == "__main__":
    main()


"""
==========================================
CHEAT SHEET: TESSERACT BEST PRACTICES
==========================================

1️⃣ PREPROCESSING
   ✓ Convert to grayscale
   ✓ Increase contrast
   ✓ Apply thresholding (adaptive is better)
   ✓ Remove noise (fastNlMeansDenoising)
   ✓ Sharpen if text is blurry

2️⃣ PSM MODES (--psm)
   PSM 3:  Default, fully automatic
   PSM 4:  Single column of text
   PSM 6:  Single uniform block (good for invoices)
   PSM 7:  Single text line
   PSM 11: Sparse text (find as much as possible)
   PSM 13: Raw line (skip layout analysis)

3️⃣ LANGUAGE (-l)
   Always specify: -l eng (or chi_sim, fra, etc.)
   Install more: brew install tesseract-lang

4️⃣ CONFIDENCE
   - Get confidence: image_to_data()
   - Filter low confidence (< 60%)
   - Reprocess problem areas

5️⃣ PERFORMANCE
   - Resize large images (max 1920x1080)
   - Use grayscale (3x faster)
   - Choose appropriate PSM
   - Cache preprocessed images

==========================================
"""
