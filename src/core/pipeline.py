"""
Detection Pipeline - Orchestrate the complete detection workflow
"""

import logging
from typing import Dict, Any, Optional
from pathlib import Path

from .detector import MultiModalDetector, DetectionResult


logger = logging.getLogger(__name__)


class DetectionPipeline:
    """
    Complete detection pipeline that orchestrates all components.
    
    Workflow:
    1. Load configuration
    2. Initialize detectors
    3. Process input content
    4. Perform multi-modal analysis
    5. Generate report
    """
    
    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize the detection pipeline.
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = config_path
        
        # Initialize main detector
        logger.info("Initializing detection pipeline...")
        self.detector = MultiModalDetector(
            config_path=config_path,
            enable_tracing=True,
            enable_learning=True
        )
        
        logger.info("Detection pipeline initialized")
    
    def process(
        self,
        text: Optional[str] = None,
        image: Optional[str] = None,
        audio: Optional[str] = None,
        video: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> DetectionResult:
        """
        Process content through the complete detection pipeline.
        
        Args:
            text: Text content
            image: Image path
            audio: Audio path
            video: Video path
            metadata: Content metadata
            
        Returns:
            Detection result
        """
        logger.info("Starting pipeline processing...")
        
        # Run detection
        result = self.detector.detect(
            text=text,
            image=image,
            audio=audio,
            video=video,
            metadata=metadata
        )
        
        # Generate report
        self._generate_report(result)
        
        logger.info("Pipeline processing complete")
        
        return result
    
    def _generate_report(self, result: DetectionResult):
        """
        Generate detection report.
        
        Args:
            result: Detection result
        """
        logger.info("Generating detection report...")
        
        # Print summary
        print("\n" + "="*60)
        print("DETECTION REPORT")
        print("="*60)
        print(f"Is Fraudulent: {result.is_fraudulent}")
        print(f"Confidence: {result.confidence:.3f}")
        print(f"\nModality Scores:")
        for modality, score in result.modality_scores.items():
            print(f"  {modality}: {score:.3f}")
        print(f"\nCross-Modal Consistency: {result.cross_modal_consistency:.3f}")
        
        if result.provenance_trace:
            print(f"\nProvenance:")
            print(f"  Origin: {result.provenance_trace.get('origin', 'unknown')}")
            print(f"  Confidence: {result.provenance_trace.get('confidence', 0):.3f}")
        
        if result.pattern_signatures:
            print(f"\nDetected Patterns:")
            for sig in result.pattern_signatures:
                print(f"  - {sig.get('pattern_type', 'unknown')}")
                print(f"    Confidence: {sig.get('confidence', 0):.3f}")
        
        print("="*60 + "\n")

