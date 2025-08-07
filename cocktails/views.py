from django.shortcuts import render
import requests
from django.http import JsonResponse


def search_page(request):
    query = request.GET.get('query')
    name_results = []
    ingredient_results = []
    search_results = []

    if query:
        name_api_url = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s={query}"
        s1_response = requests.get(name_api_url)

        if s1_response.status_code == 200:
            s1_data = s1_response.json()
            drinks1 = s1_data.get('drinks') or []
            if drinks1:
                name_results += [{'name': drink['strDrink'], 'thumbnail': drink['strDrinkThumb']} for drink in drinks1]



        ingredient_api_url = f"https://www.thecocktaildb.com/api/json/v1/1/filter.php?i={query}"                         
        s2_response = requests.get(ingredient_api_url)

        if s2_response.status_code == 200:
            s2_data = s2_response.json()
            drinks2 = s2_data.get('drinks') or []
            if drinks2:
                ingredient_results += [{'name': drink['strDrink'],'thumbnail': drink['strDrinkThumb']} for drink in drinks2]

        search_results = name_results + ingredient_results

    return render(request, "search.html", {'search_results': search_results, 'query': query})