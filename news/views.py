import requests
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.core.cache import cache
from django.core.paginator import Paginator

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
@permission_classes([AllowAny])
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
    page_number = request.GET.get("page", 1)

    cache_key = f"top_news_{country}_{language}_{date}"
    data = cache.get(cache_key)

    if not data:
        url = f"{BASE_URL}/top-news?source-country={country}&language={language}&date={date}"
        headers = {"x-api-key": API_KEY}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            cache.set(cache_key, data, timeout=3600)  # Cache for 1 hour
        else:
            return JsonResponse(
                {"error": response.status_code, "details": response.text},
                status=response.status_code
            )

    # Assuming the API returns a 'top_news' key containing the list of articles
    news_list = data.get("top_news", [])
    if not news_list and isinstance(data, list): # Fallback if data itself is the list
        news_list = data
    
    paginator = Paginator(news_list, 20)
    page_obj = paginator.get_page(page_number)
    
    return JsonResponse({
        "top_news": list(page_obj),
        "page": page_obj.number,
        "total_pages": paginator.num_pages,
        "total_items": paginator.count
    }, safe=False)



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
