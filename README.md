# My App

A Streamlit application that allows users to upload a fundus image and create a printable net which can be cut out and assembled into a simulation eye.

## Features

- Upload images (PNG, JPG, JPEG formats supported)
- Process the image
- Download the processed image
- Simple progress indicator for better user experience

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone the repository
```bash
git clone https://github.com/stuwilmur/sim-eye-app.git
cd sim-eye-app
```

2. Create a virtual environment (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

### Running the App

```bash
streamlit run main.py
```

The app will be available at http://localhost:8501 in your web browser.

## Usage Guidelines

- Maximum file size: 10MB
- Supported formats: PNG, JPG, JPEG

## License

MIT

## Related repo
[stuwilmur/sim-eye](https://github.com/stuwilmur/sim-eye)
