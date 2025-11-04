#!/usr/bin/env python3
"""
Task #2: Batch OCR for arXiv PDFs
Converts PDFs from Task #1 to text using pdf2image + Tesseract OCR
"""

import json
import logging
import time
import os
from pathlib import Path
from typing import Dict, List, Optional
import requests
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
from datetime import datetime
import hashlib

# Create logs directory if it doesn't exist
Path('logs').mkdir(parents=True, exist_ok=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/pdf_ocr.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class PDFToTextOCR:
    """
    Professional PDF to Text OCR converter using Tesseract
    """
    
    def __init__(
        self,
        task1_json: str = "../arxiv_scraper_project/data/json/arxiv_clean.json",
        pdf_dir: str = "pdfs",
        output_dir: str = "pdf_ocr",
        max_papers: Optional[int] = None
    ):
        """
        Initialize PDF OCR converter
        
        Args:
            task1_json: Path to Task #1 output JSON
            pdf_dir: Directory to download PDFs
            output_dir: Directory for OCR text output
            max_papers: Limit number of papers to process (None = all)
        """
        self.task1_json = Path(task1_json)
        self.pdf_dir = Path(pdf_dir)
        self.output_dir = Path(output_dir)
        self.max_papers = max_papers
        
        # Create directories
        self.pdf_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Stats
        self.stats = {
            "total_papers": 0,
            "downloaded": 0,
            "ocr_completed": 0,
            "failed_downloads": 0,
            "failed_ocr": 0,
            "total_pages": 0,
            "skipped_existing": 0
        }
        
        # Resume tracking
        self.processed_ids = set()
        self._load_processed_ids()
        
    def _load_processed_ids(self):
        """Load already processed paper IDs for resume capability"""
        for txt_file in self.output_dir.glob("*.txt"):
            # Extract arxiv_id from filename (format: arxiv_XXXXX.txt)
            arxiv_id = txt_file.stem.replace("arxiv_", "")
            self.processed_ids.add(arxiv_id)
        
        if self.processed_ids:
            logger.info(f"Found {len(self.processed_ids)} already processed papers")
    
    def load_task1_data(self) -> List[Dict]:
        """
        Load papers from Task #1 JSON output
        
        Returns:
            List of paper dictionaries
        """
        logger.info(f"Loading Task #1 data from: {self.task1_json}")
        
        if not self.task1_json.exists():
            raise FileNotFoundError(
                f"Task #1 JSON not found: {self.task1_json}\n"
                f"Please run Task #1 first or update the path!"
            )
        
        with open(self.task1_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        papers = data.get('papers', [])
        logger.info(f"Loaded {len(papers)} papers from Task #1")
        
        if self.max_papers:
            papers = papers[:self.max_papers]
            logger.info(f"Limited to first {self.max_papers} papers")
        
        self.stats["total_papers"] = len(papers)
        return papers
    
    def download_pdf(self, pdf_url: str, arxiv_id: str) -> Optional[Path]:
        """
        Download PDF from arXiv
        
        Args:
            pdf_url: URL of the PDF
            arxiv_id: arXiv paper ID
            
        Returns:
            Path to downloaded PDF or None if failed
        """
        pdf_path = self.pdf_dir / f"arxiv_{arxiv_id}.pdf"
        
        # Skip if already downloaded
        if pdf_path.exists():
            logger.info(f"  ✓ PDF already exists: {pdf_path.name}")
            return pdf_path
        
        try:
            logger.info(f"  Downloading PDF from: {pdf_url}")
            response = requests.get(pdf_url, timeout=30, stream=True)
            response.raise_for_status()
            
            # Save PDF
            with open(pdf_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            file_size_mb = pdf_path.stat().st_size / (1024 * 1024)
            logger.info(f"  ✓ Downloaded: {pdf_path.name} ({file_size_mb:.2f} MB)")
            self.stats["downloaded"] += 1
            
            return pdf_path
            
        except Exception as e:
            logger.error(f"  ✗ Failed to download PDF: {e}")
            self.stats["failed_downloads"] += 1
            return None
    
    def pdf_to_images(self, pdf_path: Path, dpi: int = 300) -> List[Image.Image]:
        """
        Convert PDF pages to images
        
        Args:
            pdf_path: Path to PDF file
            dpi: Resolution for image conversion (higher = better quality)
            
        Returns:
            List of PIL Image objects
        """
        try:
            logger.info(f"  Converting PDF to images (DPI={dpi})...")
            
            images = convert_from_path(
                pdf_path,
                dpi=dpi,
                fmt='png',
                thread_count=4  # Use multiple threads
            )
            
            logger.info(f"  ✓ Converted {len(images)} pages to images")
            self.stats["total_pages"] += len(images)
            
            return images
            
        except Exception as e:
            logger.error(f"  ✗ Failed to convert PDF to images: {e}")
            return []
    
    def ocr_image(
        self,
        image: Image.Image,
        page_num: int,
        preserve_layout: bool = True
    ) -> str:
        """
        Extract text from image using Tesseract OCR
        
        Args:
            image: PIL Image object
            page_num: Page number (for logging)
            preserve_layout: Whether to preserve document layout
            
        Returns:
            Extracted text
        """
        try:
            # Configure Tesseract
            # PSM 1 = Automatic page segmentation with OSD (Orientation and Script Detection)
            # PSM 3 = Fully automatic page segmentation, but no OSD
            # PSM 6 = Assume a single uniform block of text
            
            if preserve_layout:
                config = '--psm 1'  # Best for preserving layout
            else:
                config = '--psm 3'  # Fast, good for simple docs
            
            # Extract text
            text = pytesseract.image_to_string(image, config=config)
            
            logger.info(f"    Page {page_num}: Extracted {len(text)} characters")
            return text
            
        except Exception as e:
            logger.error(f"    ✗ OCR failed for page {page_num}: {e}")
            return ""
    
    def process_pdf(
        self,
        paper: Dict,
        preserve_layout: bool = True,
        dpi: int = 300
    ) -> bool:
        """
        Complete pipeline: Download PDF → Convert to images → OCR → Save text
        
        Args:
            paper: Paper dictionary from Task #1
            preserve_layout: Whether to preserve document layout
            dpi: Image resolution for OCR
            
        Returns:
            True if successful, False otherwise
        """
        arxiv_id = paper.get('arxiv_id', 'unknown')
        pdf_url = paper.get('pdf_url')
        title = paper.get('title', 'Unknown')
        
        logger.info(f"\n{'='*80}")
        logger.info(f"Processing: {title[:60]}...")
        logger.info(f"arXiv ID: {arxiv_id}")
        logger.info(f"{'='*80}")
        
        # Check if already processed
        if arxiv_id in self.processed_ids:
            logger.info(f"  ⊙ Already processed, skipping...")
            self.stats["skipped_existing"] += 1
            return True
        
        if not pdf_url:
            logger.error(f"  ✗ No PDF URL found")
            self.stats["failed_downloads"] += 1
            return False
        
        # Step 1: Download PDF
        pdf_path = self.download_pdf(pdf_url, arxiv_id)
        if not pdf_path:
            return False
        
        # Step 2: Convert PDF to images
        images = self.pdf_to_images(pdf_path, dpi=dpi)
        if not images:
            self.stats["failed_ocr"] += 1
            return False
        
        # Step 3: OCR each page
        logger.info(f"  Running OCR on {len(images)} pages...")
        all_text = []
        
        for i, image in enumerate(images, 1):
            page_text = self.ocr_image(image, i, preserve_layout)
            if page_text:
                # Add page separator
                all_text.append(f"\n{'='*80}\n")
                all_text.append(f"PAGE {i}\n")
                all_text.append(f"{'='*80}\n\n")
                all_text.append(page_text)
        
        # Step 4: Save to text file
        output_file = self.output_dir / f"arxiv_{arxiv_id}.txt"
        full_text = "".join(all_text)
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                # Write metadata header
                f.write(f"arXiv ID: {arxiv_id}\n")
                f.write(f"Title: {title}\n")
                f.write(f"PDF URL: {pdf_url}\n")
                f.write(f"Date Processed: {datetime.now().isoformat()}\n")
                f.write(f"Total Pages: {len(images)}\n")
                f.write(f"Total Characters: {len(full_text)}\n")
                f.write(f"\n{'='*80}\n")
                f.write(f"EXTRACTED TEXT\n")
                f.write(f"{'='*80}\n\n")
                f.write(full_text)
            
            logger.info(f"  ✓ Saved OCR text: {output_file.name}")
            logger.info(f"  ✓ Total characters extracted: {len(full_text)}")
            
            self.stats["ocr_completed"] += 1
            self.processed_ids.add(arxiv_id)
            
            return True
            
        except Exception as e:
            logger.error(f"  ✗ Failed to save text file: {e}")
            self.stats["failed_ocr"] += 1
            return False
    
    def run(
        self,
        preserve_layout: bool = True,
        dpi: int = 300,
        delay_between_papers: float = 2.0
    ):
        """
        Main execution pipeline
        
        Args:
            preserve_layout: Whether to preserve document layout
            dpi: Image resolution for OCR (300 recommended)
            delay_between_papers: Delay between processing papers (seconds)
        """
        logger.info("="*80)
        logger.info("STARTING TASK #2: PDF TO TEXT OCR")
        logger.info("="*80)
        
        start_time = time.time()
        
        # Load papers from Task #1
        papers = self.load_task1_data()
        
        # Process each paper
        for i, paper in enumerate(papers, 1):
            logger.info(f"\n[{i}/{len(papers)}] Starting paper processing...")
            
            success = self.process_pdf(paper, preserve_layout, dpi)
            
            # Rate limiting
            if i < len(papers):  # Don't sleep after last paper
                time.sleep(delay_between_papers)
        
        # Final summary
        elapsed_time = time.time() - start_time
        self._print_summary(elapsed_time)
        
        # Save processing report
        self._save_report()
    
    def _print_summary(self, elapsed_time: float):
        """Print execution summary"""
        logger.info("\n" + "="*80)
        logger.info("TASK #2 COMPLETE!")
        logger.info("="*80)
        logger.info(f"Total papers: {self.stats['total_papers']}")
        logger.info(f"Successfully processed: {self.stats['ocr_completed']}")
        logger.info(f"Skipped (already done): {self.stats['skipped_existing']}")
        logger.info(f"Failed downloads: {self.stats['failed_downloads']}")
        logger.info(f"Failed OCR: {self.stats['failed_ocr']}")
        logger.info(f"Total pages processed: {self.stats['total_pages']}")
        logger.info(f"Total time: {elapsed_time/60:.2f} minutes")
        if self.stats['ocr_completed'] > 0:
            logger.info(f"Average time per paper: {elapsed_time/self.stats['ocr_completed']:.2f} seconds")
        logger.info("="*80 + "\n")
    
    def _save_report(self):
        """Save processing report"""
        report_path = Path("logs/task2_report.json")
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "statistics": self.stats,
            "output_directory": str(self.output_dir),
            "processed_papers": list(self.processed_ids)
        }
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Report saved: {report_path}")


def main():
    """Main entry point"""
    
    # Configuration
    TASK1_JSON = "../arxiv_scraper_project/data/json/arxiv_clean.json"
    MAX_PAPERS = None  # Set to 10 for testing, None for all papers
    PRESERVE_LAYOUT = True  # Preserve document layout
    DPI = 300  # Image resolution (higher = better quality, slower)
    DELAY = 2.0  # Seconds between papers
    
    # Create converter
    converter = PDFToTextOCR(
        task1_json=TASK1_JSON,
        max_papers=MAX_PAPERS
    )
    
    # Run conversion
    converter.run(
        preserve_layout=PRESERVE_LAYOUT,
        dpi=DPI,
        delay_between_papers=DELAY
    )


if __name__ == "__main__":
    main()
