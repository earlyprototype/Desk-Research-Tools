#!/usr/bin/env python3
import argparse
from website_extractor import WebsiteExtractor
from typing import List
import sys

def read_url_list(file_path: str) -> List[str]:
    """Read URLs from a file, one per line."""
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def main():
    parser = argparse.ArgumentParser(description='Extract website content and assets.')
    
    # URL input options (mutually exclusive)
    url_group = parser.add_mutually_exclusive_group(required=True)
    url_group.add_argument('--url', help='Single URL to extract')
    url_group.add_argument('--url-file', help='File containing URLs to extract (one per line)')
    url_group.add_argument('--crawl', help='URL to start crawling from')
    url_group.add_argument('--subdomains', help='Domain to extract subdomains from')
    
    # Output options
    parser.add_argument('--output', '-o', help='Output directory name (optional)')
    parser.add_argument('--base-dir', '-b', default='extracted_sites',
                      help='Base directory for all extractions (default: extracted_sites)')
    
    # Crawling options
    parser.add_argument('--max-pages', type=int, help='Maximum number of pages to extract')
    parser.add_argument('--max-depth', type=int, help='Maximum depth for crawling')
    
    args = parser.parse_args()
    
    try:
        # Initialize extractor with crawling limits if specified
        extractor = WebsiteExtractor(
            base_output_dir=args.base_dir,
            max_pages=args.max_pages,
            max_depth=args.max_depth
        )
        
        # Handle different extraction modes
        if args.url:
            # Single URL extraction
            output_dir = extractor.extract_site(args.url, args.output)
            print(f"\nWebsite successfully extracted to: {output_dir}")
            
        elif args.url_file:
            # Batch extraction from file
            urls = read_url_list(args.url_file)
            output_dirs = extractor.extract_site_batch(urls, args.output)
            print("\nBatch extraction completed:")
            for i, dir in enumerate(output_dirs, 1):
                print(f"{i}. {dir}")
            
        elif args.crawl:
            # Domain crawling
            output_dirs = extractor.crawl_domain(args.crawl, args.output)
            print("\nDomain crawling completed:")
            for i, dir in enumerate(output_dirs, 1):
                print(f"{i}. {dir}")
            
        elif args.subdomains:
            # Subdomain extraction
            output_dirs = extractor.extract_subdomains(args.subdomains, args.output)
            print("\nSubdomain extraction completed:")
            for i, dir in enumerate(output_dirs, 1):
                print(f"{i}. {dir}")
        
    except Exception as e:
        print(f"\nError: {str(e)}", file=sys.stderr)
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 