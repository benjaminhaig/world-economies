import requests
from ..config.config import COUNTRY_CODES  # Import the list of country codes

# Define the World Bank API endpoint and parameters for GDP data
base_url = "https://api.worldbank.org/v2/country/{country_code}/indicator/NY.GDP.MKTP.CD"
params = {
    'format': 'json',  # Response format
    'date': '2023',    # Year to check for GDP data
    'per_page': 1      # Only need one result per request
}

# List to store countries missing GDP data for 2023
missing_gdp_countries = []

# Loop through each country code and check for GDP data
for country_code in COUNTRY_CODES:
    # Construct the API URL for the specific country
    url = base_url.format(country_code=country_code)
    
    # Make the API request
    response = requests.get(url, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Check if the data contains valid GDP information
        if data and isinstance(data, list) and len(data) > 1:
            gdp_data = data[1]
            
            # Check if GDP for 2023 is missing or not specified
            if not gdp_data or not gdp_data[0]['value']:
                missing_gdp_countries.append(country_code)
        else:
            # If no valid data is returned, add the country to the list
            missing_gdp_countries.append(country_code)
    else:
        print(f"Failed to retrieve data for {country_code}. HTTP Status code: {response.status_code}")

# Print the list of countries missing GDP data for 2023
print("Countries missing GDP data for 2023:")
print(missing_gdp_countries)