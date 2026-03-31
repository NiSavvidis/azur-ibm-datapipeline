import os
import urllib
import time
import random
from datetime import datetime, timezone
from dotenv import load_dotenv
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import the database models from database.py
from database import Category, Product, User, Seller, Order

load_dotenv()

# 1. Connect to Azure (Exactly as in database.py)
params = urllib.parse.quote_plus(
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={os.getenv('DB_HOST')};"
    f"DATABASE={os.getenv('DB_NAME')};"
    f"UID={os.getenv('DB_USER')};"
    f"PWD={os.getenv('DB_PASSWORD')};"
    f"Encrypt=yes;"
    f"TrustServerCertificate=no;"
    f"Connection Timeout=30;"
)
connection_string = f"mssql+pyodbc:///?odbc_connect={params}"
engine = create_engine(connection_string)

# Create a Session for making queries and transactions
Session = sessionmaker(bind=engine)
session = Session()

fake = Faker()

# 2. SEEDING FUNCTION (Populating initial data)
def seed_database():
    print("Checking for initial data...")
    
    # If users already exist, we don't add them again
    if session.query(User).count() > 0:
        print("The database already has data. Proceeding to simulation.")
        return

    print("The database is empty! Starting the seeding process...")
    
    # Initial Categories
    categories = [Category(name="Electronics"), Category(name="Clothing"), Category(name="Books")]
    session.add_all(categories)
    session.flush() # flush() for them to get IDs without closing the session
    
    # Initial Products
    products = [
        Product(name="Laptop", price=1200.50, category_id=categories[0].id),
        Product(name="Smartphone", price=800.00, category_id=categories[0].id),
        Product(name="T-Shirt", price=25.00, category_id=categories[1].id),
        Product(name="Jeans", price=50.00, category_id=categories[1].id),
        Product(name="Python Book", price=45.00, category_id=categories[2].id)
    ]
    session.add_all(products)
    
    # Initial Users (Customers)
    for _ in range(10):
        user = User(username=fake.user_name(), email=fake.email())
        session.add(user)
        
    # Initial Sellers
    for _ in range(3):
        seller = Seller(full_name=fake.name(), email=fake.email())
        session.add(seller)
        
    session.commit()
    print("The seeding completed successfully!")

# 3. SIMULATION FUNCTION (Generating Orders)
def simulate_orders():
    print("Starting the orders simulation... (Press Ctrl+C to stop)")
    
    # We fetch all IDs from the database to randomly select from them
    user_ids = [u.id for u in session.query(User.id).all()]
    seller_ids = [s.id for s in session.query(Seller.id).all()]
    products = session.query(Product).all()
    
    while True:
        try:
            # Choose random items for the order
            random_user = random.choice(user_ids)
            random_seller = random.choice(seller_ids)
            random_product = random.choice(products)
            qty = random.randint(1, 5)
            
            # Create the order (Table 5: Order)
            new_order = Order(
                user_id=random_user,
                seller_id=random_seller,
                product_id=random_product.id,
                quantity=qty,
                price_at_purchase=random_product.price, # We keep the price at the time of purchase
                status=random.choice(['pending', 'completed', 'shipped']),
                order_date=datetime.now(timezone.utc)
            )
            
            session.add(new_order)
            session.commit()
            
            print(f"[{datetime.now().strftime('%H:%M:%S')}] New order: Product ID {random_product.id} x {qty} | User ID: {random_user}")
            
        except Exception as e:
            print(f"Error: {e}")
            session.rollback()
            
        # Wait 10 seconds before the next order (I made it 10 instead of 2 minutes so you can see results quickly!)
        time.sleep(10)

if __name__ == "__main__":
    seed_database()
    simulate_orders()