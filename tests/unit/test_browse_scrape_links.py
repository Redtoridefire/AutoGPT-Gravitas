from bs4 import BeautifulSoup
from autogpt.commands.web_requests import scrape_links, extract_hyperlinks

"""
Code Analysis

Objective:
The objective of the 'scrape_links' function is to scrape hyperlinks from a
given URL and return them in a formatted way.

Inputs:
- url: a string representing the URL to be scraped.

Flow:
1. Send a GET request to the given URL using the requests library and the user agent header from the config file.
2. Check if the response contains an HTTP error. If it does, return "error".
3. Parse the HTML content of the response using the BeautifulSoup library.
4. Remove any script and style tags from the parsed HTML.
5. Extract all hyperlinks from the parsed HTML using the 'extract_hyperlinks' function.
6. Format the extracted hyperlinks using the 'format_hyperlinks' function.
7. Return the formatted hyperlinks.

Outputs:
- A list of formatted hyperlinks.

Additional aspects:
- The function uses the 'requests' and 'BeautifulSoup' libraries to send HTTP
requests and parse HTML content, respectively.
- The 'extract_hyperlinks' function is called to extract hyperlinks from the parsed HTML.
- The 'format_hyperlinks' function is called to format the extracted hyperlinks.
- The function checks for HTTP errors and returns "error" if any are found.
"""


class TestScrapeLinks:
    """
    Tests that the function returns a list of formatted hyperlinks when
    provided with a valid url that returns a webpage with hyperlinks.
    """

    def test_valid_url_with_hyperlinks(self):
        url = "https://www.google.com"
        result = scrape_links(url)
        assert len(result) > 0
        assert isinstance(result, list)
        assert isinstance(result[0], str)

    def test_valid_url(self, mocker):
        """Test that the function returns correctly formatted hyperlinks when given a valid url."""
        # Mock the requests.get() function to return a response with sample HTML containing hyperlinks
        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.text = (
            "<html><body><a href='https://www.google.com'>Google</a></body></html>"
        )
        mocker.patch("requests.Session.get", return_value=mock_response)

        # Call the function with a valid URL
        result = scrape_links("https://www.example.com")

        # Assert that the function returns correctly formatted hyperlinks
        assert result == ["Google (https://www.google.com)"]

    def test_invalid_url(self, mocker):
        """Test that the function returns "error" when given an invalid url."""
        # Mock the requests.get() function to return an HTTP error response
        mock_response = mocker.Mock()
        mock_response.status_code = 404
        mocker.patch("requests.Session.get", return_value=mock_response)

        # Call the function with an invalid URL
        result = scrape_links("https://www.invalidurl.com")

        # Assert that the function returns "error"
        assert "Error:" in result

    def test_no_hyperlinks(self, mocker):
        """Test that the function returns an empty list when the html contains no hyperlinks."""
        # Mock the requests.get() function to return a response with sample HTML containing no hyperlinks
        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.text = "<html><body><p>No hyperlinks here</p></body></html>"
        mocker.patch("requests.Session.get", return_value=mock_response)

        # Call the function with a URL containing no hyperlinks
        result = scrape_links("https://www.example.com")

        # Assert that the function returns an empty list
        assert result == []

    def test_scrape_links_with_few_hyperlinks(self, mocker):
        """Test that scrape_links() correctly extracts and formats hyperlinks from a sample HTML containing a few hyperlinks."""
        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.text = """
            <html>
                <body>
                    <div id="google-link"><a href="https://www.google.com">Google</a></div>
                    <div id="github"><a href="https://github.com">GitHub</a></div>
                    <div id="CodiumAI"><a href="https://www.codium.ai">CodiumAI</a></div>
                </body>
            </html>
        """
        mocker.patch("requests.Session.get", return_value=mock_response)

        # Call the function being tested
        result = scrape_links("https://www.example.com")

        # Assert that the function returns a list of formatted hyperlinks
        assert isinstance(result, list)
        assert len(result) == 3
        assert result[0] == "Google (https://www.google.com)"
        assert result[1] == "GitHub (https://github.com)"
        assert result[2] == "CodiumAI (https://www.codium.ai)"

    def test_extract_hyperlinks(self):
        # Create a BeautifulSoup object from a sample HTML containing hyperlinks
        body = """
        <body>
        <a href="https://google.com">Google</a>
        <a href="foo.html">Foo</a>
        <div>Lorem Ipsum. Dolore sit amet.</div>
        </body>
        """
        soup = BeautifulSoup(body, "html.parser")

        # Call the function being tested
        links = extract_hyperlinks(soup, "http://example.com")

        # Assert that the function returns a list of tuples containing the link text and the link URL
        assert links == [
            ("Google", "https://google.com"),
            ("Foo", "http://example.com/foo.html"),
        ]
