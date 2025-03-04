# Research Tools Collection

A collection of specialized tools for research content extraction, conversion, and management. This toolkit includes two main components: a Website Content Extractor and an Advanced PDF Converter.

## 🛠️ Tools Overview

### 1. Website Content Extractor
An interactive tool for downloading and organizing web content locally.

**Key Features:**
- 🌐 Multiple extraction modes (single page, batch, domain crawling)
- 🔍 Subdomain discovery and extraction
- 💾 Complete asset preservation (CSS, JS, images)
- 📂 Organized content storage
- 🎯 Automatic browser preview

[➡️ Website Extractor Documentation](website_extractor/README.md)

### 2. Advanced PDF Converter
A powerful tool for converting PDFs to multiple formats with enhanced formatting.

**Key Features:**
- 📄 Multiple output formats (HTML, Text, Markdown)
- 🎨 Preserved formatting and styling
- 📊 Table structure preservation
- 🖼️ Image extraction and embedding
- 📑 Batch processing capabilities

[➡️ PDF Converter Documentation](PDF_Converter/ADVANCED_PDF_CONVERTER_README.md)

## 🚀 Quick Start

### Website Content Extraction
```bash
cd website_extractor
python interactive_extract.py
```

### PDF Conversion
```bash
cd PDF_Converter
python advanced_pdf_converter.py
# or on Windows:
run_advanced_converter.bat
```

## 📁 Directory Structure
```
Tools/
├── website_extractor/          # Website extraction tool
│   ├── website_extractor.py    # Core extraction logic
│   ├── interactive_extract.py  # Interactive interface
│   └── requirements.txt        # Dependencies
│
├── PDF_Converter/             # PDF conversion tool
│   ├── advanced_pdf_converter.py   # Main converter
│   ├── run_advanced_converter.bat  # Windows launcher
│   ├── templates/                  # HTML templates
│   └── advanced_pdf_requirements.txt
│
└── portable_tools_setup.md    # Setup guide for new projects
```

## 💻 System Requirements

### Common Requirements
- Python 3.6 or higher
- pip (Python package manager)
- Internet connection (for website extraction)
- Sufficient disk space for content storage

### Website Extractor Dependencies
- requests>=2.31.0
- beautifulsoup4>=4.12.0
- pathlib>=1.0.1

### PDF Converter Dependencies
- pdfminer.six>=20221105
- pymupdf>=1.23.7
- markdown>=3.5.1
- tqdm>=4.66.1

## 🎯 Use Cases

### Website Extractor
1. **Research Collection**
   - Download reference materials for offline access
   - Archive important web content
   - Create local copies of documentation

2. **Content Management**
   - Organize web resources into structured folders
   - Create offline backups of online content
   - Prepare content for sharing or archiving

### PDF Converter
1. **Document Processing**
   - Convert research papers to searchable formats
   - Create web-friendly versions of PDF documents
   - Extract text for analysis or reference

2. **Content Transformation**
   - Convert PDFs to editable formats
   - Create accessible versions of documents
   - Generate multiple format outputs for different uses

## 🔧 Common Operations

### Website Content Extraction
1. **Single Page Extraction**
   ```
   1. Run interactive_extract.py
   2. Choose option 1
   3. Enter URL
   4. Content opens automatically in browser
   ```

2. **Batch Processing**
   ```
   1. Run interactive_extract.py
   2. Choose option 2
   3. Paste multiple URLs
   4. Type 'done' when finished
   ```

### PDF Conversion
1. **Single PDF Conversion**
   ```
   1. Place PDF in input directory
   2. Run advanced_pdf_converter.py
   3. Select output format
   4. Access converted files in respective folders
   ```

2. **Batch Processing**
   ```
   1. Place PDFs in input directory
   2. Run in batch mode
   3. Monitor progress in console
   4. Access all converted files
   ```

## 📚 Documentation

- [Website Extractor Guide](website_extractor/README.md)
- [PDF Converter Guide](PDF_Converter/ADVANCED_PDF_CONVERTER_README.md)
- [Portable Setup Guide](portable_tools_setup.md)

## ⚠️ Important Notes

1. **Website Extraction**
   - Respect robots.txt guidelines
   - Be mindful of website terms of service
   - Consider bandwidth and storage limitations

2. **PDF Conversion**
   - Some complex PDF layouts may require manual adjustment
   - Very large PDFs may require additional processing time
   - Check output for accuracy with critical documents

## 🆘 Troubleshooting

### Website Extractor
- Check internet connection
- Verify URL accessibility
- Ensure sufficient disk space
- Check console for error messages

### PDF Converter
- Verify PDF file integrity
- Check file permissions
- Ensure sufficient memory
- Monitor conversion logs

## 🔄 Updates and Maintenance

1. **Regular Updates**
   - Check for dependency updates
   - Test with new Python versions
   - Backup configurations before updates

2. **Customization**
   - Templates can be modified
   - Output formats can be adjusted
   - Configuration files can be customized

## 📞 Support

For issues or suggestions:
1. Check the respective tool's documentation
2. Review error messages in the console
3. Verify system requirements
4. Check file permissions and paths

## 📄 License

These tools are provided for research and documentation purposes. Please respect copyright and terms of service when using these tools. 