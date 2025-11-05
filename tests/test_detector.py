"""
Tests for multi-modal detector
"""

import pytest
from src.core import MultiModalDetector
from src.modalities import (
    TextDetector, ImageDetector, AudioDetector, VideoDetector
)


def test_text_detector():
    """Test text detector"""
    detector = TextDetector()
    result = detector.detect("This is a test text content.")
    
    assert result.score >= 0.0
    assert result.score <= 1.0
    assert isinstance(result.is_suspicious, bool)


def test_image_detector():
    """Test image detector"""
    detector = ImageDetector()
    # result = detector.detect("path/to/image.jpg")
    # assert result.score >= 0.0
    # assert result.score <= 1.0
    pass


def test_audio_detector():
    """Test audio detector"""
    detector = AudioDetector()
    # result = detector.detect("path/to/audio.wav")
    # assert result.score >= 0.0
    # assert result.score <= 1.0
    pass


def test_video_detector():
    """Test video detector"""
    detector = VideoDetector()
    # result = detector.detect("path/to/video.mp4")
    # assert result.score >= 0.0
    # assert result.score <= 1.0
    pass


def test_multi_modal_detector():
    """Test multi-modal detector"""
    detector = MultiModalDetector(enable_tracing=False, enable_learning=False)
    
    result = detector.detect(
        text="This is a sample text for testing.",
        metadata={'source': 'test', 'timestamp': '2024-01-01T00:00:00'}
    )
    
    assert hasattr(result, 'is_fraudulent')
    assert hasattr(result, 'confidence')
    assert 0.0 <= result.confidence <= 1.0

