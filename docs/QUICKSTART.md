# Quick Start Guide

## Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd "Multi-modal Evaluation System"
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up configuration:**
```bash
cp config/.env.example config/.env
# Edit config/.env with your settings
```

## Basic Usage

### Command Line Interface

Detect fraud in text content:
```bash
python main.py --text "Sample text to analyze"
```

Detect fraud in image:
```bash
python main.py --image path/to/image.jpg
```

Multi-modal detection:
```bash
python main.py --text "text.txt" --image "image.jpg" --audio "audio.wav" --video "video.mp4"
```

### Python API

```python
from src.core import MultiModalDetector

# Initialize detector
detector = MultiModalDetector()

# Detect fraud
result = detector.detect(
    text="Your text content here",
    image="path/to/image.jpg",
    audio="path/to/audio.wav",
    video="path/to/video.mp4",
    metadata={'source': 'file', 'timestamp': '2024-01-01T00:00:00'}
)

# Check results
print(f"Fraudulent: {result.is_fraudulent}")
print(f"Confidence: {result.confidence}")
print(f"Modality Scores: {result.modality_scores}")
```

## Key Features

### 1. Multi-modal Detection
- Text: Detects AI-generated text (GPT, Claude, etc.)
- Image: Detects GAN/Deepfake images
- Audio: Detects voice cloning and audio deepfakes
- Video: Detects video deepfakes

### 2. Cross-Modal Consistency
Checks consistency across different modalities to detect fabricated narratives.

### 3. Provenance Tracing
Tracks content origin and history to detect tampering.

### 4. Pattern Analysis
Reverse-engineers generative patterns to identify the source model.

### 5. Continuous Learning
Continuously learns from new patterns and evolving generators.

## Configuration

Edit `config/detector.yaml` to customize:
- Detection thresholds
- Feature extraction settings
- Tracer options
- Learning parameters

## Running Tests

```bash
pytest tests/
```

## Project Structure

```
Multi-modal Evaluation System/
├── src/
│   ├── core/              # Core detection logic
│   ├── modalities/        # Modality-specific detectors
│   ├── tracing/           # Provenance tracing
│   ├── reverse_engineering/  # Pattern analysis
│   └── learning/          # Continuous learning
├── tests/                 # Unit tests
├── config/                # Configuration files
├── models/                # Model files
├── datasets/              # Training data
└── docs/                  # Documentation
```

## Next Steps

- Read the full documentation in `docs/`
- Explore examples in `examples/`
- Customize detection models
- Integrate with your workflow

