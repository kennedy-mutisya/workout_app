from app import app
from models import db

with app.app_context():
    # Seed data will be added in Step 6.
    print("Database seeding setup is ready.")
