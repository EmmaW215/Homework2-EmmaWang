from PIL import Image
import pytesseract #pip install pytesseract first
import sys
import os

# Automatically configure TESSDATA_PREFIX if not set
# Common locations for macOS (Homebrew installation)
tessdata_locations = [
    '/opt/homebrew/share/tessdata',
    '/usr/local/share/tessdata',
    '/usr/share/tessdata'
]

if not os.environ.get('TESSDATA_PREFIX'):
    for location in tessdata_locations:
        if os.path.exists(location):
            os.environ['TESSDATA_PREFIX'] = location
            print(f"Auto-configured TESSDATA_PREFIX: {location}")
            break
    
    # If still not set, try to find it from tesseract installation
    if not os.environ.get('TESSDATA_PREFIX'):
        try:
            import shutil
            tesseract_path = shutil.which('tesseract')
            if tesseract_path:
                # Tesseract is typically at /opt/homebrew/bin/tesseract
                # tessdata is typically at /opt/homebrew/share/tessdata
                potential_tessdata = os.path.join(os.path.dirname(os.path.dirname(tesseract_path)), 'share', 'tessdata')
                if os.path.exists(potential_tessdata):
                    os.environ['TESSDATA_PREFIX'] = potential_tessdata
                    print(f"Auto-configured TESSDATA_PREFIX: {potential_tessdata}")
        except Exception:
            pass

# Parse command line arguments
# Usage: python HW1_Tesseract.py [image_path] [--lang language]
image_path = 'image.png'
language = 'eng'  # Default to English

if len(sys.argv) > 1:
    if sys.argv[1].startswith('--lang'):
        if '=' in sys.argv[1]:
            language = sys.argv[1].split('=')[1]
        elif len(sys.argv) > 2:
            language = sys.argv[2]
    else:
        image_path = sys.argv[1]
        if len(sys.argv) > 2 and sys.argv[2].startswith('--lang'):
            if '=' in sys.argv[2]:
                language = sys.argv[2].split('=')[1]
            elif len(sys.argv) > 3:
                language = sys.argv[3]

# Check if image file exists
if not os.path.exists(image_path):
    print(f"Error: Image file '{image_path}' not found!")
    print(f"Please provide an image file path as an argument, e.g.:")
    print(f"  python {sys.argv[0]} /path/to/your/image.png")
    print(f"\nOr place an image file named 'image.png' in the current directory.")
    sys.exit(1)

# Load an image using Pillow (PIL)
try:
    image = Image.open(image_path)
    print(f"Successfully loaded image: {image_path}")
    print(f"Image size: {image.size}")
    
    # Perform OCR on the image
    print(f"\nPerforming OCR with language: {language}...")
    text = pytesseract.image_to_string(image, lang=language)
    
    print("\nExtracted text:")
    print("=" * 50)
    print(text)
    print("=" * 50)
    
except Exception as e:
    print(f"Error processing image: {e}")
    sys.exit(1)