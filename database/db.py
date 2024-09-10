from app import app
from flask_sqlalchemy import SQLAlchemy
from config import COUNTRY_CODES, TESTING_COUNTRY_CODES, GLOBAL_TESTING
from database import db


def save_data_using_setup():
    from .initial_setup import save_economic_data_for_country

    country_codes = None
    if (GLOBAL_TESTING):
        country_codes = TESTING_COUNTRY_CODES.keys()
    else: 
        country_codes = COUNTRY_CODES.keys()

    for i in country_codes:
        save_economic_data_for_country(i)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        save_data_using_setup()
    
