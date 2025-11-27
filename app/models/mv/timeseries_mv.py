# app/models/mv/timeseries_mv.py
# Minimal shim to expose a Table-like object named `timeseries_mv`.
# This is intentionally simple: it provides the column names the app expects.
# If your real project uses ORM models, you can replace this later.

from sqlalchemy import Table, MetaData, Column, String, Float, TIMESTAMP

metadata = MetaData()

timeseries_mv = Table(
    "timeseries_mv",
    metadata,
    Column("timestamp", TIMESTAMP, nullable=True),
    Column("symbol", String, nullable=False),
    Column("net", Float, nullable=True),
    Column("buy", Float, nullable=True),
    Column("sell", Float, nullable=True),
    Column("total", Float, nullable=True),
)
