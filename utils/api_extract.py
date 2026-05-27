import requests
import logging

logger = logging.getLogger(__name__)


def extractApis(url: str) -> dict | list: 
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        logger.error(f"HTTP error for {url}: {e}")
    except requests.ConnectionError as e:
        logger.error(f"Connection failed for {url}: {e}")
    except requests.Timeout:
        logger.error(f"Request timed out for {url}: {e}")
    except requests.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON from {url}: {e}")

    return {}
        