from data_fetching.world_bank_call import WorldBankEconomicsAPI
from database.models import EconomicData
from database import db
from app import app
from datetime import datetime
from config import COUNTRY_CODES

def update_economic_data_for_previous_year(country_code):
    """
    Fetches and updates economic data for the previous year for a given country code.
    
    Parameters:
    country_code (str): The ISO 3166-1 alpha-3 country code (e.g., "USA").
    """
    current_year = int(datetime.now().year)
    previous_year = current_year

    wb_economics = WorldBankEconomicsAPI()
    economic_data = wb_economics.get_economic_data(country_code, start_year=previous_year-1, end_year=previous_year)

    # Print the combined DataFrame to inspect the data
    print(f"Updating data for {country_code} for the year {previous_year}...")
    print(economic_data)

    # Store the DataFrame in SQLite using SQLAlchemy
    with app.app_context():
        for index, row in economic_data.iterrows():
            # Remove "YR" prefix from year
            year = int(index.replace('YR', ''))

            # Check if the record already exists
            existing_record = EconomicData.query.filter_by(country_code=country_code, year=year).first()

            if existing_record:
                # Update the existing record
                existing_record.gdp_current_usd = row.get('GDP (current US$)')
                existing_record.gdp_per_capita_current_usd = row.get('GDP Per Capita (current US$)')
                existing_record.gdp_growth_annual_percent = row.get('GDP Growth (annual %)')
                existing_record.gni_current_usd = row.get('GNI (current US$)')
                existing_record.gni_per_capita_current_usd = row.get('GNI Per Capita (current US$)')
                existing_record.inflation_consumer_prices_annual_percent = row.get('Inflation (consumer prices, annual %)')
                existing_record.inflation_gdp_deflator_annual_percent = row.get('Inflation (GDP deflator, annual %)')
                existing_record.exports_gdp_percent = row.get('Exports of Goods and Services (% of GDP)')
                existing_record.imports_gdp_percent = row.get('Imports of Goods and Services (% of GDP)')
                existing_record.current_account_balance_gdp_percent = row.get('Current Account Balance (% of GDP)')
                existing_record.revenue_gdp_percent = row.get('Revenue (excluding grants, % of GDP)')
                existing_record.government_expenditure_gdp_percent = row.get('Government Expenditure (% of GDP)')
                existing_record.total_external_debt_stocks_usd = row.get('Total External Debt Stocks (current US$)')
                existing_record.total_debt_service_gni_percent = row.get('Total Debt Service (% of GNI)')
            else:
                # Create a new record if it doesn't exist
                economic_record = EconomicData(
                    country_code=country_code,
                    year=year,  # Use the modified year without the "YR" prefix
                    gdp_current_usd=row.get('GDP (current US$)'),
                    gdp_per_capita_current_usd=row.get('GDP Per Capita (current US$)'),
                    gdp_growth_annual_percent=row.get('GDP Growth (annual %)'),
                    gni_current_usd=row.get('GNI (current US$)'),
                    gni_per_capita_current_usd=row.get('GNI Per Capita (current US$)'),
                    inflation_consumer_prices_annual_percent=row.get('Inflation (consumer prices, annual %)'),
                    inflation_gdp_deflator_annual_percent=row.get('Inflation (GDP deflator, annual %)'),
                    exports_gdp_percent=row.get('Exports of Goods and Services (% of GDP)'),
                    imports_gdp_percent=row.get('Imports of Goods and Services (% of GDP)'),
                    current_account_balance_gdp_percent=row.get('Current Account Balance (% of GDP)'),
                    revenue_gdp_percent=row.get('Revenue (excluding grants, % of GDP)'),
                    government_expenditure_gdp_percent=row.get('Government Expenditure (% of GDP)'),
                    total_external_debt_stocks_usd=row.get('Total External Debt Stocks (current US$)'),
                    total_debt_service_gni_percent=row.get('Total Debt Service (% of GNI)')
                )
                db.session.add(economic_record)

        db.session.commit()  # Commit after each country's data is added or updated

if __name__ == "__main__":
    # List of country codes to process, including India, Russia, Mexico, and Brazil
    country_codes = COUNTRY_CODES.keys() # Added new country codes

    # Run this yearly to update data for the previous year
    for country_code in country_codes:
        update_economic_data_for_previous_year(country_code)
