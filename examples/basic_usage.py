"""
Basic usage example for Multi-modal Detection System
"""

from src.core import MultiModalDetector
from loguru import logger

def main():
    """Demonstrate basic usage of the detection system"""
    
    logger.info("Initializing Multi-modal Detection System...")
    
    # Initialize the detector
    detector = MultiModalDetector(
        enable_tracing=True,
        enable_learning=True
    )
    
    # Example 1: Text-only detection
    logger.info("\n=== Example 1: Text Detection ===")
    text_result = detector.detect(
        text="This is a sample text for fraud detection analysis.",
        metadata={
            'source': 'example',
            'timestamp': '2024-01-01T00:00:00',
            'analyst': 'multi_modal_detector'
        }
    )
    
    print(f"Text Detection Result:")
    print(f"  Is Fraudulent: {text_result.is_fraudulent}")
    print(f"  Confidence: {text_result.confidence:.3f}")
    print(f"  Scores: {text_result.modality_scores}")
    
    # Example 2: Multi-modal detection (placeholder)
    logger.info("\n=== Example 2: Multi-modal Detection ===")
    print("Note: This is a placeholder. Provide actual file paths for full detection.")
    
    # Uncomment when you have actual files:
    # result = detector.detect(
    #     text="Sample text content",
    #     image="path/to/image.jpg",
    #     audio="path/to/audio.wav",
    #     video="path/to/video.mp4",
    #     metadata={'source': 'file', 'timestamp': '2024-01-01T00:00:00'}
    # )
    
    logger.info("\nExamples completed successfully!")


if __name__ == "__main__":
    main()

