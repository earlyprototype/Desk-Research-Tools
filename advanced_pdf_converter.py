#!/usr/bin/env python3
"""
Advanced PDF Converter

This script provides enhanced PDF conversion capabilities, including:
- PDF to HTML with better formatting preservation
- PDF to Text for simple text extraction
- PDF to Markdown for structured content
- Optional image extraction

Requirements:
    - pdfminer.six
    - pymupdf (fitz)
    - markdown
    - argparse
    - tqdm

Usage:
    python advanced_pdf_converter.py --input file.pdf --output file.html --format html --images
"""

import os
import sys
import argparse
import glob
import re
from io import StringIO
from tqdm import tqdm

# Import pdfminer.six components
from pdfminer.high_level import extract_text_to_fp, extract_text
from pdfminer.layout import LAParams

# Try to import optional libraries
try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False

try:
    import markdown
    MARKDOWN_AVAILABLE = True
except ImportError:
    MARKDOWN_AVAILABLE = False

class PDFConverter:
    """Advanced PDF conversion with multiple output formats and options."""
    
    def __init__(self, include_images=False, image_dir=None):
        """
        Initialize the converter with options.
        
        Args:
            include_images (bool): Whether to extract images from PDFs
            image_dir (str): Directory to save extracted images
        """
        self.include_images = include_images
        self.image_dir = image_dir
        
        # Create image directory if needed
        if self.include_images and self.image_dir and not os.path.exists(self.image_dir):
            os.makedirs(self.image_dir)
    
    def convert_to_html(self, pdf_path, html_path):
        """
        Convert PDF to HTML with enhanced formatting.
        
        Args:
            pdf_path (str): Path to input PDF
            html_path (str): Path for output HTML
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # First extract text as plain text
            text = extract_text(pdf_path)
            
            # Create basic HTML structure
            html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>{os.path.basename(pdf_path)}</title>
<style>
    body {{ font-family: Arial, sans-serif; line-height: 1.5; max-width: 900px; margin: 0 auto; padding: 20px; }}
    h1, h2, h3, h4, h5, h6 {{ color: #333; margin-top: 24px; }}
    table {{ border-collapse: collapse; width: 100%; margin: 16px 0; }}
    table, th, td {{ border: 1px solid #ddd; }}
    th, td {{ padding: 8px; text-align: left; }}
    th {{ background-color: #f2f2f2; }}
    .page {{ border-bottom: 1px dashed #ccc; margin-bottom: 20px; padding-bottom: 20px; }}
    img {{ max-width: 100%; height: auto; border: 1px solid #ddd; padding: 5px; }}
    pre {{ white-space: pre-wrap; }}
    .pdf-images {{ margin-top: 30px; border-top: 2px solid #ccc; padding-top: 20px; }}
    .image-container {{ margin-bottom: 20px; text-align: center; }}
    .image-container p {{ font-style: italic; margin-top: 8px; color: #666; }}
</style>
</head>
<body>
<h1>{os.path.basename(pdf_path)}</h1>
<div class="content">
<pre>
{text}
</pre>
</div>
"""
            
            # Add images if enabled and PyMuPDF is available
            if self.include_images and PYMUPDF_AVAILABLE:
                html_content = self._add_images_to_html(pdf_path, html_content, html_path)
            
            # Close the HTML
            html_content += """
</body>
</html>
"""
            
            # Write the final HTML
            with open(html_path, 'w', encoding='utf-8') as html_file:
                html_file.write(html_content)
                
            return True
            
        except Exception as e:
            print(f"Error converting {pdf_path} to HTML: {str(e)}")
            return False
    
    def convert_to_text(self, pdf_path, text_path):
        """
        Convert PDF to plain text.
        
        Args:
            pdf_path (str): Path to input PDF
            text_path (str): Path for output text file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            text = extract_text(pdf_path)
            
            with open(text_path, 'w', encoding='utf-8') as text_file:
                text_file.write(text)
                
            return True
            
        except Exception as e:
            print(f"Error converting {pdf_path} to text: {str(e)}")
            return False
    
    def convert_to_markdown(self, pdf_path, md_path):
        """
        Convert PDF to Markdown format.
        
        Args:
            pdf_path (str): Path to input PDF
            md_path (str): Path for output Markdown file
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not MARKDOWN_AVAILABLE:
            print("Markdown conversion requires the 'markdown' package. Install with: pip install markdown")
            return False
            
        try:
            # First extract as plain text
            text = extract_text(pdf_path)
            
            # Simple heuristics to improve markdown structure
            # 1. Try to identify headers by length and newlines
            lines = text.split('\n')
            md_lines = []
            
            for i, line in enumerate(lines):
                line = line.strip()
                if not line:
                    md_lines.append('')
                    continue
                    
                # Potential header detection (short line followed by blank line)
                if len(line) < 80 and i < len(lines) - 1 and not lines[i+1].strip():
                    if len(line) < 30:  # Likely a main header
                        md_lines.append(f'## {line}')
                    else:  # Likely a subheader
                        md_lines.append(f'### {line}')
                else:
                    # Regular text
                    md_lines.append(line)
            
            # Join lines back together
            markdown_text = '\n'.join(md_lines)
            
            # Write the markdown file
            with open(md_path, 'w', encoding='utf-8') as md_file:
                md_file.write(markdown_text)
                
            return True
            
        except Exception as e:
            print(f"Error converting {pdf_path} to markdown: {str(e)}")
            return False
    
    def _add_images_to_html(self, pdf_path, html_content, html_path):
        """
        Extract images from PDF and add them to HTML.
        
        Args:
            pdf_path (str): Path to input PDF
            html_content (str): HTML content to augment
            html_path (str): Path to output HTML (used for relative paths)
            
        Returns:
            str: Updated HTML content with image tags
        """
        try:
            # Create a specific image directory for this HTML file
            base_name = os.path.splitext(os.path.basename(html_path))[0]
            
            # Use the main extracted_images folder at the root level
            main_image_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "extracted_images"))
            file_image_dir = os.path.join(main_image_dir, base_name)
            
            if not os.path.exists(file_image_dir):
                os.makedirs(file_image_dir)
            
            # Open the PDF document
            doc = fitz.open(pdf_path)
            image_count = 0
            all_images_html = "\n<div class='pdf-images'>\n<h2>Images from Document</h2>\n"
            
            # Iterate through pages to extract images
            for page_num, page in enumerate(doc):
                images = page.get_images(full=True)
                
                if images:  # Only create a page section if images exist
                    all_images_html += f"<h3>Images from page {page_num+1}</h3>\n"
                
                for img_index, img in enumerate(images):
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    
                    # Save the image
                    image_filename = f"image_{page_num+1}_{img_index+1}.png"
                    image_path = os.path.join(file_image_dir, image_filename)
                    
                    with open(image_path, "wb") as img_file:
                        img_file.write(image_bytes)
                    
                    # Calculate relative path from HTML to image - adjusted for root level extracted_images
                    rel_image_path = os.path.join("extracted_images", base_name, image_filename).replace('\\', '/')
                    
                    # Create image tag and add to our collection
                    all_images_html += f'<div class="image-container">\n'
                    all_images_html += f'  <img src="../{rel_image_path}" alt="Image {page_num+1}-{img_index+1}" />\n'
                    all_images_html += f'  <p>Figure {page_num+1}.{img_index+1}</p>\n'
                    all_images_html += f'</div>\n'
                    
                    image_count += 1
            
            all_images_html += "</div>\n"
            
            # Insert all images after the content
            if image_count > 0:
                print(f"Added {image_count} images to {html_path}")
                
                # We need to insert images before </body> tag
                end_pre_pos = html_content.find("</pre>")
                if end_pre_pos != -1:
                    # Insert after the </pre> tag but before the closing </div>
                    html_content = html_content[:end_pre_pos + 6] + all_images_html + html_content[end_pre_pos + 6:]
                else:
                    # If no </pre> tag found, insert before </body>
                    body_end = html_content.find("</body>")
                    if body_end != -1:
                        html_content = html_content[:body_end] + all_images_html + html_content[body_end:]
            
            return html_content
            
        except Exception as e:
            print(f"Warning: Failed to extract images from {pdf_path}: {str(e)}")
            return html_content

def batch_convert(converter, input_dir, output_dir, format_type, file_pattern="*.pdf"):
    """
    Convert all PDF files in a directory to the specified format.
    
    Args:
        converter (PDFConverter): Converter instance
        input_dir (str): Directory containing PDF files
        output_dir (str): Directory for output files
        format_type (str): Output format (html, text, markdown)
        file_pattern (str): File pattern to match PDF files
        
    Returns:
        dict: Statistics about the conversion process
    """
    # Create output directory if needed
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Debug output
    print(f"Starting batch conversion from {input_dir} to {output_dir} in {format_type} format")
    search_pattern = os.path.join(input_dir, file_pattern)
    print(f"Using search pattern: {search_pattern}")
    
    # Get all PDF files in the input directory
    pdf_files = glob.glob(os.path.join(input_dir, file_pattern))
    
    # Show found files
    print(f"Found {len(pdf_files)} PDF files:")
    for pdf in pdf_files[:5]:  # Show first 5 files
        print(f"  - {pdf}")
    if len(pdf_files) > 5:
        print(f"  - ... and {len(pdf_files) - 5} more files")
    
    # Statistics
    stats = {
        "total": len(pdf_files),
        "successful": 0,
        "failed": 0,
        "skipped": 0,
        "failures": []  # Track failed files and reasons
    }
    
    # Process each PDF file with progress bar
    for pdf_path in tqdm(pdf_files, desc=f"Converting PDFs to {format_type}", ncols=100):
        # Get the base filename without extension
        base_name = os.path.basename(pdf_path)
        file_name = os.path.splitext(base_name)[0]
        
        # Create the output path with appropriate extension
        if format_type == 'html':
            output_path = os.path.join(output_dir, f"{file_name}.html")
        elif format_type == 'text':
            output_path = os.path.join(output_dir, f"{file_name}.txt")
        elif format_type == 'markdown':
            output_path = os.path.join(output_dir, f"{file_name}.md")
        else:
            print(f"Unsupported format type: {format_type}")
            stats["failed"] += 1
            stats["failures"].append((pdf_path, f"Unsupported format: {format_type}"))
            continue
        
        # Check if file already exists
        if os.path.exists(output_path):
            # Check modification times
            pdf_mod_time = os.path.getmtime(pdf_path)
            out_mod_time = os.path.getmtime(output_path)
            
            # Skip if output is newer than PDF (already converted)
            if out_mod_time > pdf_mod_time:
                stats["skipped"] += 1
                continue
        
        # Perform conversion based on format type
        try:
            if format_type == 'html':
                success = converter.convert_to_html(pdf_path, output_path)
            elif format_type == 'text':
                success = converter.convert_to_text(pdf_path, output_path)
            elif format_type == 'markdown':
                success = converter.convert_to_markdown(pdf_path, output_path)
            
            # Update statistics
            if success:
                stats["successful"] += 1
            else:
                stats["failed"] += 1
                stats["failures"].append((pdf_path, "Conversion failed"))
        except Exception as e:
            error_message = str(e)
            print(f"Error converting {pdf_path}: {error_message}")
            stats["failed"] += 1
            stats["failures"].append((pdf_path, error_message[:100] + "..." if len(error_message) > 100 else error_message))
    
    # Generate a detailed report
    print("\nConversion complete!")
    print(f"Total files: {stats['total']}")
    print(f"Successfully converted: {stats['successful']}")
    print(f"Failed: {stats['failed']}")
    print(f"Skipped (already up-to-date): {stats['skipped']}")
    
    # Show failures if any
    if stats["failures"]:
        print("\nFailed files:")
        for file_path, reason in stats["failures"][:10]:  # Show first 10 failures
            print(f"  - {os.path.basename(file_path)}: {reason}")
        if len(stats["failures"]) > 10:
            print(f"  - ... and {len(stats['failures']) - 10} more failures")
        
        # Ask if user wants to retry failed conversions with alternative converter
        if stats["failed"] > 0 and format_type == 'html' and converter.include_images:
            print("\nSome files failed with the advanced converter.")
            print("Would you like to try converting failed files with the alternative text-only converter? (y/n)")
            retry_choice = input().strip().lower()
            if retry_choice == 'y':
                # Create alternative converter instance
                alt_converter = PDFConverter(include_images=False)
                
                # Process only failed files
                failed_files = [file_path for file_path, _ in stats["failures"]]
                retry_successful = 0
                
                print(f"\nRetrying {len(failed_files)} failed files with alternative converter...")
                for pdf_path in tqdm(failed_files, desc="Retrying with alt converter"):
                    base_name = os.path.basename(pdf_path)
                    file_name = os.path.splitext(base_name)[0]
                    output_path = os.path.join(output_dir, f"{file_name}.html")
                    
                    try:
                        if alt_converter.convert_to_html(pdf_path, output_path):
                            retry_successful += 1
                    except Exception as e:
                        pass  # Already failed, just continue with others
                
                print(f"\nSuccessfully recovered {retry_successful} of {len(failed_files)} failed files.")
    
    return stats

def main():
    # Set up command line argument parser
    parser = argparse.ArgumentParser(description="Advanced PDF Converter")
    
    # Create a mutually exclusive group for input options
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--input", help="Input PDF file path")
    input_group.add_argument("--input_dir", help="Input directory containing PDF files")
    
    # Create a mutually exclusive group for output options
    output_group = parser.add_mutually_exclusive_group(required=True)
    output_group.add_argument("--output", help="Output file path")
    output_group.add_argument("--output_dir", help="Output directory for converted files")
    
    # Additional options
    parser.add_argument("--format", choices=['html', 'text', 'markdown'], default='html',
                        help="Output format (default: html)")
    parser.add_argument("--images", action='store_true', 
                        help="Extract and include images in the output (for HTML format)")
    parser.add_argument("--image_dir", default="extracted_images",
                        help="Directory to store extracted images (default: 'extracted_images')")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Check if we have necessary libraries for image extraction
    if args.images and not PYMUPDF_AVAILABLE:
        print("Warning: Image extraction requires PyMuPDF. Install with: pip install pymupdf")
        print("Continuing without image extraction...")
        args.images = False
    
    # Initialize converter
    converter = PDFConverter(include_images=args.images, image_dir=args.image_dir)
    
    # Check if we're in batch mode or single file mode
    if args.input_dir and args.output_dir:
        # Batch mode
        print(f"Starting batch conversion from {args.input_dir} to {args.output_dir} in {args.format} format")
        stats = batch_convert(converter, args.input_dir, args.output_dir, args.format)
        
        # Print statistics
        print(f"\nConversion complete!")
        print(f"Total files: {stats['total']}")
        print(f"Successfully converted: {stats['successful']}")
        print(f"Failed: {stats['failed']}")
        
    elif args.input and args.output:
        # Single file mode
        print(f"Converting {args.input} to {args.output} in {args.format} format")
        
        if args.format == 'html':
            success = converter.convert_to_html(args.input, args.output)
        elif args.format == 'text':
            success = converter.convert_to_text(args.input, args.output)
        elif args.format == 'markdown':
            success = converter.convert_to_markdown(args.input, args.output)
        else:
            print(f"Unsupported format: {args.format}")
            return 1
        
        if success:
            print("Conversion successful!")
        else:
            print("Conversion failed.")
            return 1
    else:
        # Invalid combination of arguments
        parser.error("You must provide either --input and --output for single file conversion "
                     "or --input_dir and --output_dir for batch conversion.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 