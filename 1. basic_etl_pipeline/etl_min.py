# etl_min.py (psycopg v3)
import requests
import pandas as pd
import psycopg  # v3

# 1) Extract
data = requests.get("https://jsonplaceholder.typicode.com/posts", timeout=10).json()

# 2) Transform
df = pd.DataFrame(data)[["userId", "id", "title"]]

# 3) Load
with psycopg.connect("dbname=mydb user=myuser password=mypassword host=localhost port=5433") as conn:
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS posts (
          user_id  INTEGER,
          post_id  INTEGER PRIMARY KEY,
          title    TEXT
        );
        """)

        for row in df.itertuples(index=False):
            cur.execute(
                "INSERT INTO posts (user_id, post_id, title) VALUES (%s, %s, %s) ON CONFLICT (post_id) DO NOTHING",
                (row.userId, row.id, row.title),
            )
    # commit happens when the 'with conn' block exits
