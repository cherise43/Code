from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from faker import Faker
from models import Customer, Restaurant, Reviews, Base, Restaurant_Customer
import random

# Create an engine to connect to the SQLite database
engine = create_engine('sqlite:///trial.db')

# Create a session factory bound to the engine
Session = sessionmaker(bind=engine)

# Create a session
session = Session()

# Initialize the Faker library for generating fake data
fake = Faker()

# Clear existing data (optional)
# You can uncomment these lines if you want to clear existing data before seeding.
# session.query(Customer).delete()
# session.query(Restaurant).delete()
# session.query(Reviews).delete()
# session.query(Restaurant_Customer).delete()

# Commit the changes (optional)
# If you uncommented the delete lines above, you can commit the changes here.
# session.commit()

def seed_data():
    # Seed Customers
    print("Seeding Customers...")
    customers = []
    for _ in range(10):
        customer = Customer(
            first_name=fake.first_name(),
            last_name=fake.last_name()
        )
        customers.append(customer)
        session.add(customer)
    session.commit()
    print("Customers Seeded")

    # Seed Restaurants
    print("Seeding Restaurants...")
    restaurants = []
    for _ in range(5):
        restaurant = Restaurant(
            name=fake.company(),
            price=random.choice(['$'])
        )
        restaurants.append(restaurant)
        session.add(restaurant)
    session.commit()
    print("Restaurants Seeded")

    # Seed Reviews
    print("Seeding Reviews...")
    for customer in customers:
        for _ in range(3):
            restaurant = random.choice(restaurants)
            review = Reviews(
                star_rating=random.randint(1, 5),
                Customer_id=customer.id,
                Resturant_id=restaurant.id
            )
            session.add(review)
    session.commit()
    print("Reviews Seeded")

    # Seed Restaurant_Customer association (many-to-many)
    print("Seeding Restaurant_Customer association...")
    for restaurant in restaurants:
        for customer in random.sample(customers, random.randint(1, 5)):
            association = Restaurant_Customer.insert().values(
                customer_id=customer.id,
                restaurant_id=restaurant.id
            )
            session.execute(association)
    session.commit()
    print("Restaurant_Customer association Seeded")

if __name__ == '__main__':
    # Create database tables if they don't exist
    Base.metadata.create_all(engine)

    # Seed the data
    seed_data()

    # Close the session
    session.close()
