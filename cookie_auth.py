class Authenticator:
    """
    A class to authenticate requests using cookies.

    """

    def __init__(self, cookie_string: str) -> None:
        """
        Initialize the Authenticator with a cookie string.

        Args:
            cookie_string: The cookie string to parse.
        """
        self.cookies: dict = self._parse_cookies(cookie_string)

    @staticmethod
    def _parse_cookies(cookie_string: str) -> dict:
        """
        Convert the cookie string to a dictionary.

        Args:
            cookie_string: The cookie string to parse.

        Returns:
            A dictionary of the parsed cookies.
        """
        return {
            cookie.split("=")[0]: cookie.split("=")[1]
            for cookie in cookie_string.split("; ")
        }

    def get_cookies(self) -> dict:
        """
        Return the parsed cookies.

        Returns:
            The parsed cookies.
        """
        return self.cookies
