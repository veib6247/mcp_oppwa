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

    try:
        with open("dist/output.json", "w") as file:
            json.dump(result, file, indent=2)

    except Exception as e:
        print(f"Failed to output file:", e)


if __name__ == "__main__":
    main()
