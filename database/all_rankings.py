from datetime import datetime
from .get_rankings import get_rankings
from .models import EconomicData, IMFData
from database import db
import database
from sqlalchemy import func


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
    # inflation_average_query = IMFData.query.filter_by(year=current_year).order_by(IMFData.inflation_avg_consumer_prices.desc()).all()
    inflation_average_query = (IMFData.query
    .filter_by(year=current_year)
    .order_by(
        IMFData.inflation_avg_consumer_prices.desc(),
        IMFData.country_code.desc()
    )
    .all()) 
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

    # Gini Coefficient
    gini_subquery = (
    db.session.query(
        EconomicData.country_code,
        func.max(EconomicData.year).label('max_year')
    )
    .filter(EconomicData.gini_index != None)
    .group_by(EconomicData.country_code)
    .subquery()
    )

    gini_query = (
        EconomicData.query
        .join(
            gini_subquery,
            (EconomicData.country_code == gini_subquery.c.country_code) &
            (EconomicData.year == gini_subquery.c.max_year)
        )
        .filter(EconomicData.gini_index != None)
        .order_by(EconomicData.gini_index.asc())
        .all()
    )
    gini_rank = get_rankings(gini_query, country_code=country_code)

    # Lowest 10%
    lowest_ten_subquery = (
        db.session.query(
            EconomicData.country_code,
            func.max(EconomicData.year).label('max_year')
        )
        .filter(EconomicData.lowest_ten_percent != None)
        .group_by(EconomicData.country_code)
        .subquery()
    )

    lowest_ten_query = (
        EconomicData.query
        .join(
            lowest_ten_subquery,
            (EconomicData.country_code == lowest_ten_subquery.c.country_code) &
            (EconomicData.year == lowest_ten_subquery.c.max_year)
        )
        .filter(EconomicData.lowest_ten_percent != None)
        .order_by(EconomicData.lowest_ten_percent.asc())
        .all()
    )
    lowest_10_rank = get_rankings(lowest_ten_query, country_code=country_code, inverse=True)

    # Highest 10%
    highest_ten_subquery = (
        db.session.query(
            EconomicData.country_code,
            func.max(EconomicData.year).label('max_year')
        )
        .filter(EconomicData.highest_ten_percent != None)
        .group_by(EconomicData.country_code)
        .subquery()
    )

    highest_ten_query = (
        EconomicData.query
        .join(
            highest_ten_subquery,
            (EconomicData.country_code == highest_ten_subquery.c.country_code) &
            (EconomicData.year == highest_ten_subquery.c.max_year)
        )
        .filter(EconomicData.highest_ten_percent != None)
        .order_by(EconomicData.highest_ten_percent.asc())
        .all()
    )
    highest_10_rank = get_rankings(highest_ten_query, country_code=country_code)


    equality_ranks = {
        "gini_rank": gini_rank,
        "lowest_ten_rank": lowest_10_rank,
        "highest_ten_rank": highest_10_rank
    }

    # Employment & Trade

    # Unemployment
    unemployment_subquery = (
    db.session.query(
        EconomicData.country_code,
        func.max(EconomicData.year).label('max_year')
    )
    .filter(EconomicData.unemployment != None)
    .group_by(EconomicData.country_code)
    .subquery()
    )

    unemployment_query = (
        EconomicData.query
        .join(
            unemployment_subquery,
            (EconomicData.country_code == unemployment_subquery.c.country_code) &
            (EconomicData.year == unemployment_subquery.c.max_year)
        )
        .filter(EconomicData.unemployment != None)
        .order_by(EconomicData.unemployment.asc())
        .all()
    )
    unemployment_rank = get_rankings(unemployment_query, country_code=country_code)

    # Exports (%)
    exports_subquery = (
    db.session.query(
        EconomicData.country_code,
        func.max(EconomicData.year).label('max_year')
    )
    .filter(EconomicData.exports_gdp_percent != None)
    .group_by(EconomicData.country_code)
    .subquery()
    )

    exports_query = (
        EconomicData.query
        .join(
            exports_subquery,
            (EconomicData.country_code == exports_subquery.c.country_code) &
            (EconomicData.year == exports_subquery.c.max_year)
        )
        .filter(EconomicData.exports_gdp_percent != None)
        .order_by(EconomicData.exports_gdp_percent.desc())
        .all()
    )
    exports_rank = get_rankings(exports_query, country_code=country_code)

    # Imports (%)
    imports_subquery = (
    db.session.query(
        EconomicData.country_code,
        func.max(EconomicData.year).label('max_year')
    )
    .filter(EconomicData.exports_gdp_percent != None)
    .group_by(EconomicData.country_code)
    .subquery()
    )

    imports_query = (
        EconomicData.query
        .join(
            imports_subquery,
            (EconomicData.country_code == imports_subquery.c.country_code) &
            (EconomicData.year == imports_subquery.c.max_year)
        )
        .filter(EconomicData.imports_gdp_percent != None)
        .order_by(EconomicData.imports_gdp_percent.desc())
        .all()
    )
    imports_rank = get_rankings(imports_query, country_code=country_code)

    additional_ranks = {
        'unemployment_rank': unemployment_rank,
        'exports_rank': exports_rank,
        'imports_rank': imports_rank
    }


    ranks = {
        'inflation_ranks': inflation_ranks,
        'gdp_ranks': gdp_ranks,
        'gni_ranks': gni_ranks,
        'equality_ranks': equality_ranks,
        'additional_ranks': additional_ranks
    }
    
    return ranks