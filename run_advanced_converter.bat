@echo off
echo Advanced PDF Converter Tool
echo -------------------------------

REM Check if output directories exist, create if they don't
if not exist "HTML_Resources" mkdir HTML_Resources
if not exist "Text_Resources" mkdir Text_Resources 
if not exist "Markdown_Resources" mkdir Markdown_Resources
if not exist "extracted_images" mkdir extracted_images

REM Install requirements
echo Installing required packages...
pip install -r advanced_pdf_requirements.txt

echo.
echo Choose conversion format:
echo 1. PDF to HTML with images (best quality)
echo 2. PDF to HTML (without images)
echo 3. PDF to plain text (fastest)
echo 4. PDF to Markdown
echo 5. All formats
echo.

set /p format_choice="Enter your choice (1-5): "

if "%format_choice%"=="1" (
    echo Converting PDFs to HTML with images...
    python advanced_pdf_converter.py --input_dir Resources --output_dir HTML_Resources --format html --images
) else if "%format_choice%"=="2" (
    echo Converting PDFs to HTML...
    python advanced_pdf_converter.py --input_dir Resources --output_dir HTML_Resources --format html
) else if "%format_choice%"=="3" (
    echo Converting PDFs to text...
    python advanced_pdf_converter.py --input_dir Resources --output_dir Text_Resources --format text
) else if "%format_choice%"=="4" (
    echo Converting PDFs to Markdown...
    python advanced_pdf_converter.py --input_dir Resources --output_dir Markdown_Resources --format markdown
) else if "%format_choice%"=="5" (
    echo Converting PDFs to all formats...
    echo.
    echo HTML with images:
    python advanced_pdf_converter.py --input_dir Resources --output_dir HTML_Resources --format html --images
    echo.
    echo Text:
    python advanced_pdf_converter.py --input_dir Resources --output_dir Text_Resources --format text
    echo.
    echo Markdown:
    python advanced_pdf_converter.py --input_dir Resources --output_dir Markdown_Resources --format markdown
) else (
    echo Invalid choice. Exiting...
    goto end
)

:end
echo.
echo Conversion process completed.
pause 