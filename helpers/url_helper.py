from urllib.parse import urlparse

import requests


class UrlHelper:

    @staticmethod
    def is_url_valid(url: str) -> bool:
        parsed = urlparse(url)
        is_valid = all([parsed.scheme, parsed.netloc])
        if not is_valid:
            print("❌ Invalid URL. Please enter a valid URL (e.g. https://example.com)")
            return False
        return True

    @staticmethod
    def is_url_reachable(url: str) -> bool:
        try:
            response = requests.head(url, timeout=3)
            is_reachable = response.status_code < 400
            if not is_reachable:
                print("❌ Webpage in the given URL is not reachable. Retry with a different URL.")
                return False
            return True
        except requests.RequestException:
            return False