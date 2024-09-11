from data_fetching.world_bank_call import WorldBankEconomicsAPI
from data_fetching.imf_call import IMFEconomicsAPI
from database.models import EconomicData, IMFData 
from database import db
from app import app
from datetime import datetime
from config import COUNTRY_CODES, TESTING_COUNTRY_CODES

def save_economic_data_for_country(country_code):
    """
    Fetches and saves economic data for a given country code to the database (previously available 20 years).
    
    Parameters:
    country_code (str): The ISO 3166-1 alpha-3 country code (e.g., "USA").
    """

    current_year = int(datetime.now().year)
    previous_year = current_year - 1
    twenty_years_ago = current_year - 21

    # init world bank
    wb_economics = WorldBankEconomicsAPI()
    economic_data = wb_economics.get_economic_data(country_code, start_year=twenty_years_ago, end_year=previous_year)

    # init imf
    imf_economics = IMFEconomicsAPI()
    imf_data = imf_economics.run(country_code=country_code, start_year=twenty_years_ago, end_year=previous_year)

    # Print the combined DataFrame to inspect the data
    print(f"Saving data for {country_code}...")

    # Store the DataFrame in SQLite using SQLAlchemy
    with app.app_context():
        for index, row in economic_data.iterrows():
            # Remove "YR" prefix from year
            year = int(index.replace('YR', ''))

            # Create an instance of the EconomicData model for each row
            economic_record = EconomicData(
                country_code=country_code,
                year=year,  # Use the modified year without the "YR" prefix
                capital_city=row.get('capital_city'),
                latitude=row.get('latitude'),
                longitude=row.get('longitude'),
                gdp_current_usd=row.get('GDP (current US$)'),
                gdp_per_capita_current_usd=row.get('GDP Per Capita (current US$)'),
                gdp_growth_annual_percent=row.get('GDP Growth (annual %)'),
                gni_current_usd=row.get('GNI (current US$)'),
                gni_per_capita_current_usd=row.get('GNI Per Capita (current US$)'),
                gni_growth_percent=row.get("GNI growth (annual %)"),
                inflation_consumer_prices_annual_percent=row.get('Inflation (consumer prices, annual %)'),
                inflation_gdp_deflator_annual_percent=row.get('Inflation (GDP deflator, annual %)'),
                exports_gdp_percent=row.get('Exports of Goods and Services (% of GDP)'),
                imports_gdp_percent=row.get('Imports of Goods and Services (% of GDP)'),
                current_account_balance_gdp_percent=row.get('Current Account Balance (% of GDP)'),
                revenue_gdp_percent=row.get('Revenue (excluding grants, % of GDP)'),
                government_expenditure_gdp_percent=row.get('Government Expenditure (% of GDP)'),
                gini_index=row.get('Gini Index (0-100)'),
                unemployment=row.get('Unemployment (% of labor force)'),
                lowest_ten_percent=row.get('Income share held by lowest 10%'),
                highest_ten_percent=row.get('Income share held by highest 10%')
            )
            db.session.add(economic_record)

        for index, row in imf_data.iterrows():
            imf_record = IMFData(
                country_code=country_code,
                year=row.get('year'),
                unemployment_rate=row.get('unemployment_rate'),
                gdp_current_usd=row.get('gdp_current_prices'), 
                gdp_per_capita_usd=row.get('gdp_per_capita_current_prices'),
                gdp_growth_percent=row.get('gdp_constant_prices_change'),
                inflation_avg_consumer_prices=row.get('inflation_avg_consumer_prices'),
                inflation_end_consumer_prices=row.get('inflation_end_consumer_prices'), 
                exports_gdp_percent=row.get('exports_gdp_percent'),
                imports_gdp_percent=row.get('imports_gdp_percent'),
                population_total=row.get('population_millions'),
            )
            db.session.add(imf_record)
        
        db.session.commit()  # Commit after each country's data is added

    

if __name__ == "__main__":
    # List of country codes to process, including India, Russia, Mexico, and Brazil
    TESTING = True

    country_codes = None
    if (TESTING):
        country_codes = TESTING_COUNTRY_CODES.keys()
    else: 
        country_codes = COUNTRY_CODES.keys()  # Added new country codes

    # Process each country code
    for country_code in country_codes:
        save_economic_data_for_country(country_code)