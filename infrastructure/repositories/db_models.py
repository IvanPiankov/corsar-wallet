from sqlalchemy import DECIMAL, Column, DateTime, ForeignKey, Integer, MetaData, String, Table, text
from sqlalchemy.dialects.postgresql import UUID

metadata = MetaData()

accounts = Table(
    "accounts",
    metadata,
    Column("account_id", UUID(as_uuid=True), nullable=False, primary_key=True),
    Column("name", String, nullable=False),
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False),
    Column("account_type", String, nullable=False),
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

category = Table(
    "category",
    metadata,
    Column("category_id", Integer, primary_key=True, autoincrement=True, nullable=False),
    Column("name", String, nullable=False),
    # TODO: Добавить возможность привязывать категорию к пользователю и сделать возможность шарить их
    Column("icon", String, nullable=False),
)

subcategory = Table(
    "subcategory",
    metadata,
    Column("subcategory_id", Integer, primary_key=True, autoincrement=True, nullable=False),
    Column("category_id", Integer, ForeignKey("category.category_id"), nullable=False),
    Column("name", String, nullable=False),
    # TODO: Добавить возможность привязывать категорию к пользователю и сделать возможность шарить их
    Column("icon", String, nullable=False),
)
