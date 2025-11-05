"""
Cross-modal Consistency Analyzer with advanced semantic similarity
"""

import logging
import numpy as np
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

try:
    from sentence_transformers import SentenceTransformer
    HAS_SENTENCE_TRANSFORMERS = True
except ImportError:
    HAS_SENTENCE_TRANSFORMERS = False
    logging.warning("sentence_transformers not available, using basic similarity")


logger = logging.getLogger(__name__)


@dataclass
class ConsistencyScore:
    """Score for cross-modal consistency"""
    overall: float
    pairwise: Dict[str, float]
    anomalies: List[str]


class CrossModalAnalyzer:
    """
    Analyzer for detecting inconsistencies across different modalities
    (text, image, audio, video).
    """
    
    def __init__(self, use_semantic_similarity: bool = True):
        """
        Initialize the cross-modal analyzer.
        
        Args:
            use_semantic_similarity: Whether to use advanced semantic similarity models
        """
        logger.info("Initializing cross-modal analyzer...")
        self.similarity_threshold = 0.7
        self.use_semantic_similarity = use_semantic_similarity and HAS_SENTENCE_TRANSFORMERS
        
        if self.use_semantic_similarity:
            try:
                logger.info("Loading semantic similarity model...")
                self.similarity_model = SentenceTransformer('all-MiniLM-L6-v2')
                logger.info("Semantic similarity model loaded")
            except Exception as e:
                logger.warning(f"Could not load semantic model: {e}. Using basic similarity.")
                self.use_semantic_similarity = False
                self.similarity_model = None
        else:
            self.similarity_model = None
    
    def analyze_consistency(
        self,
        text_features: Any = None,
        image_features: Any = None,
        audio_features: Any = None,
        video_features: Any = None
    ) -> ConsistencyScore:
        """
        Analyze consistency across provided modalities.
        
        Args:
            text_features: Extracted text features
            image_features: Extracted image features
            audio_features: Extracted audio features
            video_features: Extracted video features
            
        Returns:
            ConsistencyScore with overall and pairwise scores
        """
        logger.info("Starting cross-modal consistency analysis...")
        
        modalities = {}
        if text_features is not None:
            modalities['text'] = text_features
        if image_features is not None:
            modalities['image'] = image_features
        if audio_features is not None:
            modalities['audio'] = audio_features
        if video_features is not None:
            modalities['video'] = video_features
        
        if len(modalities) < 2:
            logger.warning("Insufficient modalities for consistency analysis")
            return ConsistencyScore(
                overall=1.0,
                pairwise={},
                anomalies=[]
            )
        
        # Compute pairwise similarities
        pairwise_scores = {}
        anomalies = []
        
        modality_names = list(modalities.keys())
        for i, mod1 in enumerate(modality_names):
            for mod2 in modality_names[i+1:]:
                similarity = self._compute_similarity(
                    modalities[mod1],
                    modalities[mod2]
                )
                key = f"{mod1}_{mod2}"
                pairwise_scores[key] = similarity
                
                if similarity < self.similarity_threshold:
                    anomalies.append(f"Inconsistency between {mod1} and {mod2}")
        
        # Compute overall consistency score
        if pairwise_scores:
            overall_score = np.mean(list(pairwise_scores.values()))
        else:
            overall_score = 1.0
        
        logger.info(f"Cross-modal consistency analysis complete: {overall_score:.3f}")
        
        return ConsistencyScore(
            overall=overall_score,
            pairwise=pairwise_scores,
            anomalies=anomalies
        )
    
    def _compute_similarity(self, features1: Any, features2: Any) -> float:
        """
        Compute similarity between two feature sets.
        
        Args:
            features1: First feature set
            features2: Second feature set
            
        Returns:
            Similarity score (0-1)
        """
        # Convert features to numpy arrays if needed
        if not isinstance(features1, np.ndarray):
            features1 = np.array(features1)
        if not isinstance(features2, np.ndarray):
            features2 = np.array(features2)
        
        # Handle different shapes
        if features1.shape != features2.shape:
            # Flatten or use different comparison method
            features1 = features1.flatten()
            features2 = features2.flatten()
            
            # Pad or truncate to same length
            min_len = min(len(features1), len(features2))
            features1 = features1[:min_len]
            features2 = features2[:min_len]
        
        # Compute cosine similarity
        dot_product = np.dot(features1, features2)
        norm1 = np.linalg.norm(features1)
        norm2 = np.linalg.norm(features2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        similarity = dot_product / (norm1 * norm2)
        
        # Ensure value is in [0, 1]
        return max(0.0, min(1.0, similarity))
    
    def detect_narrative_inconsistencies(
        self,
        text_content: str,
        image_description: str,
        audio_transcript: str = None,
        video_summary: str = None
    ) -> List[str]:
        """
        Detect inconsistencies in narrative content across modalities.
        
        Args:
            text_content: Main text content
            image_description: Description of image content
            audio_transcript: Audio transcript (optional)
            video_summary: Video summary (optional)
            
        Returns:
            List of detected inconsistencies
        """
        inconsistencies = []
        
        # Simple semantic comparison (placeholder for actual NLP implementation)
        # In practice, this would use semantic similarity models
        
        if audio_transcript:
            if not self._semantic_match(text_content, audio_transcript):
                inconsistencies.append("Text-audio content mismatch")
        
        if video_summary:
            if not self._semantic_match(text_content, video_summary):
                inconsistencies.append("Text-video content mismatch")
        
        if image_description:
            if not self._semantic_match(text_content, image_description):
                inconsistencies.append("Text-image content mismatch")
        
        return inconsistencies
    
    def compute_semantic_similarity(self, text1: str, text2: str) -> float:
        """
        Compute semantic similarity score between two texts.
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Similarity score (0-1)
        """
        if self.use_semantic_similarity and self.similarity_model:
            try:
                embeddings = self.similarity_model.encode([text1, text2])
                from sklearn.metrics.pairwise import cosine_similarity
                similarity = cosine_similarity(
                    embeddings[0:1], 
                    embeddings[1:2]
                )[0][0]
                return max(0.0, min(1.0, similarity))
            except Exception as e:
                logger.warning(f"Semantic similarity failed: {e}")
        
        # Fallback to basic similarity
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        if len(words1) == 0 or len(words2) == 0:
            return 0.0
        overlap = len(words1.intersection(words2)) / len(words1.union(words2))
        return overlap
    
    def _semantic_match(self, text1: str, text2: str) -> bool:
        """
        Check if two texts semantically match.
        
        Uses sentence transformers for advanced semantic similarity if available,
        otherwise falls back to basic keyword overlap.
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            True if texts are semantically similar
        """
        if self.use_semantic_similarity and self.similarity_model:
            try:
                # Use semantic embeddings for similarity
                embeddings = self.similarity_model.encode([text1, text2])
                
                # Compute cosine similarity
                from sklearn.metrics.pairwise import cosine_similarity
                similarity = cosine_similarity(
                    embeddings[0:1], 
                    embeddings[1:2]
                )[0][0]
                
                # Threshold for semantic match
                return similarity > 0.5
            except Exception as e:
                logger.warning(f"Semantic similarity failed: {e}, using basic method")
        
        # Fallback: simple keyword overlap
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if len(words1) == 0 or len(words2) == 0:
            return False
        
        overlap = len(words1.intersection(words2)) / len(words1.union(words2))
        return overlap > 0.3


