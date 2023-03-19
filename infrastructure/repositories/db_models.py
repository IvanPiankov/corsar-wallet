from sqlalchemy import DECIMAL, Column, DateTime, ForeignKey, MetaData, String, Table, text
from sqlalchemy.dialects.postgresql import ENUM, UUID

from models.enums import AccountTypes

metadata = MetaData()

wallets = Table(
    "wallets",
    metadata,
    Column("wallet_id", UUID(as_uuid=True), nullable=False, primary_key=True),
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False),
    Column("wallet_type", ENUM(AccountTypes, name="account_types"), nullable=False),
    Column("balance", DECIMAL, nullable=False),
    Column("currency", String, nullable=False),
    Column("created_at", DateTime(timezone=True), server_default=text("timezone('utc', now())"), nullable=False),
    Column("updated_at", DateTime(timezone=True), server_default=text("timezone('utc', now())"), nullable=False),
)

users = Table(
    "users",
    metadata,
    Column("user_id", UUID(as_uuid=True), nullable=False, primary_key=True),
    Column("login", String, nullable=False, unique=True),
    Column("email", String, nullable=False, unique=True),
    Column("hashed_password", String, nullable=False),
    Column("wallet_currency", String, nullable=True),
)
