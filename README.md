# Trading212 Portfolio Compare

## Description

Trading212 does not offer fantastic data insights. 1 primary thing I would love to see if my portfolio percentage gain/loss instead of the commulative investment amount. This is the purpouse of this project!

Moreover, I want to compare how my portfolio performs against a specific ticker.

## Features

- Cookie Authorization as T212 does not offer the required data in the API
- See your portfolio percentage gain/loss over time (using the same snapshot as the home page in T212)
- Overlay any ticker over your portfolio percentage gain/loss line on a graph

## Installation

To install this project, follow these steps:

1. Install [Poetry](https://python-poetry.org/docs/#installing-with-pipx) and Make (if you're on windows: `choco install make`) on your system
2. Clone the repo
3. Run `poetry install` in your terminal
4. Run `poetry shell` in your terminal to activate the virtual environment
5. Run `make compare ticker=AAPL` (any ticker you want to compare against)


## Usage

To use this project, follow these guidelines:

### 1. Authenticate your account
1. Rename/make a copy of the .env.sample file and name it .env in the project's root directory
2. Log into Trading 212 in your web browser, and press F12.
3. In the developer panel, navigate to the Network tab
4. Navigate to your portfolio page in T212 and refresh the page
5. In the Network tab in the developer panel look for the filter search box and type in settings
6. Click the result and on the right hand side select Headers then expand the Request headers section
7. Under the request headers look for the "cookie:" field and copy the cookie data to the right.
8. Paste the cooke data in the .env file and save it

### 2. Run the software
1. In the terminal run the command `make run-me ticker=AAPL` or `python3 main.py --ticker AAPL`

#### Compare against a custom ticker
If you want to compare against a ticker that is not there, you can add your own ticker from yahoo finance. (make sure to use the ticker name specified in the URL of the chart page). Just add it to the enum and replace the value as I have shown above.

## What it all looks like

![image](https://github.com/user-attachments/assets/56352ef6-aa1c-4dac-aae9-e6652ea01854)

## License

This project is licensed under the [GPL-3.0 license](https://github.com/ajcaldeira/trading212-portfolio-compare?tab=GPL-3.0-1-ov-file).
