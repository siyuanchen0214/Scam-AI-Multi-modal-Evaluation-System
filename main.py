"""
Main entry point for Multi-modal Detection System
"""

import argparse
import logging
from pathlib import Path
from src.core import DetectionPipeline
from loguru import logger


def setup_logging(log_level: str = "INFO", log_file: str = "logs/detector.log"):
    """Setup logging configuration"""
    log_dir = Path(log_file).parent
    log_dir.mkdir(parents=True, exist_ok=True)
    
    logger.add(
        log_file,
        rotation="10 MB",
        retention="10 days",
        level=log_level,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
    )
    
    logger.info(f"Logging initialized. Level: {log_level}")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Multi-modal Detection System for Fraud Detection"
    )
    
    parser.add_argument(
        '--text',
        type=str,
        help='Text content or path to text file'
    )
    parser.add_argument(
        '--image',
        type=str,
        help='Path to image file'
    )
    parser.add_argument(
        '--audio',
        type=str,
        help='Path to audio file'
    )
    parser.add_argument(
        '--video',
        type=str,
        help='Path to video file'
    )
    parser.add_argument(
        '--config',
        type=str,
        default='config/detector.yaml',
        help='Path to configuration file'
    )
    parser.add_argument(
        '--log-level',
        type=str,
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        help='Logging level'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(log_level=args.log_level)
    
    # Initialize pipeline
    logger.info("Initializing detection pipeline...")
    pipeline = DetectionPipeline(config_path=Path(args.config))
    
    # Process content
    metadata = {
        'source': 'user_input',
        'timestamp': '2024-01-01T00:00:00',
        'analyst': 'multi_modal_detector'
    }
    
    result = pipeline.process(
        text=args.text,
        image=args.image,
        audio=args.audio,
        video=args.video,
        metadata=metadata
    )
    
    # Return result
    return result


if __name__ == "__main__":
    main()

