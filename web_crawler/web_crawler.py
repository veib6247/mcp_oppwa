import json
import logging
import time
from typing import Any, Dict, List
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, Tag


class WebCrawler:
    def __init__(self, timeout: int = 10, delay: float = 1.0):
        """
        Initialize the web crawler.

        Args:
            timeout: Request timeout in seconds
            delay: Delay between requests to be respectful
        """
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.timeout = timeout
        self.delay = delay
        self.logger = logging.getLogger(__name__)

    def crawl_page(self, url: str) -> Dict[str, Any]:
        """
        Crawl a single web page and extract structured data.

        Args:
            url: The URL to crawl

        Returns:
            Dictionary containing extracted page data
        """
        try:
            # Add delay to be respectful to the server
            time.sleep(self.delay)

            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract various page elements
            page_data = {
                'url': url,
                'status_code': response.status_code,
                'title': self._extract_title(soup),
                # 'meta_description': self._extract_meta_description(soup),
                'headings': self._extract_headings(soup),
                'paragraphs': self._extract_paragraphs(soup),
                # 'links': self._extract_links(soup, url),
                # 'images': self._extract_images(soup, url),
                'text_content': self._extract_clean_text(soup),
                'structured_data': self._extract_structured_data(soup),
                'tables': self._extract_tables(soup),
                # 'forms': self._extract_forms(soup),
                # 'crawl_timestamp': time.time()
            }

            return page_data

        except requests.RequestException as e:
            self.logger.error(f"Request failed for {url}: {str(e)}")
            return {
                'url': url,
                'error': str(e),
                'status': 'failed',
                'crawl_timestamp': time.time()
            }

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract page title."""
        title_tag = soup.find('title')
        return title_tag.get_text().strip() if title_tag else ""

    def _extract_meta_description(self, soup: BeautifulSoup) -> str:
        """Extract meta description."""
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        description: str = ""

        if isinstance(meta_desc, Tag):
            content = meta_desc.attrs.get('content', '')
            description = str(content) if content else ""

        return description

    def _extract_headings(self, soup: BeautifulSoup) -> Dict[str, List[str]]:
        """Extract all heading tags (h1-h6)."""
        headings = {}
        for i in range(1, 7):
            tag = f'h{i}'
            headings[tag] = [h.get_text().strip() for h in soup.find_all(tag)]
        return headings

    def _extract_paragraphs(self, soup: BeautifulSoup) -> List[str]:
        """Extract paragraph text."""
        paragraphs = soup.find_all('p')
        return [p.get_text().strip() for p in paragraphs if p.get_text().strip()]

    def _extract_links(self, soup: BeautifulSoup, base_url: str) -> List[Dict[str, str]]:
        """Extract all links with their text and absolute URLs."""
        links = []
        for link in soup.find_all('a', href=True):
            if isinstance(link, Tag):
                href = str(link.get('href', ''))
                absolute_url = urljoin(base_url, href)
                links.append({
                    'text': link.get_text().strip(),
                    'url': absolute_url,
                    'relative_url': href
                })
        return links

    def _extract_images(self, soup: BeautifulSoup, base_url: str) -> List[Dict[str, str]]:
        """Extract image information."""
        images = []
        for img in soup.find_all('img'):
            if isinstance(img, Tag):
                src = str(img.get('src', ''))
                if src:
                    absolute_url = urljoin(base_url, src)
                    images.append({
                        'src': absolute_url,
                        'alt': img.get('alt', ''),
                        'title': img.get('title', '')
                    })
        return images

    def _extract_clean_text(self, soup: BeautifulSoup) -> str:
        """Extract clean text content from the page."""
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        # Get text and clean it up
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip()
                  for line in lines for phrase in line.split("  "))
        return ' '.join(chunk for chunk in chunks if chunk)

    def _extract_structured_data(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract JSON-LD structured data."""
        structured_data = []
        scripts = soup.find_all('script', type='application/ld+json')

        for script in scripts:
            try:
                script_text = script.get_text()
                if script_text:
                    data = json.loads(script_text)
                    structured_data.append(data)
            except json.JSONDecodeError:
                continue

        return structured_data

    def _extract_tables(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract table data."""
        tables = []
        for table in soup.find_all('table'):
            rows = []

            if isinstance(table, Tag):
                for row in table.find_all('tr'):

                    if isinstance(row, Tag):
                        cells = [cell.get_text().strip()
                                 for cell in row.find_all(['td', 'th'])]
                        if cells:
                            rows.append(cells)

            if rows:
                tables.append({
                    'headers': rows[0] if rows else [],
                    'rows': rows[1:] if len(rows) > 1 else [],
                    'raw_rows': rows
                })

        return tables

    def _extract_forms(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract form information."""
        forms = []
        for form in soup.find_all('form'):
            inputs = []

            if isinstance(form, Tag):

                for input_tag in form.find_all(['input', 'textarea', 'select']):
                    if isinstance(input_tag, Tag):
                        inputs.append({
                            'name': input_tag.get('name', ''),
                            'type': input_tag.get('type', ''),
                            'required': input_tag.has_attr('required')
                        })

                forms.append({
                    'action': form.get('action', ''),
                    'method': form.get('method', 'get'),
                    'inputs': inputs
                })

        return forms

    def get_page_summary(self, url: str) -> Dict[str, Any]:
        """
        Get a summarized version of page data suitable for MCP responses.

        Args:
            url: The URL to crawl

        Returns:
            Summarized page data
        """
        page_data = self.crawl_page(url)

        if 'error' in page_data:
            return page_data

        # Return a more concise summary
        return {
            'url': page_data['url'],
            'title': page_data['title'],
            'meta_description': page_data['meta_description'],
            'headings_count': sum(len(headings) for headings in page_data['headings'].values()),
            'paragraphs_count': len(page_data['paragraphs']),
            'links_count': len(page_data['links']),
            'images_count': len(page_data['images']),
            'has_structured_data': len(page_data['structured_data']) > 0,
            'text_preview': page_data['text_content'][:500] + "..." if len(page_data['text_content']) > 500 else page_data['text_content'],
            'crawl_timestamp': page_data['crawl_timestamp']
        }
