import os #for environment variables 
import urllib.parse #for encoding the connection string and ensuring special characters are handled correctly
from sqlalchemy import create_engine, Column, Integer, String, DateTime, MetaData, Table #for defining the database schema and managing metadata and creating the engine to connect to the database
from dotenv import load_dotenv #for loading environment variables from a .env file, which is a common practice for managing sensitive information like database credentials without hardcoding them in the source code

# Loading the settings from the .env file
load_dotenv()

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")

# SAFE CONNECTION STRING WITH ENCRYPTION AND TRUSTED CERTIFICATE
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

engine = create_engine(connection_string)
metadata = MetaData()

# --- DEFINITION OF TABLES ---

user_table = Table(
    'user', metadata,
    Column('user_id', Integer),
    Column('first_name', String(100)),
    Column('last_name', String(100)),
    Column('email', String(150)),
    Column('city', String(100)),
    Column('age', Integer),               
    Column('gender', String(20)),         
    Column('registration_date', DateTime) 
)

product_table = Table(
    'product', metadata,
    Column('product_id', Integer),
    Column('product_name', String(150)),
    Column('category_id', Integer),
    Column('price', String(50)) 
)

category_table = Table(
    'category', metadata,
    Column('category_id', Integer),
    Column('category_name', String(100))
)

seller_table = Table(
    'seller', metadata,
    Column('seller_id', Integer),
    Column('seller_name', String(100)),
    Column('age', Integer),               
    Column('gender', String(20)),         
    Column('hire_date', DateTime)         
)

online_order_table = Table(
    'online_orders', metadata,
    Column('order_id', Integer),
    Column('session_id', String(100)),
    Column('user_id', Integer),
    Column('product_id', Integer),
    Column('order_date', DateTime),
    Column('amount', String(50)),               
    Column('shipping_provider', String(150)),    
    Column('shipping_country', String(100)),     
    Column('internal_notes', String(500))
)

store_order_table = Table(
    'store_orders', metadata,
    Column('order_id', Integer),
    Column('user_id', Integer),
    Column('product_id', Integer),
    Column('seller_id', Integer),               
    Column('order_date', DateTime),
    Column('amount', String(50)),               
    Column('store_country', String(100)),        
    Column('internal_notes', String(500))
)

sales_targets_table = Table(
    'sales_targets', metadata,
    Column('target_month', String(20)),          
    Column('country', String(100)),             
    Column('target_amount', String(50))         
)

def create_tables():
    print("⏳ Creating the tables in Azure SQL...")
    metadata.create_all(engine)
    print("✅ The database is ready with all the demographic elements!")

if __name__ == "__main__":
    create_tables()