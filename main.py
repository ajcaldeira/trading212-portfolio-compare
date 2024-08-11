from commons import ExternalData
from cookie_auth import Authenticator
from dotenv import load_dotenv
from portfolio import PortfolioRequester
import os

load_dotenv(override=True)


if __name__ == "__main__":
    cookie_string: str = os.getenv("COOKIE") or input("Enter the cookie string: ")
    auth: Authenticator = Authenticator(cookie_string=cookie_string)

    PortfolioRequester(
        authenticator=auth,
        refresh_external_data=True,
        external_ticker=ExternalData.VWRLL.value,
    ).get_portfolio(show=True)
