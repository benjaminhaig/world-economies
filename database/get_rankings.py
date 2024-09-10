def get_rankings(query, country_code, inverse=False):
    """Takes in a query filtered by year and ordered by value (example gdp_current_usd on EconomicData) in descending order.
    Returns a string of where the country ranks. Pass inverse as True for metrics that when large are a negative (such as inflation).
    
    Keyword arguments:
    argument -- Query from SQLAlchemy (list), Country code (string), inverse (boolean, default False)
    Return: tuple (ranking, total number of countries)
    """
    ranking = ([index for index, item in enumerate(query) if item.country_code == country_code].pop() + 1)
    total = len(query)
    if (inverse):
        ranking = total - ranking
        ranking += 1
    economy_emojis = ["🔥 Amazing!", "💪 Strong!", "😐 Average", "😬 Struggling", "😭 Weak"]

    percent = (1 - (ranking/total)) * 100
    emoji = None
 
    if percent >= 80: emoji = economy_emojis[0]
    elif percent >= 60: emoji = economy_emojis[1]
    elif percent >= 40: emoji = economy_emojis[2]
    elif percent >= 20: emoji = economy_emojis[3]
    else: emoji = economy_emojis[-1]

    return (ranking, len(query), emoji)


    