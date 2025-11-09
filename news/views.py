import requests
from django.http import JsonResponse
from rest_framework.decorators import api_view

API_KEY = "4f917ea59eb54bef8f9eafe918739eb6"
BASE_URL = "https://api.worldnewsapi.com"


@api_view(["GET"])
def search_news(request):
    """
    Search news articles by text query.
    Example: /api/search-news/?text=earthquake
    """
    text = request.GET.get("text", "earthquake")
    language = request.GET.get("language", "en")
    earliest_date = request.GET.get("earliest", "2024-04-01")

    url = f"{BASE_URL}/search-news?text={text}&language={language}&earliest-publish-date={earliest_date}"
    headers = {"x-api-key": API_KEY}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return JsonResponse(response.json(), safe=False)
    return JsonResponse(
        {"error": response.status_code, "details": response.text},
        status=response.status_code
    )


@api_view(["GET"])
def top_news(request):
    """
    Get top news by source country and language (from headers).
    Example headers:
        country: us
        language: en
    """
    # Extract from headers
    country = request.headers.get("country", "us")
    language = request.headers.get("language", "en")
    date = request.GET.get("date", "2024-05-29")  # optional query param

    url = f"{BASE_URL}/top-news?source-country={country}&language={language}&date={date}"
    headers = {"x-api-key": API_KEY}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return JsonResponse(response.json(), safe=False)
    return JsonResponse(
        {"error": response.status_code, "details": response.text},
        status=response.status_code
    )



@api_view(["GET"])
def search_news_sources(request):
    """
    Search available news sources by name.
    Example: /api/search-sources/?name=bbc
    """
    name = request.GET.get("name", "bbc")

    url = f"{BASE_URL}/search-news-sources?name={name}"
    headers = {"x-api-key": API_KEY}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return JsonResponse(response.json(), safe=False)
    return JsonResponse(
        {"error": response.status_code, "details": response.text},
        status=response.status_code
    )
