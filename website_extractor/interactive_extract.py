#!/usr/bin/env python3
from website_extractor import WebsiteExtractor
import sys
from typing import List
import textwrap
import webbrowser
import os
from pathlib import Path

def print_header():
    """Print the tool header."""
    print("\n" + "="*60)
    print("Website Content Extractor - Interactive Mode")
    print("="*60 + "\n")

def get_menu_choice() -> int:
    """Display menu and get user choice."""
    while True:
        print("\nChoose an operation:")
        print("1. Extract single website")
        print("2. Extract multiple websites (batch mode)")
        print("3. Crawl domain")
        print("4. Extract subdomains")
        print("5. Exit")
        
        try:
            choice = int(input("\nEnter your choice (1-5): ").strip())
            if 1 <= choice <= 5:
                return choice
            print("\nError: Please enter a number between 1 and 5")
        except ValueError:
            print("\nError: Please enter a valid number")

def get_urls_input() -> List[str]:
    """
    Get URLs from user input, supporting both typing and pasting.
    Returns a list of cleaned URLs.
    """
    print("\nEnter URLs (one per line)")
    print("You can:")
    print("1. Type URLs and press Enter after each one")
    print("2. Paste multiple URLs at once")
    print("3. Type 'done' on a new line when finished\n")
    
    urls = []
    while True:
        try:
            line = input().strip()
            if line.lower() == 'done':
                break
            
            # Split input in case multiple URLs were pasted
            for url in line.split():
                if url:  # Skip empty strings
                    # Add http:// if no protocol specified
                    if not url.startswith(('http://', 'https://')):
                        url = 'https://' + url
                    urls.append(url)
                    
        except EOFError:  # Handle Ctrl+D
            break
        except KeyboardInterrupt:  # Handle Ctrl+C
            print("\nInput cancelled.")
            return []
    
    return urls

def get_crawl_limits():
    """Get max pages and depth for crawling."""
    try:
        max_pages = input("\nEnter maximum number of pages (press Enter for no limit): ").strip()
        max_pages = int(max_pages) if max_pages else None
        
        max_depth = input("Enter maximum crawl depth (press Enter for no limit): ").strip()
        max_depth = int(max_depth) if max_depth else None
        
        return max_pages, max_depth
    except ValueError:
        print("\nInvalid input. Using no limits.")
        return None, None

def open_in_browser(output_dir: str):
    """Open the extracted content in the default web browser."""
    if output_dir:
        index_path = Path(output_dir) / "index.html"
        if index_path.exists():
            file_url = f"file:///{index_path.absolute().as_posix()}"
            print(f"\nOpening {file_url} in your browser...")
            webbrowser.open(file_url)
        else:
            print(f"\nNo index.html found in {output_dir}")

def main():
    print_header()
    
    while True:
        choice = get_menu_choice()
        
        if choice == 5:  # Exit
            print("\nGoodbye!")
            break
            
        # Initialize extractor
        extractor = WebsiteExtractor()
        
        try:
            if choice == 1:  # Single website
                print("\nEnter the website URL:")
                urls = get_urls_input()
                if urls:
                    output_dir = extractor.extract_site(urls[0])
                    print(f"\nWebsite extracted to: {output_dir}")
                    open_in_browser(output_dir)
                
            elif choice == 2:  # Batch mode
                urls = get_urls_input()
                if urls:
                    print(f"\nProcessing {len(urls)} URLs...")
                    output_dirs = extractor.extract_site_batch(urls)
                    print("\nExtraction completed. Output directories:")
                    for i, dir in enumerate(output_dirs, 1):
                        print(f"{i}. {dir}")
                    
                    # Ask which site to open
                    if output_dirs:
                        try:
                            choice = input("\nEnter number to open in browser (or press Enter to skip): ").strip()
                            if choice and choice.isdigit() and 1 <= int(choice) <= len(output_dirs):
                                open_in_browser(output_dirs[int(choice)-1])
                        except (ValueError, IndexError):
                            pass
                
            elif choice == 3:  # Crawl domain
                urls = get_urls_input()
                if urls:
                    max_pages, max_depth = get_crawl_limits()
                    extractor.max_pages = max_pages
                    extractor.max_depth = max_depth
                    
                    print(f"\nCrawling domain: {urls[0]}")
                    output_dirs = extractor.crawl_domain(urls[0])
                    print("\nCrawling completed. Output directories:")
                    for i, dir in enumerate(output_dirs, 1):
                        print(f"{i}. {dir}")
                    
                    # Ask which site to open
                    if output_dirs:
                        try:
                            choice = input("\nEnter number to open in browser (or press Enter to skip): ").strip()
                            if choice and choice.isdigit() and 1 <= int(choice) <= len(output_dirs):
                                open_in_browser(output_dirs[int(choice)-1])
                        except (ValueError, IndexError):
                            pass
                
            elif choice == 4:  # Extract subdomains
                urls = get_urls_input()
                if urls:
                    print(f"\nExtracting subdomains for: {urls[0]}")
                    output_dirs = extractor.extract_subdomains(urls[0])
                    print("\nExtraction completed. Output directories:")
                    for i, dir in enumerate(output_dirs, 1):
                        print(f"{i}. {dir}")
                    
                    # Ask which site to open
                    if output_dirs:
                        try:
                            choice = input("\nEnter number to open in browser (or press Enter to skip): ").strip()
                            if choice and choice.isdigit() and 1 <= int(choice) <= len(output_dirs):
                                open_in_browser(output_dirs[int(choice)-1])
                        except (ValueError, IndexError):
                            pass
            
            if choice != 5:
                input("\nPress Enter to continue...")
                
        except Exception as e:
            print(f"\nError: {str(e)}")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram terminated by user.")
        sys.exit(0) 