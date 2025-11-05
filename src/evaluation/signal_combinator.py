"""
Signal Combinator - Combine multiple signals for enhanced detection
"""

import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass

from .severity_classifier import SeverityLevel, SignalSeverity
from .alert_engine import AlertLevel


logger = logging.getLogger(__name__)


@dataclass
class SignalCombination:
    """Result of combining multiple signals"""
    combined_risk_score: float
    combined_severity: SeverityLevel
    signal_types: List[str]
    total_indicators: int
    confidence: float
    combination_strategy: str
    details: Dict[str, Any]


class SignalCombinator:
    """
    Combines multiple detection signals to provide enhanced,
    robust fraud detection performance.
    
    Implements various combination strategies to maximize
    detection accuracy while minimizing false positives.
    """
    
    def __init__(self, strategy: str = 'weighted_average'):
        """
        Initialize the signal combinator.
        
        Args:
            strategy: Combination strategy ('weighted_average', 'maximum', 'majority')
        """
        logger.info(f"Initializing signal combinator with strategy: {strategy}")
        
        self.strategy = strategy
        
        # Signal type importance weights
        self.importance_weights = {
            'cross_modal_inconsistency': 1.5,
            'deepfake_indicator': 2.0,
            'voice_cloning': 1.8,
            'pattern_signature': 1.4,
            'provenance_anomaly': 1.3,
            'text': 1.0,
            'image': 1.0,
            'audio': 1.0,
            'video': 1.0,
            'ai_generation': 1.2
        }
        
        logger.info("Signal combinator initialized")
    
    def combine_signals(
        self,
        signals: List[SignalSeverity],
        context: Optional[Dict[str, Any]] = None
    ) -> SignalCombination:
        """
        Combine multiple signals into a unified assessment.
        
        Args:
            signals: List of signal severities to combine
            context: Additional context about the detection
            
        Returns:
            SignalCombination with combined assessment
        """
        if not signals:
            return self._create_empty_combination()
        
        logger.info(f"Combining {len(signals)} signals using {self.strategy} strategy")
        
        # Apply combination strategy
        if self.strategy == 'weighted_average':
            result = self._weighted_average_combination(signals)
        elif self.strategy == 'maximum':
            result = self._maximum_combination(signals)
        elif self.strategy == 'majority':
            result = self._majority_vote_combination(signals)
        else:
            logger.warning(f"Unknown strategy {self.strategy}, using weighted_average")
            result = self._weighted_average_combination(signals)
        
        result.details = self._compute_details(signals, context)
        
        logger.info(f"Combined result: severity={result.combined_severity.value}, "
                   f"risk={result.combined_risk_score:.3f}")
        
        return result
    
    def _weighted_average_combination(
        self, signals: List[SignalSeverity]
    ) -> SignalCombination:
        """Combine signals using weighted average"""
        # Calculate weighted average of risk scores
        total_weighted_risk = 0.0
        total_weight = 0.0
        
        all_indicators = []
        signal_types = []
        
        for signal in signals:
            weight = self.importance_weights.get(signal.signal_type, 1.0)
            weighted_risk = signal.risk_score * weight
            
            total_weighted_risk += weighted_risk
            total_weight += weight
            all_indicators.extend(signal.indicators)
            signal_types.append(signal.signal_type)
        
        combined_risk = total_weighted_risk / total_weight if total_weight > 0 else 0.0
        
        # Determine combined severity based on risk score
        combined_severity = self._risk_to_severity(combined_risk)
        
        # Calculate confidence (average of signal confidences)
        avg_confidence = sum(s.confidence for s in signals) / len(signals)
        
        return SignalCombination(
            combined_risk_score=combined_risk,
            combined_severity=combined_severity,
            signal_types=list(set(signal_types)),
            total_indicators=len(set(all_indicators)),
            confidence=avg_confidence,
            combination_strategy='weighted_average',
            details={}
        )
    
    def _maximum_combination(
        self, signals: List[SignalSeverity]
    ) -> SignalCombination:
        """Combine signals using maximum (worst-case) severity"""
        max_severity = max(signals, key=lambda s: s.risk_score)
        
        all_indicators = []
        signal_types = []
        for signal in signals:
            all_indicators.extend(signal.indicators)
            signal_types.append(signal.signal_type)
        
        return SignalCombination(
            combined_risk_score=max_severity.risk_score,
            combined_severity=max_severity.severity,
            signal_types=list(set(signal_types)),
            total_indicators=len(set(all_indicators)),
            confidence=max_severity.confidence,
            combination_strategy='maximum',
            details={'max_signal': max_severity.signal_type}
        )
    
    def _majority_vote_combination(
        self, signals: List[SignalSeverity]
    ) -> SignalCombination:
        """Combine signals using majority vote on severity level"""
        severity_counts = {}
        for signal in signals:
            severity = signal.severity
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        # Get most common severity
        combined_severity = max(severity_counts, key=severity_counts.get)
        
        # Calculate average risk for signals with this severity
        matching_signals = [s for s in signals if s.severity == combined_severity]
        avg_risk = sum(s.risk_score for s in matching_signals) / len(matching_signals)
        
        all_indicators = []
        signal_types = []
        for signal in signals:
            all_indicators.extend(signal.indicators)
            signal_types.append(signal.signal_type)
        
        return SignalCombination(
            combined_risk_score=avg_risk,
            combined_severity=combined_severity,
            signal_types=list(set(signal_types)),
            total_indicators=len(set(all_indicators)),
            confidence=severity_counts[combined_severity] / len(signals),
            combination_strategy='majority_vote',
            details={'severity_distribution': {k.value: v for k, v in severity_counts.items()}}
        )
    
    def _risk_to_severity(self, risk_score: float) -> SeverityLevel:
        """Convert risk score to severity level"""
        if risk_score >= 2.5:
            return SeverityLevel.CRITICAL
        elif risk_score >= 1.8:
            return SeverityLevel.HIGH
        elif risk_score >= 1.2:
            return SeverityLevel.MEDIUM
        elif risk_score >= 0.5:
            return SeverityLevel.LOW
        else:
            return SeverityLevel.INFO
    
    def _create_empty_combination(self) -> SignalCombination:
        """Create an empty combination result"""
        return SignalCombination(
            combined_risk_score=0.0,
            combined_severity=SeverityLevel.INFO,
            signal_types=[],
            total_indicators=0,
            confidence=0.0,
            combination_strategy=self.strategy,
            details={}
        )
    
    def _compute_details(
        self,
        signals: List[SignalSeverity],
        context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Compute additional details about the combination"""
        details = {
            'num_signals': len(signals),
            'severity_breakdown': {}
        }
        
        for level in SeverityLevel:
            count = sum(1 for s in signals if s.severity == level)
            details['severity_breakdown'][level.value] = count
        
        if context:
            details['context'] = context
        
        return details
    
    def set_strategy(self, strategy: str):
        """
        Change the combination strategy dynamically.
        
        Args:
            strategy: New strategy to use
        """
        valid_strategies = ['weighted_average', 'maximum', 'majority']
        if strategy in valid_strategies:
            self.strategy = strategy
            logger.info(f"Combination strategy changed to: {strategy}")
        else:
            logger.warning(f"Invalid strategy: {strategy}. Valid options: {valid_strategies}")

