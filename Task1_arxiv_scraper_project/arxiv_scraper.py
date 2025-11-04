#!/usr/bin/env python3
"""
arXiv Paper Abstract Scraper - Task #1
Fetches latest 200 papers from cs.CL category, extracts abstracts using Trafilatura + Tesseract OCR
"""

import arxiv
import requests
import json
import logging
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from bs4 import BeautifulSoup
import trafilatura
from PIL import Image
from io import BytesIO
import pytesseract

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ArxivScraper:
    """
    Professional arXiv scraper with Trafilatura + Tesseract OCR fallback
    """
    
    def __init__(self, output_dir: str = "data/json", screenshot_dir: str = "data/screenshots"):
        self.output_dir = Path(output_dir)
        self.screenshot_dir = Path(screenshot_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)
        
        self.papers = []
        self.failed_papers = []
        
        # Rate limiting
        self.request_delay = 1.0  # seconds between requests
        
    def fetch_papers_from_arxiv(self, category: str = "cs.CL", max_results: int = 200) -> List[arxiv.Result]:
        """
        Fetch papers using arxiv API
        
        Args:
            category: arXiv category (default: cs.CL - Computation and Language)
            max_results: Number of papers to fetch
            
        Returns:
            List of arxiv.Result objects
        """
        logger.info(f"Fetching {max_results} papers from category: {category}")
        
        # Create search query
        search = arxiv.Search(
            query=f"cat:{category}",
            max_results=max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending
        )
        
        results = []
        try:
            for result in search.results():
                results.append(result)
                logger.info(f"Fetched: {result.title[:50]}...")
                
        except Exception as e:
            logger.error(f"Error fetching papers: {e}")
            
        logger.info(f"Successfully fetched {len(results)} papers")
        return results
    
    def extract_abstract_with_trafilatura(self, url: str) -> Optional[str]:
        """
        Extract abstract using Trafilatura for clean text extraction
        
        Args:
            url: Paper abstract URL
            
        Returns:
            Cleaned abstract text or None
        """
        try:
            # Fetch HTML content
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            html_content = response.text
            
            # Extract clean text using Trafilatura
            extracted = trafilatura.extract(
                html_content,
                include_comments=False,
                include_tables=False,
                no_fallback=False
            )
            
            if extracted:
                logger.info(f"✓ Trafilatura extracted text from {url}")
                return extracted.strip()
            else:
                logger.warning(f"✗ Trafilatura failed for {url}")
                return None
                
        except Exception as e:
            logger.error(f"Error in Trafilatura extraction: {e}")
            return None
    
    def extract_abstract_with_beautifulsoup(self, url: str) -> Optional[str]:
        """
        Fallback: Extract abstract using BeautifulSoup
        
        Args:
            url: Paper abstract URL
            
        Returns:
            Abstract text or None
        """
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'lxml')
            
            # arXiv abstract is in <blockquote> with class "abstract mathjax"
            abstract_block = soup.find('blockquote', class_='abstract')
            
            if abstract_block:
                # Remove "Abstract:" label
                abstract_text = abstract_block.get_text(strip=True)
                if abstract_text.startswith('Abstract:'):
                    abstract_text = abstract_text[9:].strip()
                    
                logger.info(f"✓ BeautifulSoup extracted abstract from {url}")
                return abstract_text
            else:
                logger.warning(f"✗ BeautifulSoup couldn't find abstract in {url}")
                return None
                
        except Exception as e:
            logger.error(f"Error in BeautifulSoup extraction: {e}")
            return None
    
    def extract_abstract_with_ocr(self, url: str, paper_id: str) -> Optional[str]:
        """
        Last resort: Screenshot + Tesseract OCR
        
        Args:
            url: Paper abstract URL
            paper_id: Unique paper identifier for filename
            
        Returns:
            OCR extracted text or None
        """
        try:
            # For OCR, we'd normally use Selenium/Playwright to take screenshots
            # For this implementation, we'll simulate with a simpler approach
            # using requests + PIL (in real production, use browser automation)
            
            logger.info(f"Attempting OCR extraction for {url}")
            
            # In a real scenario, you'd use:
            # 1. Selenium/Playwright to render the page
            # 2. Take screenshot
            # 3. Run Tesseract on screenshot
            
            # Simplified version: try to get any image from the page
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Find abstract block and try OCR on any embedded images
            abstract_block = soup.find('blockquote', class_='abstract')
            if abstract_block:
                # If there are images in abstract (rare), process them
                images = abstract_block.find_all('img')
                
                ocr_texts = []
                for img in images:
                    img_url = img.get('src')
                    if img_url:
                        if not img_url.startswith('http'):
                            img_url = f"https://arxiv.org{img_url}"
                        
                        try:
                            img_response = requests.get(img_url, timeout=5)
                            image = Image.open(BytesIO(img_response.content))
                            
                            # Apply OCR
                            ocr_text = pytesseract.image_to_string(
                                image,
                                config='--psm 6'  # Assume uniform text block
                            )
                            ocr_texts.append(ocr_text.strip())
                            
                        except Exception as e:
                            logger.error(f"Failed to OCR image {img_url}: {e}")
                            continue
                
                if ocr_texts:
                    logger.info(f"✓ OCR extracted text from {len(ocr_texts)} images")
                    return " ".join(ocr_texts)
            
            logger.warning(f"✗ OCR found no processable content in {url}")
            return None
            
        except Exception as e:
            logger.error(f"Error in OCR extraction: {e}")
            return None
    
    def process_paper(self, paper: arxiv.Result) -> Dict:
        """
        Process a single paper through extraction pipeline
        
        Pipeline: Trafilatura → BeautifulSoup → OCR
        
        Args:
            paper: arxiv.Result object
            
        Returns:
            Dictionary with paper data
        """
        paper_id = paper.entry_id.split('/')[-1]
        abs_url = f"https://arxiv.org/abs/{paper_id}"
        
        logger.info(f"\n{'='*80}")
        logger.info(f"Processing: {paper.title}")
        logger.info(f"URL: {abs_url}")
        logger.info(f"{'='*80}")
        
        # Try extraction methods in order
        abstract = None
        extraction_method = None
        
        # Method 1: Use abstract from API (most reliable)
        if paper.summary:
            abstract = paper.summary.strip()
            extraction_method = "arxiv_api"
            logger.info("✓ Used abstract from arXiv API")
        
        # Method 2: Trafilatura
        if not abstract:
            abstract = self.extract_abstract_with_trafilatura(abs_url)
            if abstract:
                extraction_method = "trafilatura"
        
        # Method 3: BeautifulSoup
        if not abstract:
            time.sleep(self.request_delay)
            abstract = self.extract_abstract_with_beautifulsoup(abs_url)
            if abstract:
                extraction_method = "beautifulsoup"
        
        # Method 4: OCR (last resort)
        if not abstract:
            time.sleep(self.request_delay)
            abstract = self.extract_abstract_with_ocr(abs_url, paper_id)
            if abstract:
                extraction_method = "tesseract_ocr"
        
        # Build result
        result = {
            "url": abs_url,
            "title": paper.title,
            "abstract": abstract if abstract else "EXTRACTION_FAILED",
            "authors": [author.name for author in paper.authors],
            "date": paper.published.strftime("%Y-%m-%d"),
            "extraction_method": extraction_method if extraction_method else "failed",
            "arxiv_id": paper_id,
            "categories": paper.categories,
            "pdf_url": paper.pdf_url
        }
        
        if abstract:
            logger.info(f"✓ Successfully processed paper with {extraction_method}")
            self.papers.append(result)
        else:
            logger.error(f"✗ Failed to extract abstract for {paper_id}")
            self.failed_papers.append(result)
        
        # Rate limiting
        time.sleep(self.request_delay)
        
        return result
    
    def save_results(self, filename: str = "arxiv_clean.json"):
        """
        Save scraped papers to JSON file
        
        Args:
            filename: Output JSON filename
        """
        output_path = self.output_dir / filename
        
        # Prepare output data
        output_data = {
            "metadata": {
                "total_papers": len(self.papers) + len(self.failed_papers),
                "successful": len(self.papers),
                "failed": len(self.failed_papers),
                "timestamp": datetime.now().isoformat(),
                "category": "cs.CL"
            },
            "papers": self.papers
        }
        
        # Save to JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        # Check file size
        file_size_mb = output_path.stat().st_size / (1024 * 1024)
        
        logger.info(f"\n{'='*80}")
        logger.info(f"✓ Results saved to: {output_path}")
        logger.info(f"✓ File size: {file_size_mb:.2f} MB")
        logger.info(f"✓ Total papers: {len(self.papers)}")
        logger.info(f"✗ Failed papers: {len(self.failed_papers)}")
        logger.info(f"{'='*80}\n")
        
        # Save failed papers separately for debugging
        if self.failed_papers:
            failed_path = self.output_dir / "failed_papers.json"
            with open(failed_path, 'w', encoding='utf-8') as f:
                json.dump(self.failed_papers, f, indent=2, ensure_ascii=False)
            logger.info(f"Failed papers saved to: {failed_path}")
    
    def run(self, category: str = "cs.CL", max_results: int = 200):
        """
        Main execution pipeline
        
        Args:
            category: arXiv category
            max_results: Number of papers to scrape
        """
        logger.info("Starting arXiv scraper...")
        start_time = time.time()
        
        # Step 1: Fetch papers from arXiv API
        arxiv_papers = self.fetch_papers_from_arxiv(category, max_results)
        
        # Step 2: Process each paper
        for i, paper in enumerate(arxiv_papers, 1):
            logger.info(f"\n[{i}/{len(arxiv_papers)}] Processing paper...")
            self.process_paper(paper)
        
        # Step 3: Save results
        self.save_results()
        
        # Summary
        elapsed_time = time.time() - start_time
        logger.info(f"\n{'='*80}")
        logger.info(f"SCRAPING COMPLETE!")
        logger.info(f"Total time: {elapsed_time/60:.2f} minutes")
        if len(arxiv_papers) > 0:
            logger.info(f"Average time per paper: {elapsed_time/len(arxiv_papers):.2f} seconds")
        logger.info(f"{'='*80}\n")


def main():
    """Main entry point"""
    # Create scraper instance
    scraper = ArxivScraper()
    
    # Run scraping
    scraper.run(category="cs.CL", max_results=200)


if __name__ == "__main__":
    main()
