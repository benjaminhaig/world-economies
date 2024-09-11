import wbgapi as wb
import pandas as pd
from app import app
from database import db

class WorldBankEconomicsAPI:
    def __init__(self):
        # Dictionary of economic indicators with meaningful names
        self.indicators = {
            "NY.GDP.MKTP.CD": "GDP (current US$)",
            "NY.GDP.PCAP.CD": "GDP Per Capita (current US$)",
            "NY.GDP.MKTP.KD.ZG": "GDP Growth (annual %)",
            "NY.GNP.MKTP.CD": "GNI (current US$)",
            "NY.GNP.PCAP.CD": "GNI Per Capita (current US$)",
            "NY.GNP.MKTP.KD.ZG": "GNI growth (annual %)",
            "FP.CPI.TOTL.ZG": "Inflation (consumer prices, annual %)",
            "NY.GDP.DEFL.KD.ZG": "Inflation (GDP deflator, annual %)",
            "NE.EXP.GNFS.ZS": "Exports of Goods and Services (% of GDP)",
            "NE.IMP.GNFS.ZS": "Imports of Goods and Services (% of GDP)",
            "GC.REV.XGRT.GD.ZS": "Revenue (excluding grants, % of GDP)",
            "GC.XPN.TOTL.GD.ZS": "Government Expenditure (% of GDP)",
            "SI.POV.GINI": 'Gini Index (0-100)',
            "SL.UEM.TOTL.ZS": 'Unemployment (% of labor force)',
            "SI.DST.FRST.10": 'Income share held by lowest 10%',
            "SI.DST.10TH.10": 'Income share held by highest 10%'
        }

    def get_country_metadata(self, country_code):
        """
        Fetches metadata for a given country, including capital city, latitude, longitude, and income level.
        
        Parameters:
        country_code (str): The ISO 3166-1 alpha-3 country code (e.g., "CAN" for Canada).
        
        Returns:
        dict: A dictionary containing the metadata.
        """
        metadata = wb.economy.get(country_code)
        return {
            'capital_city': metadata['capitalCity'],
            'latitude': metadata['latitude'],
            'longitude': metadata['longitude'],

        }

    def get_economic_data(self, country_code, start_year=2000, end_year=2021):
        """
        Retrieves economic data for the given country code and combines it into a single DataFrame.

        Parameters:
        country_code (str): The ISO 3166-1 alpha-3 country code (e.g., "CAN" for Canada).
        start_year (int): The start year for the data range.
        end_year (int): The end year for the data range.

        Returns:
        pd.DataFrame: A DataFrame where each column represents an economic indicator.
        """
        frames = []
        for indicator, name in self.indicators.items():
            # Fetch data for the indicator
            indicator_data = wb.data.DataFrame(indicator, country_code, time=range(start_year, end_year+1))

            # Check if the DataFrame has data
            if not indicator_data.empty:
                # Select the row corresponding to the country and rename the Series
                series = indicator_data.loc[country_code]
                series.name = name
                frames.append(series)
            else:
                print(f"No data found for {name}. Skipping this indicator.")

        if frames:
            # Combine all the series into a single DataFrame
            combined_data = pd.concat(frames, axis=1)

            # Fetch and add country metadata
            metadata = self.get_country_metadata(country_code)
            combined_data['capital_city'] = metadata['capital_city']
            combined_data['latitude'] = metadata['latitude']
            combined_data['longitude'] = metadata['longitude']

            return combined_data
        else:
            print("No valid data to concatenate.")
            return pd.DataFrame()  # Return an empty DataFrame

