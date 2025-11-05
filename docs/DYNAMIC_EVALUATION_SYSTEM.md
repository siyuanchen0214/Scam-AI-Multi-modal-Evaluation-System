# Dynamic Evaluation System

## Overview

The Dynamic Evaluation System is a comprehensive framework for classifying the severity level of detection signals and determining which combinations of signals should trigger alerts for potentially fraudulent content. This system provides both flexibility and scalability, ensuring robust performance under rapidly evolving threat landscapes.

## Key Components

### 1. Severity Classifier

Classifies individual detection signals into severity levels based on multiple factors.

**Severity Levels:**
- **CRITICAL**: Immediate threat requiring urgent action
- **HIGH**: Significant threat requiring prompt action
- **MEDIUM**: Moderate threat requiring monitoring
- **LOW**: Minor indicator, watch for escalation
- **INFO**: Informational, no immediate action

**Features:**
- Configurable thresholds for each severity level
- Weighted risk scoring based on signal type
- Dynamic threshold adjustment for evolving threats
- Confidence scoring based on indicators

**Usage:**
```python
from src.evaluation import SeverityClassifier, SeverityLevel

classifier = SeverityClassifier()

severity = classifier.classify_signal(
    signal_type='deepfake_indicator',
    score=0.85,
    indicators=['face_warping', 'unnatural_shadows', 'temporal_artifacts']
)

print(f"Severity: {severity.severity.value}")  # Output: critical
print(f"Risk Score: {severity.risk_score:.3f}")  # Output: 2.210
```

### 2. Alert Engine

Determines which signal combinations should trigger alerts.

**Alert Levels:**
- **EMERGENCY**: Immediate action required
- **URGENT**: High priority action needed
- **WARNING**: Action recommended
- **NOTICE**: Monitoring recommended
- **INFO**: Informational only

**Default Alert Rules:**

1. **Emergency - Critical Multi-Signal**: Critical severity with multiple strong indicators
2. **Urgent - Cross-Modal Inconsistency**: High severity cross-modal inconsistencies
3. **Urgent - Multiple High Severity**: Multiple high severity signals
4. **Warning - Provenance Anomaly**: Provenance anomalies detected
5. **Warning - Multiple Pattern Signatures**: Multiple generative patterns detected
6. **Notice - Moderate Indicators**: Multiple moderate severity indicators

**Usage:**
```python
from src.evaluation import AlertEngine

alert_engine = AlertEngine()
alerts = alert_engine.evaluate_signals(signals)

for alert in alerts:
    print(f"Alert: {alert['name']}")
    print(f"Level: {alert['level']}")
    print(f"Total Risk Score: {alert['total_risk_score']:.3f}")
```

### 3. Signal Combinator

Combines multiple signals using various strategies for enhanced detection.

**Combination Strategies:**

1. **Weighted Average** (default): Averages risk scores weighted by signal importance
2. **Maximum**: Takes the worst-case (maximum) severity
3. **Majority Vote**: Determines severity based on majority of signals

**Signal Importance Weights:**
- Deepfake indicators: 2.0x
- Voice cloning: 1.8x
- Cross-modal inconsistency: 1.5x
- Pattern signatures: 1.4x
- Provenance anomalies: 1.3x
- AI generation: 1.2x
- Standard modalities: 1.0x

**Usage:**
```python
from src.evaluation import SignalCombinator

combinator = SignalCombinator(strategy='weighted_average')
combined = combinator.combine_signals([signal1, signal2, signal3])

print(f"Combined Severity: {combined.combined_severity.value}")
print(f"Combined Risk Score: {combined.combined_risk_score:.3f}")
```

## Integration with Main Detector

The evaluation system is fully integrated with the MultiModalDetector:

```python
from src.core import MultiModalDetector

# Initialize with evaluation enabled (default)
detector = MultiModalDetector(enable_evaluation=True)

# Detect content
result = detector.detect(
    text="Suspicious content",
    image="image.jpg",
    metadata={'source': 'website'}
)

# Access evaluation results
if result.details.get('alerts'):
    print(f"Alerts triggered: {len(result.details['alerts'])}")
    for alert in result.details['alerts']:
        print(f"  - {alert['name']} ({alert['level']})")

if result.details.get('signal_combination'):
    combo = result.details['signal_combination']
    print(f"Combined severity: {combo.combined_severity.value}")
```

## Dynamic Configuration

### Custom Alert Rules

Add custom rules to adapt to new threats:

```python
def custom_crypto_scam_condition(signals):
    """Custom condition for cryptocurrency scam detection"""
    patterns = [s for s in signals if 'pattern' in s.signal_type]
    provenances = [s for s in signals if 'provenance' in s.signal_type]
    return len(patterns) >= 2 and len(provenances) >= 1

alert_engine.add_custom_rule(
    name="Custom - Crypto Scam Pattern",
    condition=custom_crypto_scam_condition,
    alert_level=AlertLevel.URGENT,
    priority=9,
    description="Detects cryptocurrency scam patterns"
)
```

### Threshold Adjustment

Adapt to evolving threats by updating thresholds:

```python
# Update severity thresholds
classifier.update_thresholds({
    'critical': {'min_score': 0.95, 'min_indicators': 4},
    'high': {'min_score': 0.75, 'min_indicators': 3}
})

# Update alert thresholds
new_threshold = AlertThreshold(
    required_severities={SeverityLevel.CRITICAL, SeverityLevel.HIGH},
    min_signals=3,
    min_risk_score=2.5,
    alert_level=AlertLevel.EMERGENCY,
    description="New emergency threshold"
)
alert_engine.update_thresholds({'emergency_strict': new_threshold})
```

### Strategy Selection

Switch combination strategies dynamically:

```python
# Change to maximum severity strategy for high-security scenarios
combinator.set_strategy('maximum')
```

## Use Cases

### 1. Financial Fraud Detection

```python
# Financial scams often have multiple high-severity signals
result = detector.detect(
    text=scam_email,
    image=company_logo,
    metadata={'url': 'phishing-site.com'}
)

# Check for urgent alerts
for alert in result.details.get('alerts', []):
    if alert['level'] in ['urgent', 'emergency']:
        block_content()
        notify_security_team()
```

### 2. Deepfake Detection

```python
# Deepfakes typically have strong video + audio signals
result = detector.detect(
    video=video_file,
    audio=audio_file
)

# Look for combination of deepfake indicators
if result.details.get('signal_combination'):
    combo = result.details['signal_combination']
    if 'deepfake_indicator' in combo.signal_types:
        flag_for_review()
```

### 3. Advertising Fraud

```python
# Fake ads often have cross-modal inconsistencies
result = detector.detect(
    text=ad_copy,
    image=ad_image,
    metadata={'source': 'ad_network'}
)

# Trigger on cross-modal mismatches
for alert in result.details.get('alerts', []):
    if 'cross_modal' in alert['description'].lower():
        reject_ad()
```

## Benefits

### 1. Flexibility
- Configurable rules and thresholds
- Custom alert conditions
- Multiple combination strategies

### 2. Scalability
- Handles large volumes of signals
- Efficient evaluation algorithms
- Real-time processing

### 3. Robustness
- Adapts to evolving threats
- Reduces false positives through combination logic
- Provides confidence scores for decision-making

### 4. National Security Impact
- Protects consumers from fraud
- Safeguards financial systems
- Maintains digital trust in the age of generative AI
- Supports U.S. cybersecurity efforts

## Performance Metrics

- **Severity Classification**: ~1-5ms per signal
- **Alert Evaluation**: ~5-15ms for typical signal sets
- **Signal Combination**: ~1-3ms per combination
- **Memory Usage**: ~50-100MB for evaluation components

## Best Practices

1. **Start with defaults**: The default rules and thresholds are well-tuned for general use
2. **Monitor performance**: Track false positive/negative rates and adjust thresholds
3. **Update regularly**: Refresh thresholds as new threats emerge
4. **Test thoroughly**: Validate custom rules before deployment
5. **Combine strategies**: Use different strategies for different content types

## Future Enhancements

- Machine learning-based threshold optimization
- Automated rule generation from threat intelligence
- Real-time threat adaptation
- Integration with threat intelligence feeds
- Multi-tenancy support for different organizational needs

