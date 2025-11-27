from sqlalchemy import Table, Column, Integer, String, Boolean, DateTime, Float, MetaData

metadata = MetaData()

symbols = Table(
    "symbols",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("symbol", String, nullable=False, unique=True),
    Column("name", String),
    Column("is_active", Boolean, default=True),
    Column("sector", String),
    Column("industry", String),
    Column("asset_type", String),
)

prices = Table(
    "prices",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("symbol", String, nullable=False, index=True),
    Column("timestamp", DateTime, nullable=False),
    Column("net", Float),
    Column("buy", Float),
    Column("sell", Float),
    Column("total", Float),
)

timeseries_mv = Table(
    "timeseries_mv",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("symbol", String, nullable=False),
    Column("interval", String),
    Column("timestamp", DateTime),
    Column("net", Float),
    Column("buy", Float),
    Column("sell", Float),
    Column("total", Float),
)
