import datetime
import random
import string
import uuid

from typing import Optional
from psycopg.types.json import Json
from private_stuff import *

class GroceryOrderGenerator:
    def __init__(self, num_orders=10_000, items_per_order=5):
        self.num_orders = num_orders
        self.items_per_order = items_per_order
        self.products = [
            ("apples", 0.5, 2.0),
            ("bananas", 0.3, 1.0),
            ("milk", 2.0, 4.0),
            ("bread", 1.5, 4.5),
            ("eggs", 2.0, 6.0),
            ("chicken", 5.0, 15.0),
            ("cheese", 3.0, 10.0),
            ("cereal", 2.5, 7.0),
            ("yogurt", 0.7, 2.5),
            ("coffee", 4.0, 20.0),
        ]

    def _random_phone(self) -> str:
        area = random.randint(200, 999)
        prefix = random.randint(200, 999)
        line = random.randint(0, 9999)
        return f"+1-{area:03d}-{prefix:03d}-{line:04d}"

    def _random_account_id(self) -> str:
        return "".join(random.choices(string.ascii_uppercase + string.digits, k=10))

    def _random_email(self, account_id: str) -> str:
        domains = ["example.com", "grocer.com", "mail.com", "shopper.net"]
        return f"user_{account_id.lower()}@{random.choice(domains)}"

    def _random_line_item(self) -> dict:
        name, min_price, max_price = random.choice(self.products)
        unit_price = round(random.uniform(min_price, max_price), 2)
        quantity = random.randint(1, 5)
        line_total = round(unit_price * quantity, 2)
        return {
            "productId": str(uuid.uuid4()),
            "name": name,
            "unitPrice": unit_price,
            "quantity": quantity,
            "lineTotal": line_total,
        }

    def build_order(self) -> dict:
        account_id = self._random_account_id()
        line_items = [self._random_line_item() for _ in range(self.items_per_order)]
        total_cost = round(sum(item["lineTotal"] for item in line_items), 2)
        return {
            "orderId": str(uuid.uuid4()),
            "account": {
                "accountId": account_id,
                "phone": self._random_phone(),
                "email": self._random_email(account_id),
            },
            "lineItems": line_items,
            "totalCost": total_cost,
        }

def random_status() -> str:
    return random.choice(["pending", "delivered", "cancelled"])

def random_date_within_days(days: int = 30) -> datetime.datetime:
    now = datetime.datetime.now(tz=datetime.timezone.utc)
    delta_days = random.randint(0, days)
    delta_seconds = random.randint(0, 24 * 3600)
    return now - datetime.timedelta(days=delta_days, seconds=delta_seconds)

def random_promotion_code() -> Optional[str]:
    codes = [None, None, "PROMO10", "FREESHIP", "WELCOME5"]
    return random.choice(codes)

def random_notes() -> Optional[str]:
    notes = [
        None,
        "Leave at front door.",
        "Call on arrival.",
        "Substitute out-of-stock items.",
        "No plastic bags, please.",
    ]
    return random.choice(notes)

def insert_grocery_orders(num_orders: int = 10_000):
    generator = GroceryOrderGenerator(num_orders=num_orders)

    insert_sql = """
        INSERT INTO grocery_activity (
            pk,
            accountid,
            date_of_order,
            status,
            notes,
            promotion_code,
            order_data
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            batch = []
            batch_size = 500

            for _ in range(num_orders):
                order = generator.build_order()
                account_id = order["account"]["accountId"]

                row = (
                    uuid.uuid4(),                 # pk
                    account_id,                  # accountid
                    random_date_within_days(),   # date_of_order
                    random_status(),             # status
                    random_notes(),              # notes
                    random_promotion_code(),     # promotion_code
                    Json(order),                 # order_data (JSONB)
                )
                batch.append(row)

                if len(batch) >= batch_size:
                    cur.executemany(insert_sql, batch)
                    batch.clear()

            if batch:
                cur.executemany(insert_sql, batch)

if __name__ == "__main__":
    # Fill this with your CockroachDB connection info.

    insert_grocery_orders(num_orders=10_000)
    print("Inserted 10,000 grocery_activity rows.")

