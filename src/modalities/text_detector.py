"""
Text Modality Detector
"""

import logging
from typing import Union, Any
from pathlib import Path
from dataclasses import dataclass

from .base import ModalityDetector, DetectionResult


logger = logging.getLogger(__name__)


@dataclass
class TextDetectionResult(DetectionResult):
    """Result of text detection analysis"""
    pass


class TextDetector(ModalityDetector):
    """
    Detector for fraudulent patterns in text content.
    
    Analyzes text for:
    - AI-generated patterns (GPT, Claude, etc.)
    - Syntactic anomalies
    - Semantic inconsistencies
    - Repetitive patterns
    - Statistical deviations
    """
    
    def __init__(self, model_path: Union[str, Path] = None):
        """
        Initialize the text detector.
        
        Args:
            model_path: Path to text detection model
        """
        super().__init__(model_path)
        logger.info("Text detector initialized")
    
    def _load_model(self):
        """Load text detection models"""
        # Placeholder: Load actual models in implementation
        # This would load models like RoBERTa, GPT detectors, etc.
        logger.info("Loading text detection models...")
        self.feature_extractor = None  # Placeholder
        self.classifier = None  # Placeholder
    
    def detect(self, text: Union[str, Path]) -> TextDetectionResult:
        """
        Detect fraudulent patterns in text.
        
        Args:
            text: Text content (string or file path)
            
        Returns:
            TextDetectionResult with analysis
        """
        logger.info("Analyzing text content...")
        
        # Load text if path provided
        if isinstance(text, Path):
            text = text.read_text(encoding='utf-8')
        
        # Extract features
        features = self.extract_features(text)
        
        # Perform detection
        # Placeholder: Actual detection would use trained models
        score = self._compute_fraud_score(text, features)
        is_suspicious = score > 0.5
        
        logger.info(f"Text analysis complete. Score: {score:.3f}")
        
        return TextDetectionResult(
            score=score,
            features=features,
            is_suspicious=is_suspicious,
            details={
                'text_length': len(text),
                'word_count': len(text.split()),
                'average_word_length': sum(len(w) for w in text.split()) / max(len(text.split()), 1)
            }
        )
    
    def extract_features(self, text: Union[str, Path]) -> Any:
        """
        Extract features from text content.
        
        Args:
            text: Text content (string or file path)
            
        Returns:
            Extracted features
        """
        # Load text if path provided
        if isinstance(text, Path):
            text = text.read_text(encoding='utf-8')
        
        # Placeholder: Actual feature extraction
        # Features could include:
        # - Statistical features (perplexity, entropy, etc.)
        # - Embeddings (sentence transformers, word embeddings)
        # - Linguistic features (syntax patterns, word frequencies)
        features = {
            'length': len(text),
            'words': len(text.split()),
            'vocab_size': len(set(text.lower().split())),
            # Additional features would be extracted here
        }
        
        return features
    
    def _compute_fraud_score(self, text: str, features: dict) -> float:
        """
        Compute fraud score for text.
        
        Args:
            text: Text content
            features: Extracted features
            
        Returns:
            Fraud score (0-1)
        """
        # Placeholder implementation
        # In practice, this would use trained models
        
        # Simple heuristics for demonstration
        score = 0.0
        
        # Check for repetitive patterns
        if self._has_repetitive_patterns(text):
            score += 0.2
        
        # Check for statistical anomalies
        if self._has_statistical_anomalies(text, features):
            score += 0.3
        
        # Check for AI generation patterns
        if self._has_ai_patterns(text):
            score += 0.3
        
        return min(score, 1.0)
    
    def _has_repetitive_patterns(self, text: str) -> bool:
        """Check for repetitive patterns"""
        # Simple check for sentence repetition
        sentences = text.split('.')
        if len(sentences) < 2:
            return False
        
        # Check if any sentence appears multiple times
        sentence_counts = {}
        for sentence in sentences:
            sentence = sentence.strip().lower()
            if len(sentence) > 10:  # Ignore very short sentences
                sentence_counts[sentence] = sentence_counts.get(sentence, 0) + 1
        
        return any(count > 2 for count in sentence_counts.values())
    
    def _has_statistical_anomalies(self, text: str, features: dict) -> bool:
        """Check for statistical anomalies"""
        # Check for unusual vocab diversity
        vocab_size = features.get('vocab_size', 0)
        word_count = features.get('words', 1)
        
        vocab_ratio = vocab_size / word_count if word_count > 0 else 0
        # Low vocab ratio might indicate AI generation
        return vocab_ratio < 0.3
    
    def _has_ai_patterns(self, text: str) -> bool:
        """Check for AI-generated patterns"""
        # Common AI generation patterns
        ai_phrases = [
            "as an ai", "i'm an ai", "i cannot",
            "i don't have the ability", "i don't have access"
        ]
        
        text_lower = text.lower()
        return any(phrase in text_lower for phrase in ai_phrases)


