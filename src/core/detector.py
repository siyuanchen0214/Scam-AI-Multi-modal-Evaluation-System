"""
Multi-modal Detector - Main detection orchestrator
"""

import logging
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass
from pathlib import Path

from ..modalities import (
    TextDetector,
    ImageDetector,
    AudioDetector,
    VideoDetector
)
from ..tracing import ProvenanceTracer
from ..reverse_engineering import PatternAnalyzer
from ..learning import ContinuousLearner
from ..evaluation import SeverityClassifier, AlertEngine, SignalCombinator


logger = logging.getLogger(__name__)


@dataclass
class DetectionResult:
    """Result of a detection analysis"""
    is_fraudulent: bool
    confidence: float
    modality_scores: Dict[str, float]
    cross_modal_consistency: float
    provenance_trace: Optional[Dict[str, Any]]
    pattern_signatures: List[Dict[str, Any]]
    details: Dict[str, Any]


class MultiModalDetector:
    """
    Main multi-modal detector that integrates detection across all modalities
    and performs provenance tracing and pattern analysis.
    """
    
    def __init__(
        self,
        config_path: Optional[Union[str, Path]] = None,
        enable_tracing: bool = True,
        enable_learning: bool = True,
        enable_evaluation: bool = True
    ):
        """
        Initialize the multi-modal detector.
        
        Args:
            config_path: Path to configuration file
            enable_tracing: Whether to enable provenance tracing
            enable_learning: Whether to enable continuous learning
            enable_evaluation: Whether to enable dynamic evaluation
        """
        self.config_path = config_path
        self.enable_tracing = enable_tracing
        self.enable_learning = enable_learning
        self.enable_evaluation = enable_evaluation
        
        # Initialize modality detectors
        logger.info("Initializing modality detectors...")
        self.text_detector = TextDetector()
        self.image_detector = ImageDetector()
        self.audio_detector = AudioDetector()
        self.video_detector = VideoDetector()
        
        # Initialize tracing and analysis components
        if self.enable_tracing:
            logger.info("Initializing provenance tracer...")
            self.provenance_tracer = ProvenanceTracer()
        
        logger.info("Initializing pattern analyzer...")
        self.pattern_analyzer = PatternAnalyzer()
        
        if self.enable_learning:
            logger.info("Initializing continuous learner...")
            self.learner = ContinuousLearner()
        
        if self.enable_evaluation:
            logger.info("Initializing evaluation system...")
            self.severity_classifier = SeverityClassifier()
            self.alert_engine = AlertEngine()
            self.signal_combinator = SignalCombinator()
        
        logger.info("Multi-modal detector initialized successfully")
    
    def detect(
        self,
        text: Optional[Union[str, Path]] = None,
        image: Optional[Union[str, Path]] = None,
        audio: Optional[Union[str, Path]] = None,
        video: Optional[Union[str, Path]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> DetectionResult:
        """
        Detect fraudulent content across multiple modalities.
        
        Args:
            text: Text content (string or file path)
            image: Image content (file path)
            audio: Audio content (file path)
            video: Video content (file path)
            metadata: Additional metadata
            
        Returns:
            DetectionResult with detailed analysis
        """
        logger.info("Starting multi-modal detection analysis...")
        
        modality_scores = {}
        modality_features = {}
        
        # Detect in each modality
        if text is not None:
            logger.info("Analyzing text modality...")
            text_result = self.text_detector.detect(text)
            modality_scores['text'] = text_result.score
            modality_features['text'] = text_result.features
        
        if image is not None:
            logger.info("Analyzing image modality...")
            image_result = self.image_detector.detect(image)
            modality_scores['image'] = image_result.score
            modality_features['image'] = image_result.features
        
        if audio is not None:
            logger.info("Analyzing audio modality...")
            audio_result = self.audio_detector.detect(audio)
            modality_scores['audio'] = audio_result.score
            modality_features['audio'] = audio_result.features
        
        if video is not None:
            logger.info("Analyzing video modality...")
            video_result = self.video_detector.detect(video)
            modality_scores['video'] = video_result.score
            modality_features['video'] = video_result.features
        
        # Cross-modal consistency analysis
        logger.info("Analyzing cross-modal consistency...")
        cross_modal_consistency = self._analyze_cross_modal_consistency(
            modality_features
        )
        
        # Provenance tracing
        provenance_trace = None
        if self.enable_tracing and metadata:
            logger.info("Tracing content provenance...")
            provenance_trace = self.provenance_tracer.trace(
                metadata, modality_features
            )
        
        # Pattern analysis
        logger.info("Analyzing generative patterns...")
        pattern_signatures = self.pattern_analyzer.analyze(
            modality_features, provenance_trace
        )
        
        # Compute overall score and decision
        overall_score = self._compute_overall_score(
            modality_scores,
            cross_modal_consistency,
            pattern_signatures
        )
        
        is_fraudulent = overall_score > 0.5
        
        logger.info(f"Detection complete. Fraud score: {overall_score:.3f}")
        
        # Dynamic evaluation and alerting if enabled
        alerts = []
        signal_combination = None
        
        if self.enable_evaluation:
            logger.info("Performing dynamic evaluation...")
            
            # Classify signal severities
            signal_classifications = self._classify_signals(
                modality_scores, pattern_signatures, cross_modal_consistency
            )
            
            # Combine signals
            signal_combination = self.signal_combinator.combine_signals(
                signal_classifications, metadata
            )
            
            # Evaluate for alerts
            alerts = self.alert_engine.evaluate_signals(
                signal_classifications, metadata
            )
        
        # Update learning system if enabled
        if self.enable_learning:
            self.learner.update(
                modality_features, pattern_signatures, is_fraudulent
            )
        
        return DetectionResult(
            is_fraudulent=is_fraudulent,
            confidence=overall_score,
            modality_scores=modality_scores,
            cross_modal_consistency=cross_modal_consistency,
            provenance_trace=provenance_trace,
            pattern_signatures=pattern_signatures,
            details={
                'modality_features': modality_features,
                'metadata': metadata,
                'alerts': alerts,
                'signal_combination': signal_combination
            }
        )
    
    def _analyze_cross_modal_consistency(
        self, modality_features: Dict[str, Any]
    ) -> float:
        """
        Analyze consistency across modalities.
        
        Args:
            modality_features: Features extracted from each modality
            
        Returns:
            Consistency score (0-1, higher is more consistent)
        """
        if len(modality_features) < 2:
            return 1.0  # No inconsistency if only one modality
        
        # Simple consistency check (placeholder for actual implementation)
        # In practice, this would use semantic similarity or feature correlation
        consistency_score = 0.85  # Placeholder
        
        return consistency_score
    
    def _compute_overall_score(
        self,
        modality_scores: Dict[str, float],
        cross_modal_consistency: float,
        pattern_signatures: List[Dict[str, Any]]
    ) -> float:
        """
        Compute overall fraud score from all signals.
        
        Args:
            modality_scores: Individual modality scores
            cross_modal_consistency: Cross-modal consistency score
            pattern_signatures: Detected pattern signatures
            
        Returns:
            Overall fraud score (0-1)
        """
        if not modality_scores:
            return 0.0
        
        # Weighted average of modality scores
        weights = {
            'text': 0.25,
            'image': 0.25,
            'audio': 0.25,
            'video': 0.25
        }
        
        weighted_score = sum(
            modality_scores[mod] * weights.get(mod, 1.0/len(modality_scores))
            for mod in modality_scores.keys()
        )
        
        # Adjust for cross-modal consistency
        # Lower consistency increases fraud likelihood
        consistency_adjustment = 1.0 - cross_modal_consistency
        
        # Adjust for pattern signatures
        pattern_adjustment = len(pattern_signatures) * 0.1
        
        overall_score = (
            0.5 * weighted_score +
            0.3 * consistency_adjustment +
            0.2 * min(pattern_adjustment, 1.0)
        )
        
        return min(overall_score, 1.0)
    
    def _classify_signals(
        self,
        modality_scores: Dict[str, float],
        pattern_signatures: List[Dict[str, Any]],
        cross_modal_consistency: float
    ) -> List[Any]:
        """
        Classify all detection signals for severity evaluation.
        
        Args:
            modality_scores: Scores from modality detectors
            pattern_signatures: Pattern signatures detected
            cross_modal_consistency: Cross-modal consistency score
            
        Returns:
            List of SignalSeverity objects
        """
        from ..evaluation import SignalSeverity
        
        classified_signals = []
        
        # Classify modality signals
        for modality, score in modality_scores.items():
            if score > 0:
                severity = self.severity_classifier.classify_signal(
                    signal_type=modality,
                    score=score,
                    indicators=[f'{modality}_anomaly']
                )
                classified_signals.append(severity)
        
        # Classify pattern signatures
        for pattern in pattern_signatures:
            severity = self.severity_classifier.classify_signal(
                signal_type=pattern.get('pattern_type', 'unknown'),
                score=pattern.get('confidence', 0.0),
                indicators=pattern.get('indicators', [])
            )
            classified_signals.append(severity)
        
        # Classify cross-modal inconsistency
        if cross_modal_consistency < 0.7:
            inconsistency_score = 1.0 - cross_modal_consistency
            severity = self.severity_classifier.classify_signal(
                signal_type='cross_modal_inconsistency',
                score=inconsistency_score,
                indicators=['cross_modal_mismatch']
            )
            classified_signals.append(severity)
        
        return classified_signals


