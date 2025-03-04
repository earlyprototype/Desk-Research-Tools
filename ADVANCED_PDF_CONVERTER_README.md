# Advanced PDF Converter Tool

This tool provides enhanced capabilities for converting PDF files to various formats with improved quality. It was developed to make the vital information in the WEF's Global Skills Taxonomy and other project documents more accessible for analysis and reference.

## Features

- **Multiple Output Formats**:
  - HTML with enhanced formatting and styling
  - HTML with embedded images (preserves visual elements)
  - Plain text (fastest, simplest extraction)
  - Markdown with automatic header detection

- **Batch Processing**: Convert entire directories of PDF files at once with detailed progress tracking.

- **Image Extraction**: Extract and embed images from PDFs into HTML output (requires PyMuPDF).

- **Quality Improvements**:
  - Better text layout preservation
  - CSS styling for improved readability
  - Intelligent structure detection for Markdown
  - Table formatting in HTML output

- **User-Friendly Interface**: Simple batch file interface with format selection options.

## Requirements

- Python 3.6 or higher
- Required Python packages (automatically installed):
  - pdfminer.six: Core PDF text extraction
  - pymupdf (fitz): For image extraction (optional)
  - markdown: For markdown conversions (optional)
  - tqdm: For progress bars
  - argparse: For command-line argument parsing

## Installation

1. Make sure you have Python 3.6+ installed on your system.
2. Place the following files in your project directory:
   - `advanced_pdf_converter.py` (main script)
   - `advanced_pdf_requirements.txt` (dependencies)
   - `run_advanced_converter.bat` (Windows batch file)
3. Make sure you have a `Resources` directory containing your PDF files.

## Quick Start (For Windows Users)

1. Simply double-click the `run_advanced_converter.bat` file.
2. Choose your desired conversion format from the menu.
3. Wait for the conversion to complete.
4. Find your converted files in the corresponding output directory:
   - `HTML_Resources/` for HTML files
   - `Text_Resources/` for text files
   - `Markdown_Resources/` for markdown files
   - `extracted_images/` for extracted images (if enabled)

## Command Line Usage

For more control, you can run the Python script directly:

```bash
# Convert a single PDF file to HTML
python advanced_pdf_converter.py --input input.pdf --output output.html --format html

# Convert all PDFs in a directory to HTML with images
python advanced_pdf_converter.py --input_dir Resources --output_dir HTML_Resources --format html --images

# Convert all PDFs to plain text
python advanced_pdf_converter.py --input_dir Resources --output_dir Text_Resources --format text

# Convert all PDFs to Markdown
python advanced_pdf_converter.py --input_dir Resources --output_dir Markdown_Resources --format markdown
```

### Available Command Line Arguments

- `--input`: Single PDF file to convert
- `--input_dir`: Directory containing PDF files to convert
- `--output`: Output file path (for single file conversion)
- `--output_dir`: Output directory (for batch conversion)
- `--format`: Output format - one of: `html`, `text`, `markdown` (default: `html`)
- `--images`: Include images in HTML output (optional)
- `--image_dir`: Directory to store extracted images (default: `extracted_images`)

## Troubleshooting

### Common Issues

1. **Import Errors**: If you encounter import errors, ensure you've installed the required packages:
   ```
   pip install -r advanced_pdf_requirements.txt
   ```

2. **Image Extraction Not Working**: To use the image extraction feature, make sure PyMuPDF is installed:
   ```
   pip install pymupdf
   ```

3. **Conversion Quality Issues**: Some PDF files with complex layouts may not convert perfectly. Try different formats or adjust the parameters in the code for specific files.

4. **Permission Errors**: Ensure you have write permissions for the output directories.

### Performance Tips

- Text conversion is much faster than HTML with images
- For large batches, consider converting to text first for quick review
- Image extraction can significantly increase processing time and storage needs

## Limitations

- Complex document layouts (multiple columns, floating elements) may lose some formatting
- Not all PDFs contain extractable text (scanned documents without OCR)
- Image extraction works best with PDF files that have embedded images (not all PDFs contain extractable images)
- Very large PDF files may require additional memory

## Advanced Usage

For more sophisticated PDF processing needs, consider:

1. Using the PyMuPDF library directly for complex document analysis
2. Adding OCR capabilities with Tesseract for scanned documents
3. Customizing the CSS in the script for different styling

## License

This tool was created for project use within the FactoryXChange consortium's work on skills development in manufacturing. 