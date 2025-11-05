"""
Base classes for modality detectors
"""

from abc import ABC, abstractmethod
from typing import Any, Union
from pathlib import Path
from dataclasses import dataclass


@dataclass
class DetectionResult:
    """Base class for detection results"""
    score: float
    features: Any
    is_suspicious: bool
    details: dict


class ModalityDetector(ABC):
    """Base class for modality-specific detectors"""
    
    def __init__(self, model_path: Union[str, Path] = None):
        """
        Initialize the detector.
        
        Args:
            model_path: Path to the detector model
        """
        self.model_path = model_path
        self.model = None
        self._load_model()
    
    @abstractmethod
    def _load_model(self):
        """Load the detection model"""
        pass
    
    @abstractmethod
    def detect(self, content: Union[str, Path]) -> DetectionResult:
        """
        Detect fraudulent patterns in content.
        
        Args:
            content: Content to analyze (string or file path)
            
        Returns:
            DetectionResult with analysis
        """
        pass
    
    @abstractmethod
    def extract_features(self, content: Union[str, Path]) -> Any:
        """
        Extract features from content.
        
        Args:
            content: Content to extract features from
            
        Returns:
            Extracted features
        """
        pass


