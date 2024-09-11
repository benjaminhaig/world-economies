from database import db

class EconomicData(db.Model):
    __tablename__ = 'world_bank_data'
    
    id = db.Column(db.Integer, primary_key=True)
    country_code = db.Column(db.String(3), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    capital_city = db.Column(db.String(50))
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    gdp_current_usd = db.Column(db.Float)  # GDP (current US$)
    gdp_per_capita_current_usd = db.Column(db.Float)  # GDP Per Capita (current US$)
    gdp_growth_annual_percent = db.Column(db.Float)  # GDP Growth (annual %)
    gni_current_usd = db.Column(db.Float)  # GNI (current US$)
    gni_per_capita_current_usd = db.Column(db.Float)  # GNI Per Capita (current US$)
    gni_growth_percent = db.Column(db.Float) # GNI growth (annual %)
    inflation_consumer_prices_annual_percent = db.Column(db.Float)  # Inflation (consumer prices, annual %)
    inflation_gdp_deflator_annual_percent = db.Column(db.Float)  # Inflation (GDP deflator, annual %)
    exports_gdp_percent = db.Column(db.Float)  # Exports of Goods and Services (% of GDP)
    imports_gdp_percent = db.Column(db.Float)  # Imports of Goods and Services (% of GDP)
    current_account_balance_gdp_percent = db.Column(db.Float)  # Current Account Balance (% of GDP)
    revenue_gdp_percent = db.Column(db.Float)  # Revenue (excluding grants, % of GDP)
    government_expenditure_gdp_percent = db.Column(db.Float)  # Government Expenditure (% of GDP)
    gini_index=db.Column(db.Float) # Gini Index (0-100)
    unemployment=db.Column(db.Float) # Unemployment (% of labor force)
    lowest_ten_percent=db.Column(db.Float) # Income share held by lowest 10%
    highest_ten_percent=db.Column(db.Float) # Income share held by highest 10%



class IMFData(db.Model):
    __tablename__ = 'imf_data'

    id = db.Column(db.Integer, primary_key=True)
    country_code = db.Column(db.String(3), nullable=False)
    year = db.Column(db.Integer, nullable=False)

    unemployment_rate = db.Column(db.Float)  # LUR: Unemployment Rate
    gdp_current_usd = db.Column(db.Float)  # NGDPD: GDP, current prices (billions of dollars)
    gdp_per_capita_usd = db.Column(db.Float)  # NGDPDPC: GDP per capita, current prices (US Dollars)
    gdp_growth_percent = db.Column(db.Float)  # NGDP_RPCH: GDP, constant prices (% change annually)
    inflation_avg_consumer_prices = db.Column(db.Float)  # PCPIPCH: Inflation, average consumer prices
    inflation_end_consumer_prices = db.Column(db.Float) # PCPIEPCH: Inflation, end of period consumer prices
    exports_gdp_percent = db.Column(db.Float)  # BX_GDP: Exports of goods and services (% of GDP)
    imports_gdp_percent = db.Column(db.Float)  # BM_GDP: Imports of goods and services (% of GDP)
    population_total = db.Column(db.Float)  # LP: Population (millions of people)