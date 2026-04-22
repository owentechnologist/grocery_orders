"""
Create tables for grocery order data.

This script creates the grocery_activity table for storing order data
with JSONB format, suitable for CockroachDB performance testing.
"""

from private_stuff import get_connection


def create_grocery_activity_table():
    """Create the grocery_activity table with appropriate schema."""

    create_table_sql = """
    CREATE TABLE IF NOT EXISTS grocery_activity (
        pk UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        accountid STRING NOT NULL,
        date_of_order TIMESTAMP NOT NULL,
        status STRING NOT NULL,
        notes STRING,
        promotion_code STRING,
        order_data JSONB NOT NULL,

        INDEX idx_accountid (accountid),
        INDEX idx_date_of_order (date_of_order),
        INDEX idx_status (status)
    )
    """

    with get_connection() as conn:
        # Use autocommit for DDL per CockroachDB best practices
        conn.autocommit = True
        with conn.cursor() as cur:
            print("Creating grocery_activity table...")
            cur.execute(create_table_sql)
            print("✓ Table created successfully")

            # Verify table creation
            cur.execute("""
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_name = 'grocery_activity'
                ORDER BY ordinal_position
            """)

            print("\nTable schema:")
            for row in cur.fetchall():
                print(f"  {row[0]}: {row[1]}")


def drop_grocery_activity_table():
    """Drop the grocery_activity table if it exists."""

    drop_table_sql = "DROP TABLE IF EXISTS grocery_activity CASCADE"

    with get_connection() as conn:
        conn.autocommit = True
        with conn.cursor() as cur:
            print("Dropping grocery_activity table...")
            cur.execute(drop_table_sql)
            print("✓ Table dropped successfully")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--drop":
        drop_grocery_activity_table()
    else:
        create_grocery_activity_table()
        print("\nTable ready for data loading.")
        print("Run 'python loadgrocerytable.py' to populate with test data.")
