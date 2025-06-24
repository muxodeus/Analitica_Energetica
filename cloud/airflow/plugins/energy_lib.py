import os
import psycopg2
import pandas as pd
from datetime import datetime
DSN = (
    f"dbname={os.getenv('DB_NAME')} "
    f"user={os.getenv('DB_USER')} "
    f"host={os.getenv('DB_HOST')} "
    f"password={os.getenv('DB_PASS')}"
)

def compute_minute_stats(window_s=60):
    conn = psycopg2.connect(DSN); cur=conn.cursor()
    cur.execute(f"""
      SELECT vals[1] AS r1, vals[2] AS r2, vals[3] AS r3, vals[4] AS r4
      FROM raw_readings
      WHERE ts > now() - interval '{window_s} seconds'
    """)
    df = pd.DataFrame(cur.fetchall(), columns=['r1','r2','r3','r4'])
    stats = df.agg(['min','max','mean']).to_dict()
    for sensor, vals in stats.items():
        cur.execute(f"""
         INSERT INTO minute_stats(sensor, ts, min, max, avg)
         VALUES(%s, now(), %s, %s, %s)
        """, (sensor, vals['min'], vals['max'], vals['mean']))
    conn.commit(); conn.close()

def compute_trends(periods=['1h','1d','7d','30d']):
    conn = psycopg2.connect(DSN); cur=conn.cursor()
    for p in periods:
        cur.execute(f"""
          INSERT INTO trends(period, ts, slope)
          SELECT '{p}', now(),
              REGR_SLOPE(avg, extract(epoch from ts))
          FROM minute_stats WHERE ts > now() - interval '{p}'
        """)
    conn.commit(); conn.close()
