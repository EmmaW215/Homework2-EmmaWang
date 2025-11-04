#!/usr/bin/env python3
"""
Helper script to find and validate YouTube videos for ASR Task
Searches for NLP conference talks and checks video duration
"""

import json
import yt_dlp
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_video_info(video_url: str) -> Dict:
    """
    Get information about a YouTube video without downloading
    
    Args:
        video_url: YouTube URL
        
    Returns:
        Dictionary with video metadata
    """
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            
            duration_mins = info.get('duration', 0) / 60
            
            return {
                'url': video_url,
                'id': info.get('id', ''),
                'title': info.get('title', 'Unknown'),
                'duration_seconds': info.get('duration', 0),
                'duration_minutes': round(duration_mins, 2),
                'uploader': info.get('uploader', 'Unknown'),
                'upload_date': info.get('upload_date', ''),
                'view_count': info.get('view_count', 0),
                'description': info.get('description', '')[:200] + '...',
            }
    except Exception as e:
        logger.error(f"Error getting info for {video_url}: {e}")
        return None


def validate_video_duration(video_url: str, min_duration: int = 120, max_duration: int = 300) -> bool:
    """
    Check if video duration is within acceptable range
    
    Args:
        video_url: YouTube URL
        min_duration: Minimum duration in seconds (default: 2 minutes)
        max_duration: Maximum duration in seconds (default: 5 minutes)
        
    Returns:
        True if duration is acceptable
    """
    info = get_video_info(video_url)
    if not info:
        return False
    
    duration = info['duration_seconds']
    is_valid = min_duration <= duration <= max_duration
    
    logger.info(f"Video: {info['title']}")
    logger.info(f"Duration: {info['duration_minutes']} minutes - {'✓ VALID' if is_valid else '✗ INVALID'}")
    
    return is_valid


def check_video_list(video_urls: List[str]) -> List[Dict]:
    """
    Validate a list of video URLs and return their information
    
    Args:
        video_urls: List of YouTube URLs
        
    Returns:
        List of video info dictionaries
    """
    results = []
    
    for idx, url in enumerate(video_urls, 1):
        logger.info(f"\n--- Checking video {idx}/{len(video_urls)} ---")
        info = get_video_info(url)
        
        if info:
            results.append(info)
            logger.info(f"✓ Title: {info['title']}")
            logger.info(f"  Duration: {info['duration_minutes']} minutes")
            logger.info(f"  Uploader: {info['uploader']}")
        else:
            logger.warning(f"✗ Failed to get info for: {url}")
    
    return results


def generate_video_list_json(video_infos: List[Dict], output_file: str = "video_list_generated.json"):
    """
    Generate a formatted JSON file from video information
    
    Args:
        video_infos: List of video info dictionaries
        output_file: Output file path
    """
    formatted_list = []
    
    for idx, info in enumerate(video_infos, 1):
        formatted_list.append({
            "id": f"talk_{idx:02d}",
            "url": info['url'],
            "title": info['title'],
            "duration_minutes": info['duration_minutes'],
            "uploader": info['uploader'],
            "upload_date": info['upload_date'],
            # Add these fields manually after generation
            "conference": "TO_BE_FILLED",
            "speaker": "TO_BE_FILLED",
            "topic": "TO_BE_FILLED"
        })
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(formatted_list, f, indent=2, ensure_ascii=False)
    
    logger.info(f"\n✓ Generated video list: {output_file}")
    logger.info(f"  Total videos: {len(formatted_list)}")
    logger.info(f"  Please manually fill in: conference, speaker, topic fields")


def main():
    """
    Example usage - Replace with your actual YouTube URLs
    """
    
    # EXAMPLE: Replace these with actual NLP conference talk URLs
    example_urls = [
        # Add your 10 YouTube URLs here
        # "https://www.youtube.com/watch?v=...",
    ]
    
    print("\n" + "="*60)
    print("YouTube Video Validator for ASR Task")
    print("="*60)
    
    # Method 1: Check if URLs are provided
    if not example_urls or all('...' in url for url in example_urls):
        print("\n⚠️  Please add actual YouTube URLs to the 'example_urls' list!")
        print("\nHow to find suitable videos:")
        print("1. Search YouTube for: 'NLP conference talks' or 'ACL paper presentation'")
        print("2. Look for videos 2-5 minutes long")
        print("3. Channels to check:")
        print("   - ACL (Association for Computational Linguistics)")
        print("   - EMNLP Conference")
        print("   - NAACL")
        print("   - Stanford NLP")
        print("\n4. Add the URLs to this script and run again")
        return
    
    # Method 2: Validate the videos
    print("\nValidating video list...")
    video_infos = check_video_list(example_urls)
    
    # Method 3: Generate formatted JSON
    if video_infos:
        generate_video_list_json(video_infos, "asr_whisper/video_list_generated.json")
        
        # Print summary
        print("\n" + "="*60)
        print("SUMMARY")
        print("="*60)
        print(f"Valid videos: {len(video_infos)}/{len(example_urls)}")
        total_duration = sum(v['duration_minutes'] for v in video_infos)
        print(f"Total duration: {total_duration:.2f} minutes")
        print(f"\nNext steps:")
        print("1. Review 'video_list_generated.json'")
        print("2. Fill in missing metadata (conference, speaker, topic)")
        print("3. Rename to 'video_list.json'")
        print("4. Run task3_asr_whisper.py")


if __name__ == "__main__":
    main()
