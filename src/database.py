import os
import urllib # For encoding the connection string
from datetime import datetime , timezone # For timestamping log entries
from dotenv import load_dotenv # For loading environment variables from .env file
from sqlalchemy import create_engine , Column , Integer , String , Float , DateTime , ForeignKey 
# For defining the database schema
from sqlalchemy.orm import declarative_base , relationship # For defining relationships between tables

# Load environment variables from .env file
load_dotenv()

# Read the variables from the environment
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")
db_port = os.getenv("DB_PORT")


# Create the Connection String for Azure SQL and pyodbc
# We use the urllib for encoding correct special characters in the password
params = urllib.parse.quote_plus(
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={db_host};"
    f"DATABASE={db_name};"
    f"UID={db_user};"
    f"PWD={db_password};"
    f"Encrypt=yes;"
    f"TrustServerCertificate=no;"
    f"Connection Timeout=30;"
)
connection_string = f"mssql+pyodbc:///?odbc_connect={params}"

# Connect to the database using SQLAlchemy
engine = create_engine(connection_string)
Base = declarative_base()


# --- DEFINE TABLES (SCHEMA) ---

# Table 1: Products' Categories
class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer , primary_key=True , autoincrement=True)
    name = Column(String(50) , nullable=False)

# Table 2: Products
class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer , primary_key=True , autoincrement=True)
    name = Column(String(100) , nullable=False)
    price = Column(Float , nullable=False)
    category_id = Column(Integer , ForeignKey('category.id'))
    
# Table 3: Customers
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer , primary_key=True , autoincrement=True)
    username = Column(String(50) , nullable=False)
    email = Column(String(100) , nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

# Table 4: Sales_Representative
class Seller(Base):
    __tablename__ = 'seller'
    id = Column(Integer , primary_key=True , autoincrement=True)
    full_name = Column(String(100) , nullable=False)
    email = Column(String(100) , nullable=False)

# Table 5: Orders
class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer , primary_key=True , autoincrement=True)
    user_id = Column(Integer , ForeignKey('user.id'))
    seller_id = Column(Integer , ForeignKey('seller.id'))
    order_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    status = Column(String(20) , default='pending')
    product_id = Column(Integer , ForeignKey('product.id'))
    quantity = Column(Integer , nullable=False)
    price_at_purchase = Column(Float , nullable=False)

# --- EXECUTE THE CREATION OF TABLES IN THE DATABASE ---
def create_schema():
    print("Attempting to connect to Azure and create the tables...")
    Base.metadata.create_all(engine)
    print("The Schema has been created successfully in Azure")

if __name__ == "__main__":
    create_schema()