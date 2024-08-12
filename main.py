from cookie_auth import Authenticator
from dotenv import load_dotenv
from portfolio import PortfolioRequester
import os
import typer

load_dotenv(override=True)

app = typer.Typer(add_completion=False)

DEFAULT_TICKER = "%5EGSPC"


@app.command()
def compare(
    ticker: str = typer.Option(
        DEFAULT_TICKER,
        help="Ticker of the stock to compare against. Defaults to S&P 500.",
    ),
):
    """
    Compare your portfolio against a stock / index.

    e.g. https://finance.yahoo.com/chart/CNX1.L
    Use: "CNX1.L" for your input (no need for quotes)

    Common tickers:
    - S&P 500: %5EGSPC
    - VG FTSE All-World: VWRL.L
    - iShares NASDAQ 100: CNX1.L

    Args:
        ticker (str): Ticker of the stock to compare against. Defaults to S&P 500

    """
    cookie_string = os.getenv("COOKIE") or typer.prompt("Enter your cookie string")
    auth: Authenticator = Authenticator(cookie_string=cookie_string)

    PortfolioRequester(
        authenticator=auth,
        refresh_external_data=True,
        external_ticker=ticker,
    ).get_portfolio(show=True)


if __name__ == "__main__":
    app()
