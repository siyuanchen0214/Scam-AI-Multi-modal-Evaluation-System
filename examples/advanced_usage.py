"""
Advanced usage example showing provenance tracing and pattern analysis
"""

from src.core import MultiModalDetector
from src.tracing import ProvenanceTracer
from src.reverse_engineering import PatternAnalyzer
from loguru import logger

def main():
    """Demonstrate advanced features"""
    
    logger.info("Initializing advanced detection components...")
    
    # Initialize components
    detector = MultiModalDetector()
    
    # Example: Text with provenance tracing
    logger.info("\n=== Advanced Analysis ===")
    
    text = """
    This text demonstrates how the system analyzes content for fraud indicators.
    The system can detect patterns that indicate AI generation or manipulation.
    Repeated phrases and statistical anomalies are key indicators.
    """
    
    result = detector.detect(
        text=text,
        metadata={
            'source': 'test',
            'timestamp': '2024-01-01T00:00:00',
            'creator': 'user',
            'device': 'computer'
        }
    )
    
    print("\nDetailed Analysis Results:")
    print(f"Fraudulent: {result.is_fraudulent}")
    print(f"Confidence Score: {result.confidence:.3f}")
    
    print(f"\nModality Scores:")
    for modality, score in result.modality_scores.items():
        print(f"  {modality}: {score:.3f}")
    
    if result.provenance_trace:
        print(f"\nProvenance Trace:")
        print(f"  Origin: {result.provenance_trace.origin}")
        print(f"  Confidence: {result.provenance_trace.confidence:.3f}")
        print(f"  Inconsistencies: {result.provenance_trace.inconsistencies}")
    
    if result.pattern_signatures:
        print(f"\nDetected Pattern Signatures:")
        for sig in result.pattern_signatures:
            print(f"  - {sig.pattern_type}")
            print(f"    Confidence: {sig.confidence:.3f}")
            print(f"    Indicators: {sig.indicators}")
    
    if result.cross_modal_consistency:
        print(f"\nCross-Modal Consistency: {result.cross_modal_consistency:.3f}")
    
    logger.info("\nAdvanced analysis completed!")


if __name__ == "__main__":
    main()

