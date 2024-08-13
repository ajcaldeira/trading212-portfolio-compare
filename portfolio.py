from commons import T212Periods
from cookie_auth import Authenticator
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path
import cloudscraper
import json
import matplotlib.pyplot as plt
import os
import requests

load_dotenv(override=True)


class PortfolioRequester:
    URL = "https://live.services.trading212.com/rest/v2/portfolio?period={period}"
    EXTERNAL_URL = "https://query2.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1mo&range=10y"

    def __init__(
        self,
        authenticator: Authenticator,
        external_ticker: str = "5EGSPC",
        refresh_external_data: bool = False,
    ):
        """
        Initialize the PortfolioRequester with an Authenticator and User-Agent.
        """
        self.authenticator = authenticator
        self.result: list = []
        self.start_date: str | None = None
        self.refresh_external_data = refresh_external_data
        self.external_ticker: str = external_ticker
        self.EXTERNAL_URL = self.EXTERNAL_URL.format(ticker=external_ticker)
        self.scraper = cloudscraper.create_scraper()

    def get_portfolio(self, show: bool = True) -> None:
        """
        Perform the GET request to retrieve portfolio data.

        Args:
            show (bool): Whether to show the plot or not
        """
        self._get_portfolio_snapshots()
        self._plot_percentage(against=self.external_ticker, show=show)

    def _get_portfolio_snapshots(self) -> None:
        """
        Perform the GET request to retrieve portfolio snapshot data.
        """
        historical_snapshots_response = self.scraper.get(
            self.URL.format(period=T212Periods.ALL.value),
            cookies=self.authenticator.get_cookies(),
        )
        today_snapshots_response = self.scraper.get(
            self.URL.format(period=T212Periods.LAST_DAY.value),
            cookies=self.authenticator.get_cookies(),
        )

        try:
            historical_snapshots_response.raise_for_status()
            today_snapshots_response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise Exception(f"Failed to retrieve data: {e}")

        self._format_portfolio_data(
            self._join_historical_to_today(
                historical_snapshots_response.json(), today_snapshots_response.json()
            )
        )  # Return the JSON data

    def _join_historical_to_today(
        self, historical_data: dict[str, list], today_data: dict[str, list]
    ) -> dict:
        """
        Join the historical data to the today's data.

        Args:
            historical_data (dict): The historical data
            today_data (dict): The today's data

        Returns:
            dict: The joined data
        """
        historical_data["snapshots"].append(today_data["snapshots"][-1])
        return historical_data

    def _format_portfolio_data(self, data: dict) -> None:
        """
        Convert all "time" fields to the format "MM-YYYY" and calculate the percentage change.

        Args:
            data (dict): The portfolio data
        """
        total_investment = 0
        total_ppl = 0
        for snapshot in data["snapshots"]:
            date_obj = datetime.strptime(
                snapshot["time"], "%Y-%m-%dT%H:%M:%SZ"
            ).strftime("%m-%Y")
            if self.start_date is None:
                self.start_date = date_obj
            snapshot["time"] = date_obj
            percentage = snapshot["ppl"] / snapshot["investment"] * 100
            total_investment += snapshot["investment"]
            total_ppl += snapshot["ppl"]

            self.result.append(
                {
                    "investment": snapshot["investment"],
                    "ppl": snapshot["ppl"],
                    "percentage": percentage,
                }
            )

        data["snapshots"][-1]["time"] = "Today"
        self._prepare_plotting_from_original(data)
        self._prepare_plotting_from_processed()

    def _prepare_plotting_from_original(self, data: dict) -> None:
        """
        Prepare the data for plotting from the original data.

        Args:
            data (dict): The portfolio
        """
        self.x = [snapshot["time"] for snapshot in data["snapshots"]]
        self.investments = [snapshot["investment"] for snapshot in data["snapshots"]]
        self.ppls = [snapshot["ppl"] for snapshot in data["snapshots"]]

    def _prepare_plotting_from_processed(self) -> None:
        """
        Prepare the data for plotting from the processed data.

        """
        self.y1 = [snapshot["percentage"] for snapshot in self.result]

    def _plot_percentage(self, against: str, show=True):
        """
        Plot the percentage gain/loss over time.

        Args:
            against (str): The external ticker to compare against
            show (bool): Whether to show the plot or not
        """
        # Plot Percentage Gain/Loss and PPL over time
        fig, ax1 = plt.subplots()
        color = "tab:red"
        ax1.set_xlabel("Time")
        ax1.set_ylabel("Percentage", color=color)

        # Plot the percentage gain/loss
        ax1.plot(self.x, self.y1, color=color, label="Portfolio % Change")
        ax1.tick_params(axis="y", labelcolor=color)

        # Annotate the final value
        final_portfolio_value = self.y1[-1]
        ax1.annotate(
            f"{final_portfolio_value:.2f}%",
            xy=(self.x[-1], self.y1[-1]),
            xytext=(5, 0),
            textcoords="offset points",
            color=color,
            fontsize=10,
            fontweight="bold",
        )

        match against:
            case "T212PPL":
                ax2 = ax1.twinx()
                color = "tab:blue"
                self.y2 = [snapshot["ppl"] for snapshot in self.result]
                ax2.set_ylabel("PPL", color=color)
                ax2.plot(self.x, self.y2, color=color)
                ax2.tick_params(axis="y", labelcolor=color)
                final_ppl_value = self.y2[-1]
                ax2.annotate(
                    f"{final_ppl_value:.2f}",
                    xy=(self.x[-1], self.y2[-1]),
                    xytext=(5, 0),
                    textcoords="offset points",
                    color=color,
                    fontsize=10,
                    fontweight="bold",
                )
            case _:
                self._map_external_data_to_t212()
                color = "tab:gray"
                ax1.plot(
                    self.x,
                    self.y2,
                    color=color,
                    label=f"{self.external_ticker} % Change",
                )
                ax1.fill_between(self.x, self.y2, color=color, alpha=0.2)
                final_value = self.y2[-1]
                ax1.annotate(
                    f"{final_value:.2f}%",
                    xy=(self.x[-1], self.y2[-1]),
                    xytext=(5, 0),
                    textcoords="offset points",
                    color=color,
                    fontsize=10,
                    fontweight="bold",
                )

        ax1.set_xticks(self.x[:: len(self.result) // 10])  # Adjust the step for x-ticks
        fig.tight_layout()
        plt.title("Percentage Gain/Loss Comparrison")
        plt.grid(True)
        plt.subplots_adjust(top=0.85)
        ax1.legend(loc="best")
        if show:
            plt.show()
        else:
            return fig

    def _map_external_data_to_t212(self):
        """
        Map the external data to the Trading 212 data.
        """
        adjclose = self._get_external_data()

        # Calculate percentage changes
        percent_changes = [0]  # Start with 0% for the first entry
        initial_close = adjclose[0]  # The first value to compare against

        for i in range(1, len(adjclose)):
            current_close = adjclose[i]
            percentage_change = ((current_close - initial_close) / initial_close) * 100
            percent_changes.append(percentage_change)

        self.y2 = percent_changes

    def _get_external_data(self) -> list:
        """
        Get the external data from the file system or yahoo finance.

        Returns:
            list: The adjusted close prices of the external data

        """

        data_path = Path.cwd() / "data" / f"{self.external_ticker}.json"

        if self.refresh_external_data:
            response = self.scraper.get(self.EXTERNAL_URL)
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                raise Exception(f"Failed to retrieve external data: {e}")

            data = response.json()
            with data_path.open("w") as file:
                json.dump(data, file)
        else:
            external_data_file = os.getenv("EXTERNAL_DATA_FILE")
            if external_data_file is None:
                raise Exception("The external data file is not set.")
            data_path = Path.cwd() / "data" / external_data_file
            with data_path.open("r") as file:
                data = json.load(file)

        # Error check that the ticker is valid and the data is available
        if data["chart"]["error"]:
            Path.unlink(data_path)
            raise Exception(
                f"Failed to retrieve data: {data['chart']['error']['description']}. Ticker {self.external_ticker} may be invalid."
            )

        try:
            # Extract timestamps and adjusted close prices
            timestamps = data["chart"]["result"][0]["timestamp"]
            adjclose = data["chart"]["result"][0]["indicators"]["adjclose"][0][
                "adjclose"
            ]
        except KeyError:
            raise Exception(
                "Failed to extract data from the external data. Check your ticker."
            )

        # Convert the timestamps to dates
        dates = [
            datetime.fromtimestamp(timestamp).strftime("%m-%Y")
            for timestamp in timestamps
        ]

        start_date = self.start_date
        if start_date is not None:
            start_index: int = dates.index(start_date)
            adjclose = adjclose[start_index:]

            return adjclose
        raise Exception("The start date is not set.")
