import os, psycopg

DATABASE_URL = os.getenv("DATABASE_URL")

def get_conn():
    return psycopg.connect(DATABASE_URL, autocommit=True, row_factory=psycopg.rows.dict_row)

def create_schema():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
                        CREATE TABLE IF NOT EXISTS rooms (
                            id SERIAL PRIMARY KEY,
                            room_number INT NOT NULL,
                            created_at TIMESTAMP DEFAULT now()
                        );

                        ALTER TABLE rooms ADD COLUMN IF NOT EXISTS room_type VARCHAR;

                        ALTER TABLE rooms ADD COLUMN IF NOT EXISTS price NUMERIC NOT NULL CHECK (price > 0);

                        CREATE Table IF NOT EXISTS guests(
                            id SERIAL PRIMARY KEY,
                            first_name VARCHAR NOT NULL,
                            last_name VARCHAR NOT NULL,
                            address VARCHAR
                        );

                        CREATE TABLE IF NOT EXISTS bookings(
                            id SERIAL PRIMARY KEY,
                            guest_id INT REFERENCES guests(id) NOT NULL,
                            room_id INT REFERENCES rooms(id) NOT NULL,
                            date_from TIMESTAMP NOT NULL,
                            date_to TIMESTAMP NOT NULL,
                            CHECK (date_from < date_to),
                            additional_info VARCHAR
                        );
                    """)
