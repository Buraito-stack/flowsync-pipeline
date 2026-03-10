import os
import requests

MOCK_SERVER_URL = os.getenv("MOCK_SERVER_URL", "http://mock-server:5000")


def fetch_all_customers() -> list[dict]:
    """Fetch all customers from Flask mock server handling pagination."""
    all_customers = []
    page = 1
    limit = 50

    while True:
        resp = requests.get(
            f"{MOCK_SERVER_URL}/api/customers",
            params={"page": page, "limit": limit},
            timeout=10,
        )
        resp.raise_for_status()
        payload = resp.json()

        data = payload.get("data", [])
        all_customers.extend(data)

        total = payload.get("total", 0)
        if len(all_customers) >= total or not data:
            break

        page += 1

    return all_customers
