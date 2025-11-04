#!/usr/bin/env python3
"""
Task #4: Data Cleaning & Deduplication
End-to-end cleaner that merges Tasks 1-3 outputs and produces clean corpus
"""

import json
import re
import logging
from pathlib import Path
from typing import List, Dict, Set, Tuple
from collections import Counter, defaultdict
from datetime import datetime

# Import required libraries
from langdetect import detect, LangDetectException
from datasketch import MinHash, MinHashLSH
from bs4 import BeautifulSoup
import nltk
from nltk import ngrams

# Setup logging
Path('logs/cleaning').mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/cleaning/data_cleaning.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class DataCleaner:
    """
    End-to-end data cleaning pipeline
    Merges Tasks 1-3, detects language, removes HTML, deduplicates, removes PII
    """
    
    def __init__(self, 
                 task1_path: str = None,
                 task2_path: str = None,
                 task3_path: str = None,
                 output_dir: str = "cleaned_data"):
        """
        Initialize DataCleaner
        
        Args:
            task1_path: /Users/emmawang/Library/Mobile Documents/com~apple~CloudDocs/Emma My Product/AI_Projects/VicEdu_ML/HW2_DataCollectionExtraction/Bonus_HW_data_collection_projects/arxiv_scraper_project/data/json/arxiv_clean.json
            task2_path: /Users/emmawang/Library/Mobile Documents/com~apple~CloudDocs/Emma My Product/AI_Projects/VicEdu_ML/HW2_DataCollectionExtraction/Bonus_HW_data_collection_projects/pdf_text_OCR/pdf_ocr/
            task3_path: /Users/emmawang/Library/Mobile Documents/com~apple~CloudDocs/Emma My Product/AI_Projects/VicEdu_ML/HW2_DataCollectionExtraction/Bonus_HW_data_collection_projects/talks_transcripts.jsonl
            output_dir: /Users/emmawang/Library/Mobile Documents/com~apple~CloudDocs/Emma My Product/AI_Projects/VicEdu_ML/HW2_DataCollectionExtraction/Bonus_HW_data_collection_projects/Cleaning_Script/cleaned_data
        """
        self.task1_path = task1_path
        self.task2_path = task2_path
        self.task3_path = task3_path
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Statistics tracking
        self.stats = {
            'total_documents': 0,
            'task1_documents': 0,
            'task2_documents': 0,
            'task3_documents': 0,
            'total_chars_original': 0,
            'total_words_original': 0,
            'total_tokens_original': 0,
            'documents_after_language_filter': 0,
            'documents_after_html_cleaning': 0,
            'documents_after_deduplication': 0,
            'documents_after_pii_removal': 0,
            'documents_after_ngram_filter': 0,
            'total_chars_final': 0,
            'total_words_final': 0,
            'total_tokens_final': 0,
            'removal_percentage': 0,
            'pii_patterns_found': defaultdict(int),
            'languages_detected': defaultdict(int),
        }
        
        # PII patterns
        self.pii_patterns = {
            'email': re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
            'phone': re.compile(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'),
            'ssn': re.compile(r'\b\d{3}-\d{2}-\d{4}\b'),
            'credit_card': re.compile(r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b'),
            'url': re.compile(r'https?://[^\s]+'),
        }
        
        # Initialize LSH for deduplication
        self.lsh = MinHashLSH(threshold=0.7, num_perm=128)
        self.seen_docs = set()
        
    def load_data(self) -> List[Dict]:
        """
        Load all data from Tasks 1-3
        
        Returns:
            List of document dictionaries with 'text' and 'source' fields
        """
        documents = []
        
        # Load Task #1 (ArXiv papers)
        if self.task1_path and Path(self.task1_path).exists():
            logger.info(f"Loading Task #1 data from {self.task1_path}")
            try:
                with open(self.task1_path, 'r', encoding='utf-8') as f:
                    task1_data = json.load(f)
                    for paper in task1_data:
                        text = f"{paper.get('title', '')} {paper.get('abstract', '')}"
                        documents.append({
                            'text': text.strip(),
                            'source': 'task1_arxiv',
                            'id': paper.get('id', 'unknown')
                        })
                    self.stats['task1_documents'] = len(task1_data)
                    logger.info(f"Loaded {len(task1_data)} documents from Task #1")
            except Exception as e:
                logger.error(f"Error loading Task #1: {e}")
        
        # Load Task #2 (OCR PDFs)
        if self.task2_path and Path(self.task2_path).exists():
            logger.info(f"Loading Task #2 data from {self.task2_path}")
            task2_dir = Path(self.task2_path)
            txt_files = list(task2_dir.glob("*.txt"))
            for txt_file in txt_files:
                try:
                    with open(txt_file, 'r', encoding='utf-8') as f:
                        text = f.read()
                        documents.append({
                            'text': text.strip(),
                            'source': 'task2_ocr',
                            'id': txt_file.stem
                        })
                except Exception as e:
                    logger.error(f"Error loading {txt_file}: {e}")
            self.stats['task2_documents'] = len(txt_files)
            logger.info(f"Loaded {len(txt_files)} documents from Task #2")
        
        # Load Task #3 (Transcripts)
        if self.task3_path and Path(self.task3_path).exists():
            logger.info(f"Loading Task #3 data from {self.task3_path}")
            try:
                with open(self.task3_path, 'r', encoding='utf-8') as f:
                    task3_count = 0
                    for line in f:
                        try:
                            data = json.loads(line.strip())
                            documents.append({
                                'text': data.get('transcript', '').strip(),
                                'source': 'task3_transcript',
                                'id': data.get('video_id', 'unknown')
                            })
                            task3_count += 1
                        except json.JSONDecodeError:
                            continue
                self.stats['task3_documents'] = task3_count
                logger.info(f"Loaded {task3_count} documents from Task #3")
            except Exception as e:
                logger.error(f"Error loading Task #3: {e}")
        
        self.stats['total_documents'] = len(documents)
        logger.info(f"Total documents loaded: {len(documents)}")
        
        # Calculate original statistics
        for doc in documents:
            text = doc['text']
            self.stats['total_chars_original'] += len(text)
            self.stats['total_words_original'] += len(text.split())
            self.stats['total_tokens_original'] += len(text.split())
        
        return documents
    
    def detect_language(self, text: str) -> str:
        """
        Detect language of text
        
        Args:
            text: Input text
            
        Returns:
            Language code (e.g., 'en', 'fr', 'de')
        """
        try:
            # Use first 1000 chars for detection (faster)
            sample = text[:1000]
            lang = detect(sample)
            return lang
        except LangDetectException:
            return 'unknown'
    
    def filter_by_language(self, documents: List[Dict], target_lang: str = 'en') -> List[Dict]:
        """
        Filter documents by language
        
        Args:
            documents: List of document dictionaries
            target_lang: Target language code (default: 'en')
            
        Returns:
            Filtered list of documents
        """
        logger.info(f"Filtering documents by language: {target_lang}")
        filtered = []
        
        for doc in documents:
            lang = self.detect_language(doc['text'])
            self.stats['languages_detected'][lang] += 1
            
            if lang == target_lang:
                filtered.append(doc)
        
        self.stats['documents_after_language_filter'] = len(filtered)
        logger.info(f"Documents after language filter: {len(filtered)}/{len(documents)}")
        
        return filtered
    
    def clean_html(self, text: str) -> str:
        """
        Remove HTML tags and clean HTML entities
        
        Args:
            text: Input text
            
        Returns:
            Cleaned text
        """
        # Parse HTML
        soup = BeautifulSoup(text, 'html.parser')  # Changed from 'lxml' for Python 3.13 compatibility
        # Extract text
        text = soup.get_text()
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def remove_html(self, documents: List[Dict]) -> List[Dict]:
        """
        Remove HTML from all documents
        
        Args:
            documents: List of document dictionaries
            
        Returns:
            Cleaned documents
        """
        logger.info("Removing HTML tags and entities")
        
        for doc in documents:
            doc['text'] = self.clean_html(doc['text'])
        
        self.stats['documents_after_html_cleaning'] = len(documents)
        logger.info(f"HTML cleaning complete: {len(documents)} documents")
        
        return documents
    
    def create_minhash(self, text: str) -> MinHash:
        """
        Create MinHash signature for text
        
        Args:
            text: Input text
            
        Returns:
            MinHash object
        """
        m = MinHash(num_perm=128)
        # Use word-level shingling
        words = text.lower().split()
        # Create 3-grams
        for i in range(len(words) - 2):
            shingle = ' '.join(words[i:i+3])
            m.update(shingle.encode('utf-8'))
        return m
    
    def deduplicate(self, documents: List[Dict]) -> List[Dict]:
        """
        Remove duplicate documents using MinHash LSH
        
        Args:
            documents: List of document dictionaries
            
        Returns:
            Deduplicated documents
        """
        logger.info("Deduplicating documents with MinHash LSH (threshold=0.7)")
        
        unique_docs = []
        
        for idx, doc in enumerate(documents):
            text = doc['text']
            
            # Skip empty documents
            if not text or len(text.split()) < 10:
                continue
            
            # Create MinHash
            mh = self.create_minhash(text)
            
            # Check for duplicates
            result = self.lsh.query(mh)
            
            if not result:
                # No duplicates found, add to index
                self.lsh.insert(f"doc_{idx}", mh)
                unique_docs.append(doc)
            else:
                logger.debug(f"Duplicate found for doc {idx}")
        
        self.stats['documents_after_deduplication'] = len(unique_docs)
        logger.info(f"Documents after deduplication: {len(unique_docs)}/{len(documents)}")
        
        return unique_docs
    
    def remove_pii(self, text: str) -> str:
        """
        Remove PII (emails, phones, SSNs, credit cards, URLs)
        
        Args:
            text: Input text
            
        Returns:
            Text with PII removed
        """
        for pii_type, pattern in self.pii_patterns.items():
            matches = pattern.findall(text)
            if matches:
                self.stats['pii_patterns_found'][pii_type] += len(matches)
                text = pattern.sub(f'[{pii_type.upper()}_REMOVED]', text)
        
        return text
    
    def remove_pii_from_documents(self, documents: List[Dict]) -> List[Dict]:
        """
        Remove PII from all documents
        
        Args:
            documents: List of document dictionaries
            
        Returns:
            Documents with PII removed
        """
        logger.info("Removing PII (emails, phones, URLs, etc.)")
        
        for doc in documents:
            doc['text'] = self.remove_pii(doc['text'])
        
        self.stats['documents_after_pii_removal'] = len(documents)
        logger.info(f"PII removal complete: {len(documents)} documents")
        
        return documents
    
    def calculate_ngram_repetition(self, text: str, n: int = 4) -> float:
        """
        Calculate n-gram repetition ratio
        
        Args:
            text: Input text
            n: N-gram size
            
        Returns:
            Repetition ratio (0-1)
        """
        words = text.split()
        if len(words) < n:
            return 0.0
        
        # Create n-grams
        text_ngrams = list(ngrams(words, n))
        
        if not text_ngrams:
            return 0.0
        
        # Count unique vs total
        unique_ngrams = len(set(text_ngrams))
        total_ngrams = len(text_ngrams)
        
        repetition_ratio = 1 - (unique_ngrams / total_ngrams)
        return repetition_ratio
    
    def filter_by_ngrams(self, documents: List[Dict], threshold: float = 0.3) -> List[Dict]:
        """
        Filter out documents with high n-gram repetition
        
        Args:
            documents: List of document dictionaries
            threshold: Maximum repetition ratio (default: 0.3)
            
        Returns:
            Filtered documents
        """
        logger.info(f"Filtering by n-gram repetition (threshold={threshold})")
        
        filtered = []
        
        for doc in documents:
            text = doc['text']
            repetition = self.calculate_ngram_repetition(text)
            
            if repetition < threshold:
                filtered.append(doc)
            else:
                logger.debug(f"Removed doc with {repetition:.2%} repetition")
        
        self.stats['documents_after_ngram_filter'] = len(filtered)
        logger.info(f"Documents after n-gram filter: {len(filtered)}/{len(documents)}")
        
        return filtered
    
    def save_clean_corpus(self, documents: List[Dict]) -> Path:
        """
        Save cleaned corpus to file
        
        Args:
            documents: List of document dictionaries
            
        Returns:
            Path to output file
        """
        output_file = self.output_dir / "clean_corpus.txt"
        
        logger.info(f"Saving clean corpus to {output_file}")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for doc in documents:
                f.write(doc['text'])
                f.write('\n\n' + '='*80 + '\n\n')
        
        # Calculate final statistics
        for doc in documents:
            text = doc['text']
            self.stats['total_chars_final'] += len(text)
            self.stats['total_words_final'] += len(text.split())
            self.stats['total_tokens_final'] += len(text.split())
        
        # Calculate removal percentage
        if self.stats['total_tokens_original'] > 0:
            removed = self.stats['total_tokens_original'] - self.stats['total_tokens_final']
            self.stats['removal_percentage'] = (removed / self.stats['total_tokens_original']) * 100
        
        logger.info(f"Clean corpus saved: {len(documents)} documents")
        
        return output_file
    
    def save_statistics(self) -> Path:
        """
        Save cleaning statistics to file
        
        Returns:
            Path to statistics file
        """
        stats_file = self.output_dir / "stats.md"
        
        logger.info(f"Saving statistics to {stats_file}")
        
        with open(stats_file, 'w', encoding='utf-8') as f:
            f.write("# Data Cleaning Statistics\n\n")
            f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## Input Statistics\n\n")
            f.write(f"- **Total Documents Loaded**: {self.stats['total_documents']}\n")
            f.write(f"  - Task #1 (ArXiv): {self.stats['task1_documents']}\n")
            f.write(f"  - Task #2 (OCR): {self.stats['task2_documents']}\n")
            f.write(f"  - Task #3 (Transcripts): {self.stats['task3_documents']}\n\n")
            
            f.write(f"- **Original Characters**: {self.stats['total_chars_original']:,}\n")
            f.write(f"- **Original Words**: {self.stats['total_words_original']:,}\n")
            f.write(f"- **Original Tokens**: {self.stats['total_tokens_original']:,}\n\n")
            
            f.write("## Cleaning Pipeline Results\n\n")
            f.write(f"1. **After Language Filter**: {self.stats['documents_after_language_filter']} documents\n")
            f.write(f"2. **After HTML Cleaning**: {self.stats['documents_after_html_cleaning']} documents\n")
            f.write(f"3. **After Deduplication**: {self.stats['documents_after_deduplication']} documents\n")
            f.write(f"4. **After PII Removal**: {self.stats['documents_after_pii_removal']} documents\n")
            f.write(f"5. **After N-gram Filter**: {self.stats['documents_after_ngram_filter']} documents\n\n")
            
            f.write("## Output Statistics\n\n")
            f.write(f"- **Final Documents**: {self.stats['documents_after_ngram_filter']}\n")
            f.write(f"- **Final Characters**: {self.stats['total_chars_final']:,}\n")
            f.write(f"- **Final Words**: {self.stats['total_words_final']:,}\n")
            f.write(f"- **Final Tokens**: {self.stats['total_tokens_final']:,}\n")
            f.write(f"- **Data Removed**: {self.stats['removal_percentage']:.2f}%\n\n")
            
            f.write("## Language Detection\n\n")
            f.write("| Language | Count |\n")
            f.write("|----------|-------|\n")
            for lang, count in sorted(self.stats['languages_detected'].items(), 
                                     key=lambda x: x[1], reverse=True):
                f.write(f"| {lang} | {count} |\n")
            f.write("\n")
            
            f.write("## PII Patterns Removed\n\n")
            f.write("| Type | Count |\n")
            f.write("|------|-------|\n")
            for pii_type, count in sorted(self.stats['pii_patterns_found'].items()):
                f.write(f"| {pii_type} | {count} |\n")
            f.write("\n")
        
        logger.info("Statistics saved")
        
        return stats_file
    
    def run_pipeline(self):
        """
        Run the complete cleaning pipeline
        """
        logger.info("="*80)
        logger.info("Starting Task #4: Data Cleaning & Deduplication")
        logger.info("="*80)
        
        # Step 1: Load data
        documents = self.load_data()
        
        if not documents:
            logger.error("No documents loaded! Check your input paths.")
            return
        
        # Step 2: Language filtering
        documents = self.filter_by_language(documents, target_lang='en')
        
        # Step 3: HTML cleaning
        documents = self.remove_html(documents)
        
        # Step 4: Deduplication
        documents = self.deduplicate(documents)
        
        # Step 5: PII removal
        documents = self.remove_pii_from_documents(documents)
        
        # Step 6: N-gram filtering
        documents = self.filter_by_ngrams(documents, threshold=0.3)
        
        # Step 7: Save results
        output_file = self.save_clean_corpus(documents)
        stats_file = self.save_statistics()
        
        logger.info("="*80)
        logger.info("Task #4 Complete!")
        logger.info("="*80)
        logger.info(f"Clean corpus saved to: {output_file}")
        logger.info(f"Statistics saved to: {stats_file}")
        logger.info(f"Final document count: {len(documents)}")
        logger.info(f"Data removed: {self.stats['removal_percentage']:.2f}%")


def main():
    """Main execution function"""
    
    # Download NLTK data if needed
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        logger.info("Downloading NLTK punkt tokenizer...")
        nltk.download('punkt')
    
    # Initialize cleaner with default paths
    cleaner = DataCleaner(
        task1_path="../arxiv_scraper_project/data/json/arxiv_clean.json",
        task2_path="../pdf_text_OCR/pdf_ocr",
        task3_path="../asr_whisper/asr_whisper/transcripts/talks_transcripts.jsonl",
        output_dir="cleaned_data"
    )
    
    # Run the pipeline
    cleaner.run_pipeline()


if __name__ == "__main__":
    main()