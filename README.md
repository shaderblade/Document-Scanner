# Document Scanner Web App

A web-based document scanner application built using Flask and OpenCV.

## Installation

1. Clone the repository and open that directory:
   ```bash
      git clone https://github.com/shaderblade/Document-Scanner
      cd Document-Scanner
   ```

2. Create a virtual environment (Recommended)
   ```bash
      python -m venv venv
      source venv/bin/activate  # On Windows, use "venv\Scripts\activate"
   ```

3. Install the required packages
   ```bash
      pip install -r requirements.txt
   ```

4. Run the application
   ```bash
      python app.py
   ```


## Usage
- Open your web browser and navigate to http://localhost:5000.
- Upload an image containing a document.
- Click the "Scan" button to process the image.
- Download the scanned document.