"""
Alert Engine - Determine which signal combinations trigger alerts
"""

import logging
from typing import Dict, List, Any, Optional, Set, Callable
from dataclasses import dataclass
from enum import Enum

from .severity_classifier import SeverityLevel, SignalSeverity


logger = logging.getLogger(__name__)


class AlertLevel(Enum):
    """Alert levels for triggered alerts"""
    EMERGENCY = "emergency"    # Immediate action required
    URGENT = "urgent"         # High priority action needed
    WARNING = "warning"       # Action recommended
    NOTICE = "notice"         # Monitoring recommended
    INFO = "info"             # Informational only


@dataclass
class AlertThreshold:
    """Threshold configuration for alert triggering"""
    required_severities: Set[SeverityLevel]
    min_signals: int
    min_risk_score: float
    alert_level: AlertLevel
    description: str


@dataclass
class AlertRule:
    """Rule for evaluating signal combinations"""
    name: str
    condition: Callable[[List[SignalSeverity]], bool]
    alert_level: AlertLevel
    priority: int  # Higher priority rules checked first
    description: str


class AlertEngine:
    """
    Dynamic alert engine that determines which combinations of signals
    should trigger alerts for potentially fraudulent content.
    
    Provides flexibility and scalability through configurable rules.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the alert engine.
        
        Args:
            config: Configuration dictionary with alert rules
        """
        logger.info("Initializing alert engine...")
        
        # Default alert rules
        self.rules = self._initialize_default_rules()
        
        # Alert thresholds
        self.thresholds = self._initialize_thresholds()
        
        # Load custom config if provided
        if config:
            self.rules.extend(config.get('custom_rules', []))
            self.thresholds.update(config.get('thresholds', {}))
        
        logger.info(f"Alert engine initialized with {len(self.rules)} rules")
    
    def _initialize_default_rules(self) -> List[AlertRule]:
        """Initialize default alert rules"""
        rules = []
        
        # Emergency: Critical severity with multiple strong indicators
        def emergency_condition(signals: List[SignalSeverity]) -> bool:
            critical_count = sum(1 for s in signals if s.severity == SeverityLevel.CRITICAL)
            high_count = sum(1 for s in signals if s.severity == SeverityLevel.HIGH)
            return critical_count >= 1 and (critical_count + high_count) >= 2
        
        rules.append(AlertRule(
            name="Emergency - Critical Multi-Signal",
            condition=emergency_condition,
            alert_level=AlertLevel.EMERGENCY,
            priority=10,
            description="Critical severity signals with multiple indicators"
        ))
        
        # Urgent: High cross-modal inconsistency
        def urgent_cross_modal(signals: List[SignalSeverity]) -> bool:
            cross_modal = [s for s in signals if 'cross_modal' in s.signal_type.lower()]
            return any(s.severity in [SeverityLevel.HIGH, SeverityLevel.CRITICAL] 
                      for s in cross_modal)
        
        rules.append(AlertRule(
            name="Urgent - Cross-Modal Inconsistency",
            condition=urgent_cross_modal,
            alert_level=AlertLevel.URGENT,
            priority=9,
            description="High severity cross-modal inconsistencies detected"
        ))
        
        # Urgent: Multiple high severity signals
        def urgent_multi_high(signals: List[SignalSeverity]) -> bool:
            high_count = sum(1 for s in signals if s.severity == SeverityLevel.HIGH)
            return high_count >= 3
        
        rules.append(AlertRule(
            name="Urgent - Multiple High Severity",
            condition=urgent_multi_high,
            alert_level=AlertLevel.URGENT,
            priority=8,
            description="Multiple high severity signals detected"
        ))
        
        # Warning: Provenance anomalies
        def warning_provenance(signals: List[SignalSeverity]) -> bool:
            provenance = [s for s in signals if 'provenance' in s.signal_type.lower()]
            return any(s.severity in [SeverityLevel.MEDIUM, SeverityLevel.HIGH] 
                      for s in provenance)
        
        rules.append(AlertRule(
            name="Warning - Provenance Anomaly",
            condition=warning_provenance,
            alert_level=AlertLevel.WARNING,
            priority=7,
            description="Provenance anomalies detected"
        ))
        
        # Warning: Pattern signatures detected
        def warning_patterns(signals: List[SignalSeverity]) -> bool:
            patterns = [s for s in signals if 'pattern' in s.signal_type.lower()]
            return len(patterns) >= 2
        
        rules.append(AlertRule(
            name="Warning - Multiple Pattern Signatures",
            condition=warning_patterns,
            alert_level=AlertLevel.WARNING,
            priority=6,
            description="Multiple generative pattern signatures detected"
        ))
        
        # Notice: Moderate threat indicators
        def notice_moderate(signals: List[SignalSeverity]) -> bool:
            medium_count = sum(1 for s in signals if s.severity == SeverityLevel.MEDIUM)
            return medium_count >= 2
        
        rules.append(AlertRule(
            name="Notice - Moderate Indicators",
            condition=notice_moderate,
            alert_level=AlertLevel.NOTICE,
            priority=5,
            description="Multiple moderate severity indicators"
        ))
        
        # Sort rules by priority (highest first)
        rules.sort(key=lambda r: r.priority, reverse=True)
        
        return rules
    
    def _initialize_thresholds(self) -> Dict[str, AlertThreshold]:
        """Initialize alert thresholds"""
        return {
            'emergency': AlertThreshold(
                required_severities={SeverityLevel.CRITICAL},
                min_signals=2,
                min_risk_score=2.0,
                alert_level=AlertLevel.EMERGENCY,
                description="Emergency alert threshold"
            ),
            'urgent': AlertThreshold(
                required_severities={SeverityLevel.HIGH, SeverityLevel.CRITICAL},
                min_signals=2,
                min_risk_score=1.5,
                alert_level=AlertLevel.URGENT,
                description="Urgent alert threshold"
            ),
            'warning': AlertThreshold(
                required_severities={SeverityLevel.MEDIUM, SeverityLevel.HIGH},
                min_signals=2,
                min_risk_score=1.0,
                alert_level=AlertLevel.WARNING,
                description="Warning alert threshold"
            )
        }
    
    def evaluate_signals(
        self,
        signals: List[SignalSeverity],
        context: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Evaluate signal combinations and determine which alerts to trigger.
        
        Args:
            signals: List of classified signal severities
            context: Additional context about the detection
            
        Returns:
            List of alert dictionaries
        """
        logger.info(f"Evaluating {len(signals)} signals for alert triggers")
        
        triggered_alerts = []
        
        # Check each rule in priority order
        for rule in self.rules:
            if rule.condition(signals):
                alert = self._create_alert(rule, signals, context)
                triggered_alerts.append(alert)
                logger.info(f"Alert triggered: {rule.name}")
        
        # If no rule matched, check threshold-based alerts
        if not triggered_alerts:
            threshold_alerts = self._check_thresholds(signals)
            triggered_alerts.extend(threshold_alerts)
        
        # Sort alerts by priority
        triggered_alerts.sort(key=lambda a: a['priority'], reverse=True)
        
        return triggered_alerts
    
    def _create_alert(
        self,
        rule: AlertRule,
        signals: List[SignalSeverity],
        context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Create an alert from a matched rule"""
        # Calculate aggregate metrics
        total_risk = sum(s.risk_score for s in signals)
        severity_distribution = {}
        for level in SeverityLevel:
            severity_distribution[level.value] = sum(
                1 for s in signals if s.severity == level
            )
        
        alert = {
            'name': rule.name,
            'level': rule.alert_level.value,
            'priority': rule.priority,
            'description': rule.description,
            'triggered_at': self._get_timestamp(),
            'signal_count': len(signals),
            'total_risk_score': total_risk,
            'severity_distribution': severity_distribution,
            'signals': [
                {
                    'type': s.signal_type,
                    'severity': s.severity.value,
                    'risk_score': s.risk_score,
                    'indicators': s.indicators
                }
                for s in signals
            ],
            'context': context or {}
        }
        
        return alert
    
    def _check_thresholds(
        self, signals: List[SignalSeverity]
    ) -> List[Dict[str, Any]]:
        """Check if signals meet any threshold criteria"""
        alerts = []
        
        # Calculate total risk score
        total_risk = sum(s.risk_score for s in signals)
        
        # Check each threshold
        for threshold_name, threshold in self.thresholds.items():
            # Count signals meeting required severity
            matching_severities = [
                s for s in signals if s.severity in threshold.required_severities
            ]
            
            # Check if threshold is met
            if (len(matching_severities) >= threshold.min_signals and
                total_risk >= threshold.min_risk_score):
                
                alert = {
                    'name': f'Threshold Alert: {threshold_name}',
                    'level': threshold.alert_level.value,
                    'priority': threshold.alert_level.value == 'emergency' and 10 or 5,
                    'description': threshold.description,
                    'triggered_at': self._get_timestamp(),
                    'signal_count': len(signals),
                    'total_risk_score': total_risk,
                    'threshold_met': threshold_name,
                    'context': {}
                }
                alerts.append(alert)
                logger.info(f"Threshold alert triggered: {threshold_name}")
        
        return alerts
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def add_custom_rule(
        self,
        name: str,
        condition: Callable[[List[SignalSeverity]], bool],
        alert_level: AlertLevel,
        priority: int,
        description: str
    ):
        """
        Add a custom alert rule dynamically.
        
        Args:
            name: Rule name
            condition: Function that evaluates signals
            alert_level: Alert level to trigger
            priority: Priority level (higher = checked first)
            description: Rule description
        """
        rule = AlertRule(
            name=name,
            condition=condition,
            alert_level=alert_level,
            priority=priority,
            description=description
        )
        
        self.rules.append(rule)
        self.rules.sort(key=lambda r: r.priority, reverse=True)
        
        logger.info(f"Custom rule added: {name}")
    
    def update_thresholds(self, new_thresholds: Dict[str, AlertThreshold]):
        """Update alert thresholds dynamically"""
        self.thresholds.update(new_thresholds)
        logger.info(f"Alert thresholds updated")

