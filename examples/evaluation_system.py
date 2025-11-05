"""
Example demonstrating the dynamic evaluation system
"""

from src.core import MultiModalDetector
from src.evaluation import SeverityClassifier, AlertEngine, SignalCombinator
from loguru import logger

def main():
    """Demonstrate the dynamic evaluation system"""
    
    logger.info("=== Dynamic Evaluation System Demo ===")
    
    # Initialize the full detection system with evaluation enabled
    detector = MultiModalDetector(enable_evaluation=True)
    
    # Example 1: Simulated high-risk content
    logger.info("\n--- Example 1: High-Risk Fraudulent Content ---")
    
    result = detector.detect(
        text="This is clearly AI-generated content with repetitive patterns and anomalies.",
        metadata={
            'source': 'suspicious_website',
            'timestamp': '2024-01-01T00:00:00',
            'url': 'http://fraud-example.com'
        }
    )
    
    print(f"\nDetection Result:")
    print(f"  Is Fraudulent: {result.is_fraudulent}")
    print(f"  Confidence: {result.confidence:.3f}")
    
    # Display evaluation results
    if result.details.get('alerts'):
        print(f"\n  Alerts Triggered: {len(result.details['alerts'])}")
        for alert in result.details['alerts']:
            print(f"\n    Alert: {alert['name']}")
            print(f"      Level: {alert['level'].upper()}")
            print(f"      Priority: {alert['priority']}")
            print(f"      Total Risk Score: {alert['total_risk_score']:.3f}")
            print(f"      Description: {alert['description']}")
    
    if result.details.get('signal_combination'):
        combo = result.details['signal_combination']
        print(f"\n  Signal Combination:")
        print(f"    Combined Severity: {combo.combined_severity.value}")
        print(f"    Combined Risk Score: {combo.combined_risk_score:.3f}")
        print(f"    Signal Types: {combo.signal_types}")
        print(f"    Total Indicators: {combo.total_indicators}")
        print(f"    Strategy: {combo.combination_strategy}")
    
    # Example 2: Demonstrate standalone evaluation components
    logger.info("\n--- Example 2: Standalone Evaluation Components ---")
    
    # Severity Classifier
    classifier = SeverityClassifier()
    
    sample_signal = classifier.classify_signal(
        signal_type='deepfake_indicator',
        score=0.85,
        indicators=['face_warping', 'unnatural_shadows', 'temporal_artifacts']
    )
    
    print(f"\nSeverity Classification:")
    print(f"  Signal Type: {sample_signal.signal_type}")
    print(f"  Severity Level: {sample_signal.severity.value.upper()}")
    print(f"  Risk Score: {sample_signal.risk_score:.3f}")
    print(f"  Confidence: {sample_signal.confidence:.3f}")
    print(f"  Indicators: {sample_signal.indicators}")
    
    # Alert Engine
    alert_engine = AlertEngine()
    
    signals = [sample_signal]
    alerts = alert_engine.evaluate_signals(signals)
    
    print(f"\nAlert Evaluation:")
    print(f"  Signals Evaluated: {len(signals)}")
    if alerts:
        print(f"  Alerts Triggered: {len(alerts)}")
        for alert in alerts:
            print(f"    - {alert['name']} ({alert['level']})")
    else:
        print(f"  No alerts triggered (thresholds not met)")
    
    # Signal Combinator
    combinator = SignalCombinator(strategy='weighted_average')
    
    signal1 = classifier.classify_signal('text', 0.7, ['ai_patterns'])
    signal2 = classifier.classify_signal('cross_modal_inconsistency', 0.8, ['content_mismatch'])
    signal3 = classifier.classify_signal('pattern_signature', 0.6, ['gpt_pattern'])
    
    combined = combinator.combine_signals([signal1, signal2, signal3])
    
    print(f"\nSignal Combination:")
    print(f"  Strategy: {combined.combination_strategy}")
    print(f"  Combined Severity: {combined.combined_severity.value}")
    print(f"  Combined Risk Score: {combined.combined_risk_score:.3f}")
    print(f"  Signal Types: {combined.signal_types}")
    print(f"  Total Indicators: {combined.total_indicators}")
    
    logger.info("\n=== Demo Complete ===")


if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    main()

