from datetime import datetime
from .get_rankings import get_rankings
from .models import EconomicData, IMFData


def all_rankings(country_code):
    current_year = int(datetime.now().year) - 1

    # GDP Ranking (USD)
    gdp_rank_query = EconomicData.query.filter_by(year=current_year).order_by(EconomicData.gdp_current_usd.desc()).all()
    gdp_rank = get_rankings(gdp_rank_query, country_code)

    # GDP Per Capita Ranking (USD)
    gdp_per_capita_rank_query = EconomicData.query.filter_by(year=current_year).order_by(EconomicData.gdp_per_capita_current_usd.desc()).all()
    gdp_per_capita_rank = get_rankings(gdp_per_capita_rank_query, country_code)

    # GDP Annual Growth Average (%)
    gdp_annual_growth_rank_query = EconomicData.query.filter_by(year=current_year).order_by(EconomicData.gdp_growth_annual_percent.desc()).all()
    gdp_annual_growth_rank = get_rankings(gdp_annual_growth_rank_query, country_code)
    
    # Make dictionary of GDP ranks
    gdp_ranks = {
        'gdp_rank': gdp_rank,
        'gdp_per_capita_rank': gdp_per_capita_rank,
        'gdp_annual_growth_rank': gdp_annual_growth_rank
    }

    # Inflation Ranks
    inflation_average_query = IMFData.query.filter_by(year=current_year).order_by(IMFData.inflation_avg_consumer_prices.desc()).all()
    inflation_average_rank = get_rankings(inflation_average_query, country_code, inverse=True)

    inflation_end_query = IMFData.query.filter_by(year=current_year).order_by(IMFData.inflation_end_consumer_prices.desc()).all()
    inflation_end_rank = get_rankings(inflation_end_query, country_code, inverse=True)

    inflation_deflator_query = EconomicData.query.filter_by(year=current_year).order_by(EconomicData.inflation_gdp_deflator_annual_percent.desc()).all()
    inflation_deflator_rank = get_rankings(inflation_deflator_query, country_code, inverse=True)

    inflation_ranks = {
        'inflation_avg_rank': inflation_average_rank,
        'inflation_end_rank': inflation_end_rank,
        'inflation_deflator_rank': inflation_deflator_rank
    }

    # GNI Ranks
    gni_usd_query = EconomicData.query.filter_by(year=current_year).order_by(EconomicData.gni_current_usd.desc()).all()
    gni_usd_rank = get_rankings(gni_usd_query, country_code=country_code)

    gni_per_capita_query = EconomicData.query.filter_by(year=current_year).order_by(EconomicData.gni_per_capita_current_usd.desc()).all()
    gni_per_capita_rank = get_rankings(gni_per_capita_query, country_code=country_code)

    gni_annual_growth_query = EconomicData.query.filter_by(year=current_year).order_by(EconomicData.gni_growth_percent.desc()).all()
    gni_annual_growth_rank = get_rankings(gni_annual_growth_query, country_code=country_code)

    gni_ranks = {
        'gni_rank': gni_usd_rank,
        'gni_per_capita_rank': gni_per_capita_rank,
        'gni_annual_growth_rank': gni_annual_growth_rank
    }

    ranks = {
        'inflation_ranks': inflation_ranks,
        'gdp_ranks': gdp_ranks,
        'gni_ranks': gni_ranks
    }
    
    return ranks