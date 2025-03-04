import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import shutil
from pathlib import Path
import logging
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import re
from typing import Set, List, Optional

class WebsiteExtractor:
    """A tool for extracting website content and assets."""
    
    def __init__(self, base_output_dir="extracted_sites", max_pages=None, max_depth=None):
        """
        Initialize the extractor with base output directory.
        
        Args:
            base_output_dir (str): Base directory for all extractions
            max_pages (int, optional): Maximum number of pages to extract
            max_depth (int, optional): Maximum depth for crawling (None for unlimited)
        """
        self.base_output_dir = base_output_dir
        self.max_pages = max_pages
        self.max_depth = max_depth
        self.session = requests.Session()
        self.visited_urls: Set[str] = set()
        self.queue: Queue = Queue()
        self.setup_logging()
    
    def setup_logging(self):
        """Configure logging for the extractor."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def extract_site(self, url, project_name=None):
        """
        Extract content from a website URL.
        
        Args:
            url (str): The URL to extract content from
            project_name (str, optional): Name for the project folder. If None, derived from URL
        """
        if not project_name:
            project_name = urlparse(url).netloc.replace(".", "_")
        
        # Create project directory
        project_dir = Path(self.base_output_dir) / project_name
        project_dir.mkdir(parents=True, exist_ok=True)
        
        self.logger.info(f"Starting extraction of {url} to {project_dir}")
        
        try:
            # Get the main page
            response = self.session.get(url)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract and download assets
            self._extract_assets(soup, url, project_dir)
            
            # Update links in HTML to point to local assets
            self._update_links(soup, url)
            
            # Save the modified HTML
            index_path = project_dir / "index.html"
            with open(index_path, "w", encoding="utf-8") as f:
                f.write(str(soup.prettify()))
            
            self.logger.info(f"Successfully extracted site to {project_dir}")
            return str(project_dir)
            
        except Exception as e:
            self.logger.error(f"Error extracting site: {str(e)}")
            raise
    
    def _extract_assets(self, soup, base_url, project_dir):
        """Extract and save all assets from the page."""
        # Create asset directories
        assets_dir = project_dir / "assets"
        css_dir = assets_dir / "css"
        js_dir = assets_dir / "js"
        img_dir = assets_dir / "images"
        
        for directory in [css_dir, js_dir, img_dir]:
            directory.mkdir(parents=True, exist_ok=True)
        
        # Extract and save CSS files
        for css in soup.find_all("link", rel="stylesheet"):
            if css.get("href"):
                self._download_asset(css["href"], base_url, css_dir, "css")
                css["href"] = self._get_relative_path(css_dir, project_dir, css["href"])
        
        # Extract and save JavaScript files
        for script in soup.find_all("script", src=True):
            if script.get("src"):
                self._download_asset(script["src"], base_url, js_dir, "js")
                script["src"] = self._get_relative_path(js_dir, project_dir, script["src"])
        
        # Extract and save images
        for img in soup.find_all("img"):
            if img.get("src"):
                self._download_asset(img["src"], base_url, img_dir, "images")
                img["src"] = self._get_relative_path(img_dir, project_dir, img["src"])
    
    def _download_asset(self, url, base_url, save_dir, asset_type):
        """Download an asset file."""
        try:
            absolute_url = urljoin(base_url, url)
            filename = os.path.basename(urlparse(url).path)
            if not filename:
                filename = "index" + self._get_extension(asset_type)
            
            save_path = save_dir / filename
            
            # Skip if already downloaded
            if save_path.exists():
                return filename
            
            response = self.session.get(absolute_url)
            response.raise_for_status()
            
            with open(save_path, "wb") as f:
                f.write(response.content)
            
            self.logger.info(f"Downloaded {asset_type} asset: {filename}")
            return filename
            
        except Exception as e:
            self.logger.warning(f"Failed to download asset {url}: {str(e)}")
            return None
    
    def _get_extension(self, asset_type):
        """Get default extension for asset type."""
        extensions = {
            "css": ".css",
            "js": ".js",
            "images": ".png"
        }
        return extensions.get(asset_type, "")
    
    def _get_relative_path(self, asset_dir, project_dir, original_path):
        """Convert asset path to relative path from project root."""
        try:
            filename = os.path.basename(urlparse(original_path).path)
            if not filename:
                filename = "index" + self._get_extension(asset_dir.name)
            
            relative_path = os.path.relpath(asset_dir / filename, project_dir)
            return relative_path.replace("\\", "/")
            
        except Exception:
            return original_path
    
    def _update_links(self, soup, base_url):
        """Update all links in the HTML to work with local files."""
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if not href.startswith(("http://", "https://", "mailto:", "#")):
                a["href"] = urljoin(base_url, href)

    def extract_site_batch(self, urls: List[str], project_name: Optional[str] = None) -> List[str]:
        """
        Extract content from multiple URLs in batch.
        
        Args:
            urls (List[str]): List of URLs to extract
            project_name (str, optional): Base name for the project folder
            
        Returns:
            List[str]: List of output directories
        """
        output_dirs = []
        
        for i, url in enumerate(urls):
            try:
                # Create unique project name for each URL if not specified
                current_project = f"{project_name}_{i+1}" if project_name else None
                output_dir = self.extract_site(url, current_project)
                output_dirs.append(output_dir)
                self.logger.info(f"Completed {i+1}/{len(urls)}: {url}")
            except Exception as e:
                self.logger.error(f"Failed to extract {url}: {str(e)}")
        
        return output_dirs

    def crawl_domain(self, start_url: str, project_name: Optional[str] = None) -> List[str]:
        """
        Crawl a domain starting from a URL, extracting all linked pages within the same domain.
        
        Args:
            start_url (str): Starting URL for crawling
            project_name (str, optional): Base name for the project folder
            
        Returns:
            List[str]: List of output directories
        """
        base_domain = urlparse(start_url).netloc
        self.visited_urls.clear()
        self.queue = Queue()
        self.queue.put((start_url, 0))  # (url, depth)
        output_dirs = []
        pages_extracted = 0

        while not self.queue.empty():
            current_url, depth = self.queue.get()
            
            # Check if we've hit the limits
            if self.max_pages and pages_extracted >= self.max_pages:
                break
            if self.max_depth and depth > self.max_depth:
                continue
            
            # Skip if already visited
            if current_url in self.visited_urls:
                continue
            
            try:
                # Extract the current page
                current_project = f"{project_name}_{pages_extracted+1}" if project_name else None
                output_dir = self.extract_site(current_url, current_project)
                output_dirs.append(output_dir)
                self.visited_urls.add(current_url)
                pages_extracted += 1
                
                # Find and queue new links
                self._queue_new_links(current_url, base_domain, depth + 1)
                
            except Exception as e:
                self.logger.error(f"Failed to extract {current_url}: {str(e)}")
        
        return output_dirs

    def _queue_new_links(self, url: str, base_domain: str, depth: int):
        """Queue new links found on the page for crawling."""
        try:
            response = self.session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for a in soup.find_all('a', href=True):
                href = a['href']
                absolute_url = urljoin(url, href)
                parsed = urlparse(absolute_url)
                
                # Only queue links from the same domain that we haven't visited
                if (parsed.netloc == base_domain and 
                    absolute_url not in self.visited_urls and
                    not href.startswith(('#', 'mailto:', 'tel:'))):
                    self.queue.put((absolute_url, depth))
                    
        except Exception as e:
            self.logger.warning(f"Failed to queue links from {url}: {str(e)}")

    def extract_subdomains(self, domain: str, project_name: Optional[str] = None) -> List[str]:
        """
        Extract content from all subdomains of a given domain.
        
        Args:
            domain (str): Base domain to extract subdomains from
            project_name (str, optional): Base name for the project folder
            
        Returns:
            List[str]: List of output directories
        """
        # Remove protocol if present
        clean_domain = re.sub(r'^https?://', '', domain)
        
        # Try common subdomains
        common_subdomains = ['www', 'blog', 'docs', 'api', 'support', 'help']
        urls_to_try = [f"https://{sub}.{clean_domain}" for sub in common_subdomains]
        urls_to_try.append(f"https://{clean_domain}")
        
        # Filter out unreachable subdomains
        valid_urls = []
        for url in urls_to_try:
            try:
                response = self.session.head(url, timeout=5)
                if response.status_code == 200:
                    valid_urls.append(url)
                    self.logger.info(f"Found valid subdomain: {url}")
            except Exception:
                continue
        
        # Extract content from valid URLs
        return self.extract_site_batch(valid_urls, project_name)

if __name__ == "__main__":
    # Example usage
    extractor = WebsiteExtractor(max_pages=10, max_depth=2)
    
    # Single page extraction
    extractor.extract_site("https://example.com", "example_site")
    
    # Batch extraction
    urls = ["https://example.com", "https://example.org"]
    extractor.extract_site_batch(urls, "batch_example")
    
    # Domain crawling
    extractor.crawl_domain("https://example.com", "crawl_example")
    
    # Subdomain extraction
    extractor.extract_subdomains("example.com", "subdomain_example") 