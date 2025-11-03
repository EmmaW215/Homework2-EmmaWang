"""
Tesseract OCR Best Practices Tutorial
Author: Emma Wang
Purpose: Learn Tesseract OCR with preprocessing, PSM modes, and optimization
"""

import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import cv2
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, Tuple
import os


class TesseractBestPractices:
    """
    Comprehensive Tesseract OCR class demonstrating best practices
    """
    
    def __init__(self):
        """Initialize with Tesseract configuration"""
        # Verify Tesseract installation
        try:
            pytesseract.get_tesseract_version()
            print("✅ Tesseract is installed and working!")
        except Exception as e:
            print(f"❌ Tesseract not found: {e}")
            print("Install: brew install tesseract (macOS) or apt-get install tesseract-ocr (Linux)")
    
    # ==================== SECTION 1: IMAGE PREPROCESSING ====================
    
    def preprocess_image(self, image_path: str, method: str = 'all') -> np.ndarray:
        """
        Preprocess image to improve OCR accuracy
        
        Args:
            image_path: Path to input image
            method: Preprocessing method ('grayscale', 'threshold', 'denoise', 'all')
        
        Returns:
            Preprocessed image as numpy array
        """
        print(f"\n{'='*60}")
        print(f"PREPROCESSING: {method.upper()}")
        print(f"{'='*60}")
        
        # Load image with OpenCV
        img = cv2.imread(image_path)
        
        if img is None:
            raise FileNotFoundError(f"Cannot load image: {image_path}")
        
        print(f"Original image shape: {img.shape}")
        
        # Always convert to grayscale first for processing
        if len(img.shape) == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            if method == 'grayscale':
                print("✓ Converted to grayscale")
        
        if method == 'threshold' or method == 'all':
            # Apply adaptive thresholding (better than simple threshold)
            img = cv2.adaptiveThreshold(
                img, 255, 
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                cv2.THRESH_BINARY, 
                11, 2
            )
            print("✓ Applied adaptive thresholding")
        
        if method == 'denoise' or method == 'all':
            # Denoise using Non-local Means Denoising
            img = cv2.fastNlMeansDenoising(img, None, 10, 7, 21)
            print("✓ Applied denoising")
        
        return img
    
    def enhance_image(self, image_path: str) -> Image:
        """
        Enhance image using PIL (brightness, contrast, sharpness)
        
        Args:
            image_path: Path to input image
        
        Returns:
            Enhanced PIL Image
        """
        print(f"\n{'='*60}")
        print("IMAGE ENHANCEMENT")
        print(f"{'='*60}")
        
        img = Image.open(image_path)
        
        # Increase contrast
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2.0)  # Increase contrast by 2x
        print("✓ Enhanced contrast (2.0x)")
        
        # Increase sharpness
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(1.5)
        print("✓ Enhanced sharpness (1.5x)")
        
        # Adjust brightness if needed
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.2)
        print("✓ Enhanced brightness (1.2x)")
        
        return img
    
    def visualize_preprocessing(self, image_path: str):
        """
        Visualize different preprocessing steps
        """
        original = cv2.imread(image_path)
        original_rgb = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
        
        grayscale = self.preprocess_image(image_path, 'grayscale')
        threshold = self.preprocess_image(image_path, 'threshold')
        denoised = self.preprocess_image(image_path, 'denoise')
        full_preprocess = self.preprocess_image(image_path, 'all')
        
        # Create visualization
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        fig.suptitle('Image Preprocessing Comparison', fontsize=16)
        
        images = [
            (original_rgb, 'Original'),
            (grayscale, 'Grayscale'),
            (threshold, 'Adaptive Threshold'),
            (denoised, 'Denoised'),
            (full_preprocess, 'Full Preprocessing'),
        ]
        
        for idx, (img, title) in enumerate(images):
            row, col = idx // 3, idx % 3
            axes[row, col].imshow(img, cmap='gray' if len(img.shape) == 2 else None)
            axes[row, col].set_title(title)
            axes[row, col].axis('off')
        
        # Hide the last subplot
        axes[1, 2].axis('off')
        
        plt.tight_layout()
        output_path = os.path.join(os.path.dirname(__file__), 'preprocessing_comparison.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"\n✅ Visualization saved to '{output_path}'")
        plt.close()
    
    # ==================== SECTION 2: PSM MODES ====================
    
    def demonstrate_psm_modes(self, image_path: str):
        """
        Demonstrate different Page Segmentation Modes
        
        PSM Modes:
        0  = Orientation and script detection only
        1  = Automatic page segmentation with OSD
        3  = Fully automatic page segmentation (default)
        4  = Single column of text
        6  = Single uniform block of text
        7  = Single text line
        8  = Single word
        10 = Single character
        11 = Sparse text (find as much text as possible)
        13 = Raw line (bypass all Tesseract layout analysis)
        """
        print(f"\n{'='*60}")
        print("PSM MODE COMPARISON")
        print(f"{'='*60}")
        
        # Preprocess image first
        img = self.preprocess_image(image_path, 'all')
        
        # Test different PSM modes
        psm_modes = {
            3: "Fully automatic (Default)",
            4: "Single column",
            6: "Single uniform block",
            7: "Single text line",
            11: "Sparse text",
            13: "Raw line"
        }
        
        results = {}
        
        for psm, description in psm_modes.items():
            try:
                # Configure Tesseract with specific PSM
                custom_config = f'--psm {psm}'
                text = pytesseract.image_to_string(img, config=custom_config)
                results[psm] = text.strip()
                
                print(f"\nPSM {psm}: {description}")
                print(f"Text length: {len(text)} characters")
                print(f"Preview: {text[:100]}..." if len(text) > 100 else f"Text: {text}")
                
            except Exception as e:
                print(f"PSM {psm} failed: {e}")
        
        return results
    
    def get_detailed_info(self, image_path: str, psm: int = 3):
        """
        Get detailed OCR information including bounding boxes and confidence
        
        Args:
            image_path: Path to image
            psm: Page segmentation mode
        """
        print(f"\n{'='*60}")
        print(f"DETAILED OCR ANALYSIS (PSM={psm})")
        print(f"{'='*60}")
        
        img = self.preprocess_image(image_path, 'all')
        custom_config = f'--psm {psm}'
        
        # Get detailed data
        data = pytesseract.image_to_data(img, config=custom_config, output_type=pytesseract.Output.DICT)
        
        # Filter out empty detections
        n_boxes = len(data['text'])
        valid_detections = []
        
        for i in range(n_boxes):
            if int(data['conf'][i]) > 60:  # Only high confidence (>60%)
                text = data['text'][i].strip()
                if text:  # Not empty
                    valid_detections.append({
                        'text': text,
                        'confidence': data['conf'][i],
                        'left': data['left'][i],
                        'top': data['top'][i],
                        'width': data['width'][i],
                        'height': data['height'][i]
                    })
        
        print(f"\nTotal detections: {n_boxes}")
        print(f"Valid detections (conf > 60%): {len(valid_detections)}")
        
        # Show top 10 detections
        print("\nTop 10 detected words:")
        print(f"{'Text':<20} {'Confidence':<12} {'Position (x,y)'}")
        print("-" * 60)
        
        for det in valid_detections[:10]:
            print(f"{det['text']:<20} {det['confidence']:<12.1f} ({det['left']}, {det['top']})")
        
        return valid_detections
    
    def draw_bounding_boxes(self, image_path: str, psm: int = 3):
        """
        Draw bounding boxes on detected text
        """
        img = cv2.imread(image_path)
        img_data = img.copy()
        
        # Get detections
        gray = self.preprocess_image(image_path, 'grayscale')
        custom_config = f'--psm {psm}'
        data = pytesseract.image_to_data(gray, config=custom_config, output_type=pytesseract.Output.DICT)
        
        n_boxes = len(data['text'])
        for i in range(n_boxes):
            if int(data['conf'][i]) > 60:  # High confidence
                (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
                
                # Draw rectangle
                cv2.rectangle(img_data, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
                # Add confidence score
                conf_text = f"{data['conf'][i]:.1f}%"
                cv2.putText(img_data, conf_text, (x, y - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
        
        # Save result
        output_path = os.path.join(os.path.dirname(__file__), 'bounding_boxes.png')
        cv2.imwrite(output_path, img_data)
        print(f"\n✅ Bounding boxes saved to '{output_path}'")
        
        return img_data
    
    # ==================== SECTION 3: LANGUAGE SUPPORT ====================
    
    def list_available_languages(self):
        """
        List all installed Tesseract languages
        """
        print(f"\n{'='*60}")
        print("AVAILABLE LANGUAGES")
        print(f"{'='*60}")
        
        try:
            langs = pytesseract.get_languages()
            print(f"\nTotal languages installed: {len(langs)}")
            print("\nLanguage codes:")
            for i, lang in enumerate(sorted(langs), 1):
                print(f"  {i:2d}. {lang}")
            
            return langs
        except Exception as e:
            print(f"Error getting languages: {e}")
            return []
    
    def ocr_with_language(self, image_path: str, lang: str = 'eng', psm: int = 3):
        """
        Perform OCR with specific language
        
        Args:
            image_path: Path to image
            lang: Language code (e.g., 'eng', 'chi_sim', 'fra')
            psm: Page segmentation mode
        """
        print(f"\n{'='*60}")
        print(f"OCR WITH LANGUAGE: {lang.upper()}")
        print(f"{'='*60}")
        
        img = self.preprocess_image(image_path, 'all')
        
        # Custom config with language and PSM
        custom_config = f'--psm {psm} -l {lang}'
        
        try:
            text = pytesseract.image_to_string(img, config=custom_config)
            print(f"\n✅ Successfully extracted text in '{lang}'")
            print(f"Text length: {len(text)} characters")
            print(f"\nExtracted text:\n{'-'*60}")
            print(text)
            print('-'*60)
            
            return text
        except Exception as e:
            print(f"❌ Error with language '{lang}': {e}")
            print(f"Tip: Install language data with: brew install tesseract-lang")
            return None
    
    # ==================== SECTION 4: PRACTICAL EXAMPLES ====================
    
    def ocr_invoice(self, image_path: str):
        """
        Example: Extract structured data from invoice
        """
        print(f"\n{'='*60}")
        print("INVOICE OCR EXAMPLE")
        print(f"{'='*60}")
        
        # Best settings for invoices: PSM 6 (single block)
        img = self.preprocess_image(image_path, 'all')
        custom_config = '--psm 6'
        
        text = pytesseract.image_to_string(img, config=custom_config)
        
        # Extract structured information
        import re
        
        invoice_data = {
            'total': None,
            'date': None,
            'invoice_number': None
        }
        
        # Find total amount (e.g., $123.45, €123.45)
        total_pattern = r'(?:Total|Amount)[\s:]*[\$€£]?([\d,]+\.?\d*)'
        total_match = re.search(total_pattern, text, re.IGNORECASE)
        if total_match:
            invoice_data['total'] = total_match.group(1)
        
        # Find date (various formats)
        date_pattern = r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}'
        date_match = re.search(date_pattern, text)
        if date_match:
            invoice_data['date'] = date_match.group(0)
        
        # Find invoice number
        inv_pattern = r'Invoice[#\s:]*(\w+)'
        inv_match = re.search(inv_pattern, text, re.IGNORECASE)
        if inv_match:
            invoice_data['invoice_number'] = inv_match.group(1)
        
        print(f"\nExtracted invoice data:")
        for key, value in invoice_data.items():
            print(f"  {key}: {value if value else 'Not found'}")
        
        return invoice_data
    
    def ocr_table(self, image_path: str):
        """
        Example: Extract table data with proper structure
        """
        print(f"\n{'='*60}")
        print("TABLE OCR EXAMPLE")
        print(f"{'='*60}")
        
        # Best settings for tables: PSM 6 with preserve_interword_spaces
        img = self.preprocess_image(image_path, 'all')
        custom_config = '--psm 6 preserve_interword_spaces=1'
        
        text = pytesseract.image_to_string(img, config=custom_config)
        
        # Parse table (simple row-based approach)
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        print(f"\nDetected {len(lines)} table rows:")
        for i, line in enumerate(lines, 1):
            print(f"  Row {i}: {line}")
        
        return lines
    
    # ==================== SECTION 5: PERFORMANCE COMPARISON ====================
    
    def compare_methods(self, image_path: str):
        """
        Compare different preprocessing + PSM combinations
        """
        print(f"\n{'='*60}")
        print("PERFORMANCE COMPARISON")
        print(f"{'='*60}")
        
        import time
        
        # Test configurations
        configs = [
            ('No preprocessing', None, 3, ''),
            ('Grayscale only', 'grayscale', 3, ''),
            ('Full preprocessing', 'all', 3, ''),
            ('Full + PSM 6', 'all', 6, '--psm 6'),
            ('Full + PSM 11', 'all', 11, '--psm 11'),
        ]
        
        results = []
        
        for name, preprocess, psm, config in configs:
            start_time = time.time()
            
            # Load image
            if preprocess:
                img = self.preprocess_image(image_path, preprocess)
            else:
                img = cv2.imread(image_path)
            
            # Run OCR
            text = pytesseract.image_to_string(img, config=config if config else f'--psm {psm}')
            
            elapsed = time.time() - start_time
            
            results.append({
                'name': name,
                'time': elapsed,
                'length': len(text),
                'text_preview': text[:50].replace('\n', ' ')
            })
        
        # Display results
        print(f"\n{'Method':<25} {'Time (s)':<12} {'Chars':<10} {'Preview'}")
        print("-" * 80)
        for r in results:
            print(f"{r['name']:<25} {r['time']:<12.3f} {r['length']:<10} {r['text_preview']}")
        
        return results


# ==================== MAIN DEMONSTRATION ====================

def main():
    """
    Main demonstration of Tesseract best practices
    """
    print("=" * 80)
    print(" " * 20 + "TESSERACT OCR TUTORIAL")
    print(" " * 15 + "Best Practices & Practical Examples")
    print("=" * 80)
    
    # Initialize
    ocr = TesseractBestPractices()
    
    # Create a sample image for testing
    print("\n📝 Creating sample test image...")
    create_sample_image()
    
    # Use relative path from script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sample_image = os.path.join(script_dir, 'preprocessing_comparison.png')
    
    if not os.path.exists(sample_image):
        # Try using sample_text.png if preprocessing_comparison.png doesn't exist
        sample_image = os.path.join(script_dir, 'sample_text.png')
        if not os.path.exists(sample_image):
            print("❌ Sample image not found. Please provide your own image.")
            return
    
    # Section 1: Preprocessing
    print("\n" + "=" * 80)
    print("SECTION 1: IMAGE PREPROCESSING")
    print("=" * 80)
    
    ocr.visualize_preprocessing(sample_image)
    
    # Section 2: PSM Modes
    print("\n" + "=" * 80)
    print("SECTION 2: PAGE SEGMENTATION MODES (PSM)")
    print("=" * 80)
    
    ocr.demonstrate_psm_modes(sample_image)
    ocr.get_detailed_info(sample_image, psm=6)
    ocr.draw_bounding_boxes(sample_image, psm=6)
    
    # Section 3: Languages
    print("\n" + "=" * 80)
    print("SECTION 3: LANGUAGE SUPPORT")
    print("=" * 80)
    
    ocr.list_available_languages()
    ocr.ocr_with_language(sample_image, lang='eng', psm=6)
    
    # Section 4: Performance
    print("\n" + "=" * 80)
    print("SECTION 4: PERFORMANCE COMPARISON")
    print("=" * 80)
    
    ocr.compare_methods(sample_image)
    
    print("\n" + "=" * 80)
    print("✅ TUTORIAL COMPLETE!")
    print("=" * 80)
    print("\nGenerated files:")
    print("  - preprocessing_comparison.png")
    print("  - bounding_boxes.png")
    print("  - sample_text.png")
    print("\nNext steps:")
    print("  1. Try with your own images")
    print("  2. Experiment with different PSM modes")
    print("  3. Install additional language packs")
    print("  4. Fine-tune preprocessing parameters")


def create_sample_image():
    """
    Create a sample image for testing OCR
    """
    from PIL import Image, ImageDraw, ImageFont
    
    # Create a white background image
    width, height = 800, 400
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Sample text
    sample_text = """
    Machine Learning & AI
    
    This is a sample text for OCR testing.
    It contains multiple lines with different content.
    
    Numbers: 1234567890
    Special characters: @#$%^&*()
    
    Invoice #12345
    Date: 11/02/2025
    Total: $1,234.56
    """
    
    # Draw text
    try:
        # Try to use a nice font
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
    except:
        # Fall back to default font
        font = ImageFont.load_default()
    
    # Add some lines
    y_position = 30
    for line in sample_text.strip().split('\n'):
        draw.text((50, y_position), line, fill='black', font=font)
        y_position += 35
    
    # Save to the same directory as this script
    output_path = os.path.join(os.path.dirname(__file__), 'sample_text.png')
    img.save(output_path)
    print(f"✅ Sample image created: {output_path}")


if __name__ == "__main__":
    main()
