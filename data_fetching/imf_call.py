import aiohttp
import asyncio
import pandas as pd

class IMFEconomicsAPI:
    def __init__(self):
        self.base_url = "https://www.imf.org/external/datamapper/api/v1"
        self.indicators = {
            "LUR": "unemployment_rate",
            "NGDPD": "gdp_current_prices",
            "NGDPDPC": "gdp_per_capita_current_prices",
            "NGDP_RPCH": "gdp_constant_prices_change",
            "PCPIPCH": "inflation_avg_consumer_prices",
            "PCPIEPCH": "inflation_end_consumer_prices",
            "BX_GDP": "exports_gdp_percent",
            "BM_GDP": "imports_gdp_percent",
            "LP": "population_millions"
        }
        self.conversion_factors = {
            "NGDPD": 1_000_000_000,  # GDP in billions of dollars
            "NGDPDPC": 1,  # GDP per capita in USD
            "LP": 1_000_000,  # Population in millions of people
        }

    async def fetch_data(self, session, indicator, country_code, periods):
        url = f"{self.base_url}/data/{indicator}/{country_code}?periods={periods}"
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                # Extract data correctly from the nested JSON response
                indicator_data = data.get('values', {}).get(indicator, {}).get(country_code, {})
                print(f"Fetched data for {indicator}: {indicator_data}")  # Debugging output
                
                # Apply conversion if necessary
                if indicator in self.conversion_factors:
                    factor = self.conversion_factors[indicator]
                    indicator_data = {year: value * factor for year, value in indicator_data.items()}

                return indicator_data, indicator
            else:
                print(f"Failed to fetch data for {indicator}: HTTP {response.status}")
                return {}, indicator

    async def get_economic_data(self, country_code, start_year, end_year):
        # Create a comma-separated list of periods (years)
        periods = ','.join(str(year) for year in range(start_year, end_year + 1))

        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            tasks = [
                self.fetch_data(session, indicator, country_code, periods)
                for indicator in self.indicators
            ]
            responses = await asyncio.gather(*tasks)

            # Process responses
            all_data = []
            for data, indicator in responses:
                if data:
                    # Convert to DataFrame
                    indicator_name = self.indicators[indicator]
                    df = pd.DataFrame.from_dict(data, orient='index', columns=[indicator_name])
                    df.index.name = 'year'
                    all_data.append(df)

            if all_data:
                combined_data = pd.concat(all_data, axis=1)
                # Add country code column and reorder columns
                combined_data.insert(0, 'country_code', country_code)
                combined_data.reset_index(inplace=True)
                return combined_data
            else:
                print(f"No data found for {country_code}.")
                return pd.DataFrame()

    def run(self, country_code, start_year, end_year):
        return asyncio.run(self.get_economic_data(country_code, start_year, end_year))


# Example usage
if __name__ == "__main__":
    imf_api = IMFEconomicsAPI()
    country_code = "AFG"
    start_year = 2000
    end_year = 2023
    
    # Run the asyncio loop
    val = imf_api.run(country_code, start_year, end_year)
    val.to_csv('economic_data.csv')
    