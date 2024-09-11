from flask import Flask, render_template, request
import database
from config import COUNTRY_CODES, TESTING_COUNTRY_CODES, GLOBAL_TESTING, CURRENT_YEAR
import database.models
from database.all_rankings import all_rankings
import pycountry

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
database.db.init_app(app)

print("*** Testing Dataset: ", GLOBAL_TESTING, " ***")

# Maintenance Mode Support
maintenance_mode = False

def check_maintenance_mode(func):
    def wrapper(*args, **kwargs):
        if maintenance_mode:
            return render_template('maintenance.html')
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__  # Preserve the original function name
    return wrapper

@app.route('/')
@check_maintenance_mode
def index():
    gdp_query = database.models.EconomicData.query.filter_by(year=CURRENT_YEAR).order_by(database.models.EconomicData.gdp_current_usd.desc()).all()
    inflation_query = (database.models.IMFData.query
    .filter_by(year=CURRENT_YEAR)
    .order_by(
        database.models.IMFData.inflation_avg_consumer_prices.asc(),
        database.models.IMFData.country_code.asc()
    )
    .all()) 

    country_codes = COUNTRY_CODES
    if (GLOBAL_TESTING):
        country_codes = TESTING_COUNTRY_CODES

    return render_template('index.html', gdp_query=gdp_query, inflation_query=inflation_query, country_codes=country_codes)

@app.route('/country/<country_code>')
@check_maintenance_mode
def country(country_code):
    # Determine which dictionary to use based on GLOBAL_TESTING
    if GLOBAL_TESTING:
        c = TESTING_COUNTRY_CODES.get(country_code)
    else:
        c = COUNTRY_CODES.get(country_code)

    # Query the data for the specific country
    wb_data = database.models.EconomicData.query.filter_by(country_code=country_code).order_by(database.models.EconomicData.year.asc()).all()
    imf_data = database.models.IMFData.query.filter_by(country_code=country_code).order_by(database.models.IMFData.year.asc()).all()

    # Calculate Ranks
    ranks = all_rankings(country_code)

    # Render the template with the required data
    return render_template('country.html', country_code=country_code, country_name=c, wb_data=wb_data, imf_data=imf_data, gdp_ranks=ranks.get('gdp_ranks'), inflation_ranks=ranks.get('inflation_ranks'), gni_ranks=ranks.get('gni_ranks'))

# Template Functions:
@app.template_filter('round_even')
def round_even(value):
    return round(value / 2) * 2

@app.template_filter('round_even_format')
def round_even_format(value):
    return f"{round(value / 2) * 2:,}"

@app.template_filter('convert_alpha3_to_alpha2')
def convert_alpha3_to_alpha2(value):
    country = pycountry.countries.get(alpha_3=value)
    return country.alpha_2 if country else None

@app.template_filter('most_recent_non_null_with_year')
def most_recent_non_null_with_year(data, attribute):
    for item in reversed(data):
        value = getattr(item, attribute, None)
        if value is not None:
            return (value, getattr(item, 'year', 'Unknown'))
    return (None, 'Unknown') 

@app.context_processor
def inject_country_codes():
    return dict(country_codes=COUNTRY_CODES, version="Beta 0.0.1")

if __name__ == "__main__":
    app.run(debug=True, port=8000)