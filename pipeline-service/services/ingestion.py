import os
import requests
from datetime import datetime, date
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from models.customer import Customer

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


def parse_customer(raw: dict) -> dict:
    """Parse raw dict into values suitable for DB upsert."""
    dob = raw.get("date_of_birth")
    created = raw.get("created_at")

    return {
        "customer_id": raw["customer_id"],
        "first_name": raw["first_name"],
        "last_name": raw["last_name"],
        "email": raw["email"],
        "phone": raw.get("phone"),
        "address": raw.get("address"),
        "date_of_birth": date.fromisoformat(dob) if dob else None,
        "account_balance": Decimal(str(raw["account_balance"])) if raw.get("account_balance") is not None else None,
        "created_at": datetime.fromisoformat(created.replace("Z", "+00:00")) if created else None,
    }


def upsert_customers(db: Session, customers: list[dict]) -> int:
    """Upsert customer records into PostgreSQL. Returns count processed."""
    if not customers:
        return 0

    parsed = [parse_customer(c) for c in customers]

    stmt = insert(Customer).values(parsed)
    stmt = stmt.on_conflict_do_update(
        index_elements=["customer_id"],
        set_={
            "first_name": stmt.excluded.first_name,
            "last_name": stmt.excluded.last_name,
            "email": stmt.excluded.email,
            "phone": stmt.excluded.phone,
            "address": stmt.excluded.address,
            "date_of_birth": stmt.excluded.date_of_birth,
            "account_balance": stmt.excluded.account_balance,
            "created_at": stmt.excluded.created_at,
        },
    )

    db.execute(stmt)
    db.commit()
    return len(parsed)
