from mcp.server.fastmcp import FastMCP

from web_crawler import WebCrawler

# Create an MCP server
mcp = FastMCP("payreto-api-helper")


@mcp.tool()
def oppwa_copy_and_pay_integration_details() -> dict[str, str]:
    """Returns the COPYandPAY integration page."""
    crawler = WebCrawler()
    return crawler.crawl_page("https://docs.oppwa.com/integrations/widget")


@mcp.tool()
def oppwa_copy_and_pay_integration_api_reference() -> dict[str, str]:
    """Returns the COPYandPAY API reference page."""
    crawler = WebCrawler()
    return crawler.crawl_page("https://docs.oppwa.com/integrations/widget/api")


@mcp.tool()
def oppwa_pay_by_link_integration() -> dict[str, str]:
    """Returns the details from the PAY By Link oppwa integration page."""
    crawler = WebCrawler()
    return crawler.crawl_page("https://docs.oppwa.com/integrations/paybylink")


@mcp.tool()
def oppwa_pay_by_link_integration_api_reference() -> dict[str, str]:
    """Returns the details from the PAY By Link oppwa API reference page."""
    crawler = WebCrawler()
    return crawler.crawl_page("https://docs.oppwa.com/integrations/paybylink/api")


@mcp.tool()
def oppwa_transaction_reporting() -> dict[str, str]:
    """Transaction reports allow to retrieve detailed transactional data from the oppwa platform."""
    crawler = WebCrawler()
    return crawler.crawl_page("https://docs.oppwa.com/integrations/reporting/transaction")


# @mcp.tool()
# def prtpg_standard_checkout() -> dict[str, str]:
#     """Returns the details from the Standard Checkout integration page of the prtpg platform."""
#     crawler = WebCrawler()
#     return crawler.crawl_page("https://docs.prtpg.com/integration/standard-checkout.php")


# @mcp.tool()
# def prtpg_standard_checkout_api_reference() -> dict[str, str]:
#     """Returns the details from the Standard Checkout API reference page of the prtpg platform."""
#     crawler = WebCrawler()
#     return crawler.crawl_page("https://docs.prtpg.com/integration/standard-checkout-specifications.php")
