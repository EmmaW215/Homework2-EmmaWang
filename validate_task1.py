#!/usr/bin/env python3
"""
Validation Script for Task #1: arXiv Paper Abstract Scraper
Checks output quality, completeness, and compliance with requirements
"""

import json
import sys
from pathlib import Path
from collections import Counter


def validate_json_file(filepath: Path) -> dict:
    """Validate JSON structure and content"""
    
    print(f"\n{'='*80}")
    print(f"VALIDATING: {filepath}")
    print(f"{'='*80}\n")
    
    results = {
        "file_exists": False,
        "valid_json": False,
        "file_size_ok": False,
        "has_metadata": False,
        "has_papers": False,
        "paper_count": 0,
        "required_fields_ok": True,
        "extraction_methods": Counter(),
        "failed_extractions": 0,
        "issues": []
    }
    
    # Check 1: File exists
    if not filepath.exists():
        results["issues"].append(f"❌ File not found: {filepath}")
        return results
    
    results["file_exists"] = True
    print("✓ File exists")
    
    # Check 2: File size
    file_size_mb = filepath.stat().st_size / (1024 * 1024)
    print(f"✓ File size: {file_size_mb:.2f} MB", end="")
    
    if file_size_mb <= 1.0:
        results["file_size_ok"] = True
        print(" (OK)")
    else:
        results["issues"].append(f"❌ File size exceeds 1MB: {file_size_mb:.2f}MB")
        print(" (EXCEEDS 1MB LIMIT!)")
    
    # Check 3: Valid JSON
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        results["valid_json"] = True
        print("✓ Valid JSON format")
    except json.JSONDecodeError as e:
        results["issues"].append(f"❌ Invalid JSON: {e}")
        print(f"❌ Invalid JSON: {e}")
        return results
    
    # Check 4: Metadata
    if "metadata" in data:
        results["has_metadata"] = True
        print("\n--- Metadata ---")
        for key, value in data["metadata"].items():
            print(f"  {key}: {value}")
    else:
        results["issues"].append("⚠️  No metadata found")
    
    # Check 5: Papers array
    if "papers" not in data:
        results["issues"].append("❌ No 'papers' array found")
        print("❌ No 'papers' array found")
        return results
    
    results["has_papers"] = True
    papers = data["papers"]
    results["paper_count"] = len(papers)
    
    print(f"\n✓ Found {len(papers)} papers")
    
    # Check 6: Required fields for each paper
    required_fields = ["url", "title", "abstract", "authors", "date"]
    
    print("\n--- Paper Validation ---")
    for i, paper in enumerate(papers[:5]):  # Check first 5 papers in detail
        print(f"\nPaper {i+1}:")
        print(f"  Title: {paper.get('title', 'MISSING')[:60]}...")
        
        for field in required_fields:
            if field not in paper:
                results["required_fields_ok"] = False
                results["issues"].append(f"❌ Paper {i+1} missing field: {field}")
                print(f"  ❌ Missing: {field}")
            elif paper[field] in [None, "", []]:
                results["required_fields_ok"] = False
                results["issues"].append(f"❌ Paper {i+1} has empty field: {field}")
                print(f"  ❌ Empty: {field}")
            else:
                print(f"  ✓ {field}: OK")
        
        # Track extraction method
        method = paper.get("extraction_method", "unknown")
        results["extraction_methods"][method] += 1
        
        # Check for failed extractions
        if paper.get("abstract") == "EXTRACTION_FAILED":
            results["failed_extractions"] += 1
    
    if len(papers) > 5:
        print(f"\n... checking remaining {len(papers) - 5} papers ...")
        
        for paper in papers[5:]:
            # Quick validation
            for field in required_fields:
                if field not in paper or paper[field] in [None, "", []]:
                    results["required_fields_ok"] = False
                    results["issues"].append(f"⚠️  Paper has missing/empty field: {field}")
            
            method = paper.get("extraction_method", "unknown")
            results["extraction_methods"][method] += 1
            
            if paper.get("abstract") == "EXTRACTION_FAILED":
                results["failed_extractions"] += 1
    
    # Summary statistics
    print("\n--- Extraction Method Distribution ---")
    for method, count in results["extraction_methods"].most_common():
        percentage = (count / len(papers)) * 100
        print(f"  {method}: {count} ({percentage:.1f}%)")
    
    if results["failed_extractions"] > 0:
        fail_rate = (results["failed_extractions"] / len(papers)) * 100
        print(f"\n⚠️  Failed extractions: {results['failed_extractions']} ({fail_rate:.1f}%)")
        
        if fail_rate > 10:
            results["issues"].append(f"⚠️  High failure rate: {fail_rate:.1f}%")
    
    return results


def print_final_report(results: dict):
    """Print final validation report"""
    
    print(f"\n{'='*80}")
    print("FINAL VALIDATION REPORT")
    print(f"{'='*80}\n")
    
    # Overall status
    all_checks_passed = (
        results["file_exists"] and
        results["valid_json"] and
        results["file_size_ok"] and
        results["has_metadata"] and
        results["has_papers"] and
        results["required_fields_ok"] and
        results["failed_extractions"] < results["paper_count"] * 0.1  # <10% failure
    )
    
    if all_checks_passed:
        print("🎉 ALL CHECKS PASSED! Ready for submission.")
        print(f"✓ {results['paper_count']} papers successfully scraped")
        print(f"✓ Success rate: {((results['paper_count'] - results['failed_extractions']) / results['paper_count'] * 100):.1f}%")
    else:
        print("⚠️  VALIDATION ISSUES FOUND:")
        for issue in results["issues"]:
            print(f"  {issue}")
    
    print(f"\n{'='*80}\n")
    
    return 0 if all_checks_passed else 1


def main():
    """Main validation entry point"""
    
    # Default file path
    json_path = Path("data/json/arxiv_clean.json")
    
    # Allow custom path as argument
    if len(sys.argv) > 1:
        json_path = Path(sys.argv[1])
    
    # Run validation
    results = validate_json_file(json_path)
    
    # Print report
    exit_code = print_final_report(results)
    
    # Additional recommendations
    if exit_code == 0:
        print("📋 Deliverables checklist:")
        print("  ✅ arxiv_clean.json (validated)")
        print("  ✅ arxiv_scraper.py (your script)")
        print("  ✅ requirements.txt (dependencies)")
        print("  ✅ logs/scraper.log (execution logs)")
        print("\n📦 Ready to package for submission!")
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
