"""
Provenance Tracer - Track content origin and history
"""

import logging
import hashlib
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime


logger = logging.getLogger(__name__)


@dataclass
class ProvenanceTrace:
    """Trace of content provenance"""
    content_hash: str
    origin: str
    metadata: Dict[str, Any]
    history: List[Dict[str, Any]]
    confidence: float
    inconsistencies: List[str]


class ProvenanceTracer:
    """
    Tracer for tracking content provenance and detecting inconsistencies.
    
    Tracks:
    - Content origin and source
    - Modification history
    - Cross-modal consistency
    - Metadata authenticity
    """
    
    def __init__(self):
        """Initialize the provenance tracer"""
        logger.info("Initializing provenance tracer...")
        self.content_registry = {}  # Store content hashes and metadata
    
    def trace(
        self,
        metadata: Dict[str, Any],
        modality_features: Dict[str, Any] = None
    ) -> ProvenanceTrace:
        """
        Trace content provenance.
        
        Args:
            metadata: Content metadata (source, timestamp, etc.)
            modality_features: Features from different modalities
            
        Returns:
            ProvenanceTrace with origin and history
        """
        logger.info("Tracing content provenance...")
        
        # Generate content hash
        content_hash = self._generate_hash(metadata, modality_features)
        
        # Extract origin information
        origin = self._extract_origin(metadata)
        
        # Build history
        history = self._build_history(metadata, modality_features)
        
        # Check for inconsistencies
        inconsistencies = self._check_inconsistencies(
            metadata, modality_features
        )
        
        # Compute confidence
        confidence = self._compute_confidence(
            metadata, inconsistencies, modality_features
        )
        
        trace = ProvenanceTrace(
            content_hash=content_hash,
            origin=origin,
            metadata=metadata,
            history=history,
            confidence=confidence,
            inconsistencies=inconsistencies
        )
        
        # Store in registry
        self.content_registry[content_hash] = trace
        
        logger.info(f"Provenance trace complete. Confidence: {confidence:.3f}")
        
        return trace
    
    def _generate_hash(
        self,
        metadata: Dict[str, Any],
        modality_features: Dict[str, Any] = None
    ) -> str:
        """
        Generate hash for content tracking.
        
        Args:
            metadata: Content metadata
            modality_features: Modality features
            
        Returns:
            Content hash string
        """
        # Combine metadata and features into hashable string
        hash_content = str(metadata)
        if modality_features:
            hash_content += str(modality_features)
        
        # Generate SHA-256 hash
        hash_obj = hashlib.sha256(hash_content.encode('utf-8'))
        return hash_obj.hexdigest()
    
    def _extract_origin(self, metadata: Dict[str, Any]) -> str:
        """
        Extract origin information from metadata.
        
        Args:
            metadata: Content metadata
            
        Returns:
            Origin string
        """
        # Extract origin information
        sources = [
            metadata.get('source'),
            metadata.get('creator'),
            metadata.get('camera'),
            metadata.get('device'),
            metadata.get('software'),
        ]
        
        # Find first non-None source
        origin = next((s for s in sources if s is not None), 'unknown')
        
        return origin
    
    def _build_history(
        self,
        metadata: Dict[str, Any],
        modality_features: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """
        Build content history.
        
        Args:
            metadata: Content metadata
            modality_features: Modality features
            
        Returns:
            List of history entries
        """
        history = []
        
        # Add creation timestamp
        if 'timestamp' in metadata:
            history.append({
                'event': 'created',
                'timestamp': metadata['timestamp'],
                'source': metadata.get('source', 'unknown')
            })
        
        # Add modifications if present
        if 'modifications' in metadata:
            for mod in metadata['modifications']:
                history.append(mod)
        
        # Add detection timestamp
        history.append({
            'event': 'detected',
            'timestamp': datetime.now().isoformat(),
            'analyst': 'multi_modal_detector'
        })
        
        return history
    
    def _check_inconsistencies(
        self,
        metadata: Dict[str, Any],
        modality_features: Dict[str, Any] = None
    ) -> List[str]:
        """
        Check for provenance inconsistencies.
        
        Args:
            metadata: Content metadata
            modality_features: Modality features
            
        Returns:
            List of detected inconsistencies
        """
        inconsistencies = []
        
        # Check timestamp consistency
        if self._has_timestamp_inconsistencies(metadata):
            inconsistencies.append("Timestamp inconsistencies detected")
        
        # Check metadata validity
        if self._has_invalid_metadata(metadata):
            inconsistencies.append("Invalid or suspicious metadata")
        
        # Check cross-modal consistency if features provided
        if modality_features and self._has_cross_modal_inconsistencies(
            metadata, modality_features
        ):
            inconsistencies.append("Cross-modal inconsistencies detected")
        
        # Check for known suspicious patterns
        if self._has_suspicious_patterns(metadata):
            inconsistencies.append("Suspicious provenance patterns detected")
        
        return inconsistencies
    
    def _has_timestamp_inconsistencies(self, metadata: Dict[str, Any]) -> bool:
        """Check for timestamp inconsistencies"""
        # Check if timestamp is in the future
        if 'timestamp' in metadata:
            try:
                ts = datetime.fromisoformat(metadata['timestamp'])
                if ts > datetime.now():
                    return True
            except:
                pass
        
        return False
    
    def _has_invalid_metadata(self, metadata: Dict[str, Any]) -> bool:
        """Check for invalid metadata"""
        # Check for missing critical fields
        if 'timestamp' not in metadata:
            return True
        
        # Check for suspicious metadata values
        if 'source' in metadata and metadata['source'] in ['unknown', 'anonymous']:
            return True
        
        return False
    
    def _has_cross_modal_inconsistencies(
        self,
        metadata: Dict[str, Any],
        modality_features: Dict[str, Any]
    ) -> bool:
        """Check for cross-modal inconsistencies"""
        # Placeholder: Check if features match metadata claims
        # e.g., if metadata says "natural photo" but features show AI generation
        return False
    
    def _has_suspicious_patterns(self, metadata: Dict[str, Any]) -> bool:
        """Check for known suspicious patterns"""
        # Check for patterns commonly seen in fraudulent content
        suspicious_patterns = ['test', 'sample', 'fake']
        
        metadata_str = str(metadata).lower()
        return any(pattern in metadata_str for pattern in suspicious_patterns)
    
    def _compute_confidence(
        self,
        metadata: Dict[str, Any],
        inconsistencies: List[str],
        modality_features: Dict[str, Any] = None
    ) -> float:
        """
        Compute confidence in provenance trace.
        
        Args:
            metadata: Content metadata
            inconsistencies: Detected inconsistencies
            modality_features: Modality features
            
        Returns:
            Confidence score (0-1)
        """
        confidence = 1.0
        
        # Reduce confidence for inconsistencies
        confidence -= len(inconsistencies) * 0.2
        
        # Reduce confidence for missing metadata
        if 'source' not in metadata:
            confidence -= 0.3
        
        # Reduce confidence for suspicious origins
        if metadata.get('source') in ['unknown', 'anonymous', 'test']:
            confidence -= 0.3
        
        return max(0.0, min(1.0, confidence))
    
    def verify_chain(self, trace: ProvenanceTrace) -> bool:
        """
        Verify the complete provenance chain.
        
        Args:
            trace: Provenance trace to verify
            
        Returns:
            True if chain is valid
        """
        # Check if all history entries are consistent
        for i, entry in enumerate(trace.history[:-1]):
            next_entry = trace.history[i + 1]
            
            # Timestamps should be monotonic
            if entry.get('timestamp') and next_entry.get('timestamp'):
                try:
                    ts1 = datetime.fromisoformat(entry['timestamp'])
                    ts2 = datetime.fromisoformat(next_entry['timestamp'])
                    if ts1 > ts2:
                        logger.warning("Non-monotonic timestamps in provenance chain")
                        return False
                except:
                    pass
        
        # Check for missing critical events
        events = [entry.get('event') for entry in trace.history]
        if 'created' not in events:
            logger.warning("Missing 'created' event in provenance chain")
            return False
        
        return True


