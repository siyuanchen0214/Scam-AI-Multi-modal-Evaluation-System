"""
Severity Classifier - Classify severity level of detection signals
"""

import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


logger = logging.getLogger(__name__)


class SeverityLevel(Enum):
    """Severity levels for detection signals"""
    CRITICAL = "critical"      # Immediate threat requiring urgent action
    HIGH = "high"              # Significant threat requiring prompt action
    MEDIUM = "medium"          # Moderate threat requiring monitoring
    LOW = "low"                # Minor indicator, watch for escalation
    INFO = "info"              # Informational, no immediate action


@dataclass
class SignalSeverity:
    """Classification result for a signal"""
    signal_type: str
    severity: SeverityLevel
    confidence: float
    indicators: List[str]
    risk_score: float
    metadata: Dict[str, Any]


class SeverityClassifier:
    """
    Dynamic classifier for determining severity levels of detection signals.
    
    Adapts to evolving threat landscapes through configurable thresholds
    and machine learning techniques.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the severity classifier.
        
        Args:
            config: Configuration dictionary with severity thresholds
        """
        logger.info("Initializing severity classifier...")
        
        # Default severity thresholds
        self.thresholds = {
            'critical': {'min_score': 0.9, 'min_indicators': 3},
            'high': {'min_score': 0.7, 'min_indicators': 2},
            'medium': {'min_score': 0.5, 'min_indicators': 1},
            'low': {'min_score': 0.3, 'min_indicators': 1},
            'info': {'min_score': 0.0, 'min_indicators': 0}
        }
        
        # Load custom config if provided
        if config:
            self.thresholds.update(config.get('thresholds', {}))
        
        # Signal type weights (importance of each signal type)
        self.signal_weights = {
            'text': 1.0,
            'image': 1.0,
            'audio': 1.0,
            'video': 1.0,
            'cross_modal_inconsistency': 1.5,
            'provenance_anomaly': 1.3,
            'pattern_signature': 1.4,
            'deepfake_indicator': 2.0,
            'voice_cloning': 1.8,
            'ai_generation': 1.2
        }
        
        logger.info("Severity classifier initialized")
    
    def classify_signal(
        self,
        signal_type: str,
        score: float,
        indicators: List[str],
        metadata: Optional[Dict[str, Any]] = None
    ) -> SignalSeverity:
        """
        Classify the severity level of a detection signal.
        
        Args:
            signal_type: Type of signal (e.g., 'text', 'image', 'deepfake')
            score: Detection score (0-1)
            indicators: List of specific indicators detected
            metadata: Additional metadata about the signal
            
        Returns:
            SignalSeverity with classification result
        """
        logger.info(f"Classifying {signal_type} signal with score {score:.3f}")
        
        if metadata is None:
            metadata = {}
        
        # Calculate weighted risk score
        base_weight = self.signal_weights.get(signal_type, 1.0)
        risk_score = score * base_weight
        
        # Adjust for number of indicators
        indicator_multiplier = 1.0 + (len(indicators) * 0.1)
        risk_score *= min(indicator_multiplier, 1.5)
        
        # Determine severity level based on thresholds
        severity = self._determine_severity(score, len(indicators), risk_score)
        
        # Compute confidence based on indicators and score
        confidence = self._compute_confidence(score, indicators, severity)
        
        result = SignalSeverity(
            signal_type=signal_type,
            severity=severity,
            confidence=confidence,
            indicators=indicators,
            risk_score=risk_score,
            metadata=metadata
        )
        
        logger.info(f"Classified as {severity.value} severity (risk: {risk_score:.3f})")
        
        return result
    
    def _determine_severity(
        self, score: float, num_indicators: int, risk_score: float
    ) -> SeverityLevel:
        """
        Determine severity level based on score, indicators, and risk.
        
        Args:
            score: Detection score
            num_indicators: Number of indicators
            risk_score: Weighted risk score
            
        Returns:
            SeverityLevel
        """
        # Use both score and risk_score for classification
        combined_score = (score * 0.6) + (risk_score / 2.0)
        
        # Check thresholds in descending order
        if (combined_score >= self.thresholds['critical']['min_score'] and
            num_indicators >= self.thresholds['critical']['min_indicators']):
            return SeverityLevel.CRITICAL
        
        if (combined_score >= self.thresholds['high']['min_score'] and
            num_indicators >= self.thresholds['high']['min_indicators']):
            return SeverityLevel.HIGH
        
        if (combined_score >= self.thresholds['medium']['min_score'] and
            num_indicators >= self.thresholds['medium']['min_indicators']):
            return SeverityLevel.MEDIUM
        
        if (combined_score >= self.thresholds['low']['min_score']):
            return SeverityLevel.LOW
        
        return SeverityLevel.INFO
    
    def _compute_confidence(
        self, score: float, indicators: List[str], severity: SeverityLevel
    ) -> float:
        """
        Compute confidence level for the severity classification.
        
        Args:
            score: Detection score
            indicators: Detected indicators
            severity: Assigned severity level
            
        Returns:
            Confidence score (0-1)
        """
        # Base confidence from detection score
        base_confidence = score
        
        # Boost confidence with more indicators
        indicator_bonus = min(len(indicators) * 0.05, 0.2)
        
        # Adjust for severity level (higher severity with high indicators = more confident)
        if severity in [SeverityLevel.CRITICAL, SeverityLevel.HIGH] and len(indicators) >= 2:
            severity_bonus = 0.1
        else:
            severity_bonus = 0.0
        
        total_confidence = base_confidence + indicator_bonus + severity_bonus
        
        return min(1.0, max(0.0, total_confidence))
    
    def classify_multiple_signals(
        self, signals: List[Dict[str, Any]]
    ) -> List[SignalSeverity]:
        """
        Classify multiple signals at once.
        
        Args:
            signals: List of signal dictionaries with type, score, indicators
        
        Returns:
            List of SignalSeverity objects
        """
        classifications = []
        
        for signal in signals:
            severity = self.classify_signal(
                signal_type=signal.get('type', 'unknown'),
                score=signal.get('score', 0.0),
                indicators=signal.get('indicators', []),
                metadata=signal.get('metadata', {})
            )
            classifications.append(severity)
        
        return classifications
    
    def update_thresholds(self, new_thresholds: Dict[str, Any]):
        """
        Dynamically update severity thresholds to adapt to new threats.
        
        Args:
            new_thresholds: Dictionary with updated thresholds
        """
        logger.info("Updating severity thresholds...")
        self.thresholds.update(new_thresholds)
        logger.info(f"Thresholds updated: {new_thresholds}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about severity classifications.
        
        Returns:
            Statistics dictionary
        """
        return {
            'thresholds': self.thresholds,
            'signal_weights': self.signal_weights,
            'num_levels': len(SeverityLevel)
        }

