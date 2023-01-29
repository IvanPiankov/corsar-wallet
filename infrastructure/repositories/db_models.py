from sqlalchemy import MetaData, Table, Column, DECIMAL, String, text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ENUM

from models.enums import WalletTypes

metadata = MetaData()

wallets = Table(
    "wallets",
    metadata,
    Column("wallet_id", UUID(as_uuid=True), nullable=False, primary_key=True),
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False),
    Column("wallet_type", ENUM(WalletTypes, name="wallet_types"), nullable=False),
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
    Column("password", String, nullable=False),
    Column("wallet_currency", String, nullable=False)
)
