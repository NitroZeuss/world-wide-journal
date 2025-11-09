import requests


def search_news():
    url = "https://api.worldnewsapi.com/search-news?text=earth+quake&language=en&earliest-publish-date=2024-04-01"
    api_key = "39505ce38e2b41ab9cc8a0c49d5d3735"

    headers = {'x-api-key': api_key}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code}"


def top_news():
    url = "https://api.worldnewsapi.com/top-news?source-country=us&language=en&date=2024-05-29"
    api_key = "39505ce38e2b41ab9cc8a0c49d5d3735"

    headers = {'x-api-key': api_key}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code}"


def search_sources():
    url = "https://api.worldnewsapi.com/search-news-sources?name=bbc"
    api_key = "39505ce38e2b41ab9cc8a0c49d5d3735"

    headers = {'x-api-key': api_key}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code}"


if __name__ == "__main__":
    print("Search News:\n", search_news())
    print("\nTop News:\n", top_news())
    print("\nSearch Sources:\n", search_sources())
