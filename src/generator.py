import os
import random
import time
import urllib.parse
from datetime import datetime, timedelta
from dotenv import load_dotenv
from sqlalchemy import create_engine, insert

# --- FAKER & COMMERCE PROVIDER ---
from faker import Faker
import faker_commerce 

# Importing correctly from your database.py
from database import (
    engine, user_table, product_table, category_table, 
    seller_table, online_order_table, store_order_table, sales_targets_table
)

load_dotenv()

# Initialize Faker and add the commerce provider
fake = Faker()
fake.add_provider(faker_commerce.Provider)

# --- LISTS FOR INCONSISTENCIES ---
countries_dirty = {
    "USA": ["USA", "United States", "usa", "us", "U.S.A."],
    "UK": ["UK", "United Kingdom", "uk", "u.k.", "Great Britain"],
    "Greece": ["Greece", "Ελλάδα", "GR", "greece"]
}

def get_dirty_country(country_key):
    return random.choice(countries_dirty[country_key])

def get_dirty_amount():
    base_amount = round(random.uniform(10.0, 500.0), 2)
    chance = random.random()
    if chance < 0.2: return f"${base_amount}"
    if chance < 0.4: return f"{base_amount}€"
    if chance < 0.1: return None # NULL value
    return str(base_amount)

# --- DATA GENERATION FUNCTIONS ---

def generate_static_data():
    print("📦 Generating Categories, Products, Sellers, and Targets...")
    with engine.begin() as conn:
        # Categories (Using faker-commerce)
        categories = [{"category_id": i, "category_name": fake.ecommerce_category()} for i in range(1, 6)]
        conn.execute(insert(category_table), categories)

        # Products (Using faker-commerce)
        products = [{"product_id": i, "product_name": fake.ecommerce_name(), "category_id": random.randint(1, 5), "price": str(round(random.uniform(5, 100), 2))} for i in range(1, 11)]
        conn.execute(insert(product_table), products)

        # Sellers
        sellers = [{
            "seller_id": i, 
            "seller_name": fake.name(),
            "age": random.randint(22, 65),
            "gender": random.choice(["Male", "Female", "Other"]),
            "hire_date": fake.date_time_between(start_date='-5y', end_date='now')
        } for i in range(1, 6)]
        conn.execute(insert(seller_table), sellers)

        # Targets
        targets = []
        for country in ["USA", "UK", "Greece"]:
            targets.append({
                "target_month": datetime.now().strftime("%Y-%m"),
                "country": country,
                "target_amount": str(random.randint(10000, 50000))
            })
        conn.execute(insert(sales_targets_table), targets)

def generate_historical_data(num_records=100):
    print(f"⏳ Generating {num_records} historical records from 2025...")
    for i in range(num_records):
        random_date = fake.date_time_between(start_date='-450d', end_date='-95d')
        user_id = random.randint(10000, 99999)
        
        user_data = {
            "user_id": user_id,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.email() if random.random() > 0.1 else None,
            "city": fake.city(),
            "age": random.randint(18, 80),
            "gender": random.choice(["Male", "Female", "Other"]),
            "registration_date": random_date - timedelta(days=random.randint(10, 100))
        }

        with engine.begin() as conn:
            conn.execute(insert(user_table), user_data)
            
            if random.random() > 0.5:
                conn.execute(insert(online_order_table), {
                    "order_id": random.randint(100000, 999999),
                    "session_id": f"sess_{fake.uuid4()[:8]}",
                    "user_id": user_id,
                    "product_id": random.randint(1, 10),
                    "order_date": random_date,
                    "amount": get_dirty_amount(),
                    "shipping_provider": fake.company(),
                    "shipping_country": get_dirty_country(random.choice(["USA", "UK", "Greece"])),
                    "internal_notes": "Historical Online Sale"
                })
            else:
                conn.execute(insert(store_order_table), {
                    "order_id": random.randint(100000, 999999),
                    "user_id": user_id,
                    "product_id": random.randint(1, 10),
                    "seller_id": random.randint(1, 5),
                    "order_date": random_date,
                    "amount": get_dirty_amount(),
                    "store_country": get_dirty_country(random.choice(["USA", "UK", "Greece"])),
                    "internal_notes": "Historical Store Sale"
                })

def generate_dynamic_data():
    print("🚀 Starting continuous real-time flow...")
    order_id_counter = 1000
    try:
        while True:
            user_id = random.randint(1000, 9999)
            user_data = {
                "user_id": user_id,
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "email": fake.email() if random.random() > 0.1 else None,
                "city": fake.city(),
                "age": random.randint(18, 80),
                "gender": random.choice(["Male", "Female", "Other"]),
                "registration_date": datetime.now()
            }

            with engine.begin() as conn:
                conn.execute(insert(user_table), user_data)
                
                if random.random() > 0.5:
                    conn.execute(insert(online_order_table), {
                        "order_id": order_id_counter,
                        "session_id": f"sess_{fake.uuid4()[:8]}",
                        "user_id": user_id,
                        "product_id": random.randint(1, 10),
                        "order_date": datetime.now(),
                        "amount": get_dirty_amount(),
                        "shipping_provider": fake.company(),
                        "shipping_country": get_dirty_country(random.choice(["USA", "UK", "Greece"]))
                    })
                    print(f"🛒 Online Order #{order_id_counter} created.")
                else:
                    conn.execute(insert(store_order_table), {
                        "order_id": order_id_counter,
                        "user_id": user_id,
                        "product_id": random.randint(1, 10),
                        "seller_id": random.randint(1, 5),
                        "order_date": datetime.now(),
                        "amount": get_dirty_amount(),
                        "store_country": get_dirty_country(random.choice(["USA", "UK", "Greece"]))
                    })
                    print(f"🏬 Store Order #{order_id_counter} created.")

            order_id_counter += 1
            time.sleep(random.randint(2, 5))
    except KeyboardInterrupt:
        print("\n🛑 Generator stopped.")

if __name__ == "__main__":
    generate_static_data()
    generate_historical_data(50) 
    generate_dynamic_data()