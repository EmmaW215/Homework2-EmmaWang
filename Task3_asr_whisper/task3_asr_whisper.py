#!/usr/bin/env python3
"""
Task #3: Automatic Speech Recognition (ASR) using Whisper
Transcribes NLP conference talks from YouTube with timestamps
"""

import json
import logging
import os
import time
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

import yt_dlp
import whisper

# Setup logging
Path('logs/asr').mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/asr/whisper_asr.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class WhisperASR:
    """
    Automatic Speech Recognition system using OpenAI's Whisper model
    Downloads YouTube audio and transcribes with timestamps
    """
    
    def __init__(self, 
                 audio_dir: str = "asr_whisper/audio",
                 transcript_dir: str = "asr_whisper/transcripts",
                 model_size: str = "base"):
        """
        Initialize WhisperASR
        
        Args:
            audio_dir: Directory to save downloaded audio files
            transcript_dir: Directory to save transcripts
            model_size: Whisper model size (tiny, base, small, medium, large)
        """
        self.audio_dir = Path(audio_dir)
        self.transcript_dir = Path(transcript_dir)
        self.audio_dir.mkdir(parents=True, exist_ok=True)
        self.transcript_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Loading Whisper model: {model_size}")
        self.model = whisper.load_model(model_size)
        logger.info(f"Whisper model loaded successfully")
        
    def download_audio(self, video_url: str, video_id: str) -> Optional[str]:
        """
        Download audio from YouTube video using yt-dlp
        
        Args:
            video_url: YouTube video URL
            video_id: Unique identifier for the video
            
        Returns:
            Path to downloaded audio file, or None if failed
        """
        output_path = self.audio_dir / f"{video_id}.mp3"
        
        # Skip if already downloaded
        if output_path.exists():
            logger.info(f"Audio already exists: {output_path}")
            return str(output_path)
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': str(self.audio_dir / f"{video_id}.%(ext)s"),
            'quiet': False,
            'no_warnings': False,
        }
        
        try:
            logger.info(f"Downloading audio from: {video_url}")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                title = info.get('title', 'Unknown')
                duration = info.get('duration', 0)
                logger.info(f"Downloaded: {title} (Duration: {duration}s)")
                
            return str(output_path)
            
        except Exception as e:
            logger.error(f"Failed to download {video_url}: {e}")
            return None
    
    def transcribe_audio(self, audio_path: str, video_id: str) -> Optional[Dict]:
        """
        Transcribe audio file using Whisper
        
        Args:
            audio_path: Path to audio file
            video_id: Video identifier
            
        Returns:
            Dictionary with transcription results including segments with timestamps
        """
        try:
            logger.info(f"Transcribing: {audio_path}")
            start_time = time.time()
            
            # Transcribe with Whisper
            result = self.model.transcribe(
                audio_path,
                verbose=False,
                language='en',  # Specify English for NLP talks
                task='transcribe'
            )
            
            elapsed = time.time() - start_time
            logger.info(f"Transcription completed in {elapsed:.2f}s")
            
            # Extract segments with timestamps
            segments = []
            for segment in result.get('segments', []):
                segments.append({
                    'id': segment['id'],
                    'start': segment['start'],
                    'end': segment['end'],
                    'text': segment['text'].strip(),
                    'tokens': segment.get('tokens', []),
                    'temperature': segment.get('temperature', 0.0),
                    'avg_logprob': segment.get('avg_logprob', 0.0),
                    'compression_ratio': segment.get('compression_ratio', 0.0),
                    'no_speech_prob': segment.get('no_speech_prob', 0.0)
                })
            
            return {
                'video_id': video_id,
                'language': result.get('language', 'en'),
                'text': result.get('text', '').strip(),
                'segments': segments,
                'duration': segments[-1]['end'] if segments else 0,
                'transcription_time': elapsed
            }
            
        except Exception as e:
            logger.error(f"Failed to transcribe {audio_path}: {e}")
            return None
    
    def process_video(self, video_url: str, video_id: str, metadata: Dict = None) -> Dict:
        """
        Download and transcribe a single video
        
        Args:
            video_url: YouTube URL
            video_id: Unique identifier
            metadata: Additional metadata (title, conference, etc.)
            
        Returns:
            Complete transcript entry with metadata
        """
        logger.info(f"Processing video: {video_id}")
        
        # Download audio
        audio_path = self.download_audio(video_url, video_id)
        if not audio_path:
            return {
                'video_id': video_id,
                'url': video_url,
                'status': 'failed_download',
                'error': 'Could not download audio'
            }
        
        # Transcribe
        transcript = self.transcribe_audio(audio_path, video_id)
        if not transcript:
            return {
                'video_id': video_id,
                'url': video_url,
                'status': 'failed_transcription',
                'error': 'Could not transcribe audio'
            }
        
        # Combine with metadata
        result = {
            'video_id': video_id,
            'url': video_url,
            'status': 'success',
            'processed_at': datetime.now().isoformat(),
            **transcript
        }
        
        if metadata:
            result.update(metadata)
        
        return result
    
    def process_batch(self, video_list: List[Dict], output_file: str = "talks_transcripts.jsonl"):
        """
        Process multiple videos and save to JSONL
        
        Args:
            video_list: List of dicts with 'url' and optional metadata
            output_file: Output JSONL file path
        """
        output_path = self.transcript_dir / output_file
        
        results = []
        total = len(video_list)
        
        for idx, video_info in enumerate(video_list, 1):
            logger.info(f"\n{'='*60}")
            logger.info(f"Processing video {idx}/{total}")
            logger.info(f"{'='*60}")
            
            video_url = video_info.get('url')
            video_id = video_info.get('id', f"video_{idx:02d}")
            metadata = {k: v for k, v in video_info.items() if k not in ['url', 'id']}
            
            result = self.process_video(video_url, video_id, metadata)
            results.append(result)
            
            # Save incrementally (in case of interruption)
            with open(output_path, 'w', encoding='utf-8') as f:
                for r in results:
                    f.write(json.dumps(r, ensure_ascii=False) + '\n')
            
            logger.info(f"Saved progress to {output_path}")
            
            # Small delay between videos to be respectful
            if idx < total:
                time.sleep(2)
        
        # Generate summary statistics
        self._generate_summary(results, output_path)
        
        logger.info(f"\n{'='*60}")
        logger.info(f"Batch processing complete!")
        logger.info(f"Total videos: {total}")
        logger.info(f"Successful: {sum(1 for r in results if r['status'] == 'success')}")
        logger.info(f"Failed: {sum(1 for r in results if r['status'] != 'success')}")
        logger.info(f"Output saved to: {output_path}")
        logger.info(f"{'='*60}\n")
        
        return results
    
    def _generate_summary(self, results: List[Dict], output_path: Path):
        """Generate summary statistics for the transcription batch"""
        summary_path = output_path.parent / "transcription_summary.md"
        
        successful = [r for r in results if r['status'] == 'success']
        failed = [r for r in results if r['status'] != 'success']
        
        total_duration = sum(r.get('duration', 0) for r in successful)
        total_words = sum(len(r.get('text', '').split()) for r in successful)
        total_segments = sum(len(r.get('segments', [])) for r in successful)
        
        with open(summary_path, 'w') as f:
            f.write("# ASR Transcription Summary\n\n")
            f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("## Statistics\n\n")
            f.write(f"- **Total Videos**: {len(results)}\n")
            f.write(f"- **Successful**: {len(successful)}\n")
            f.write(f"- **Failed**: {len(failed)}\n")
            f.write(f"- **Total Audio Duration**: {total_duration:.2f} seconds ({total_duration/60:.2f} minutes)\n")
            f.write(f"- **Total Words Transcribed**: {total_words:,}\n")
            f.write(f"- **Total Segments**: {total_segments}\n\n")
            
            if successful:
                avg_duration = total_duration / len(successful)
                avg_words = total_words / len(successful)
                f.write(f"- **Average Video Duration**: {avg_duration:.2f} seconds\n")
                f.write(f"- **Average Words per Video**: {avg_words:.0f}\n\n")
            
            f.write("## Successful Transcriptions\n\n")
            for r in successful:
                f.write(f"### {r['video_id']}\n")
                f.write(f"- **URL**: {r['url']}\n")
                f.write(f"- **Duration**: {r.get('duration', 0):.2f}s\n")
                f.write(f"- **Segments**: {len(r.get('segments', []))}\n")
                f.write(f"- **Language**: {r.get('language', 'unknown')}\n")
                if 'title' in r:
                    f.write(f"- **Title**: {r['title']}\n")
                f.write("\n")
            
            if failed:
                f.write("## Failed Transcriptions\n\n")
                for r in failed:
                    f.write(f"- **{r['video_id']}**: {r.get('error', 'Unknown error')}\n")
        
        logger.info(f"Summary saved to: {summary_path}")


def load_video_list(file_path: str) -> List[Dict]:
    """
    Load video list from JSON file
    
    Args:
        file_path: Path to JSON file with video information
        
    Returns:
        List of video dictionaries
    """
    with open(file_path, 'r') as f:
        return json.load(f)


def main():
    """Main execution function"""
    
    # Example video list - REPLACE WITH ACTUAL NLP CONFERENCE TALKS
    video_list = [
        {
            "id": "talk_01",
            "url": "https://www.youtube.com/shorts/BeCtc-z8wJM",
            "title": "NLP Talk Title",
            "conference": "ACL 2024",
            "speaker": "Speaker Name"
        },
        # Add 9 more videos...
    ]
    
    # Alternative: Load from JSON file
    # video_list = load_video_list('asr_whisper/video_list.json')
    
    # Initialize ASR system
    asr = WhisperASR(
        audio_dir="asr_whisper/audio",
        transcript_dir="asr_whisper/transcripts",
        model_size="base"  # Options: tiny, base, small, medium, large
    )
    
    # Process all videos
    results = asr.process_batch(
        video_list=video_list,
        output_file="talks_transcripts.jsonl"
    )
    
    logger.info("Task #3 completed successfully!")


if __name__ == "__main__":
    main()
