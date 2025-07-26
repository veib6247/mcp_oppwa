import json

from web_crawler import WebCrawler


def main():
    """Test the webcrawler"""

    # Initialize the web crawler
    crawler = WebCrawler()

    # Example URL to crawl
    url = "https://docs.oppwa.com/integrations/widget/api"

    # Crawl the URL and print the results
    result = crawler.crawl_page(url)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
