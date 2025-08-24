from django.shortcuts import render, redirect, get_object_or_404
import requests
from django.http import JsonResponse
from .models import PopularCocktail


def search_page(request):
    query = request.GET.get('query')
    name_results = []
    ingredient_results = {}
    search_results = []

    if query:
        name_api_url = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s={query}"
        s1_response = requests.get(name_api_url)

        if s1_response.status_code == 200:
            s1_data = s1_response.json()
            drinks1 = s1_data.get('drinks') or []
            if drinks1:
                name_results += [{'id': drink['idDrink'], 'name': drink['strDrink'], 'thumbnail': drink['strDrinkThumb']} for drink in drinks1]


        ingredients = query.split()
        ingredient_cocktail_set = []
        for ingredient in ingredients:
            ingredient_api_url = f"https://www.thecocktaildb.com/api/json/v1/1/filter.php?i={ingredient}"                         
            s2_response = requests.get(ingredient_api_url)

            if s2_response.status_code == 200:
                s2_data = s2_response.json()
                drinks2 = s2_data.get('drinks') or []
                if drinks2:
                    ingredient_cocktail_set.append({(drink['idDrink'], drink['strDrink'], drink['strDrinkThumb'])for drink in drinks2 if isinstance(drink,dict)})

        if ingredient_cocktail_set:
            if len(ingredient_cocktail_set) == 1:
                ingredient_results = ingredient_cocktail_set[0]
            else:
                ingredient_results = set.intersection(*ingredient_cocktail_set)

        ingredient_results = [{'id': id, 'name': name, 'thumbnail': thumb} for (id, name, thumb) in ingredient_results]

        search_results = name_results + ingredient_results

    return render(request, "search.html", {'search_results': search_results, 'query': query})



def detail_page(request, item_id):
    id_detail_url = f"https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i={item_id}"
    response = requests.get(id_detail_url)

    if response.status_code == 200:
        data = response.json()
        drinks = data.get('drinks')
        if drinks:
            drink = drinks[0]
            ingredients = []
            for i in range(1, 4): 
                ingredient = drink.get(f'strIngredient{i}')
                measure = drink.get(f'strMeasure{i}')
                if ingredient:
                    ingredients.append({
                        'ingredient': ingredient if ingredient else None,
                        'measure': measure if measure else None,
                    })

            cocktail_obj, created = PopularCocktail.objects.get_or_create(
                cocktail_id=drink['idDrink'],
                defaults={
                    'name': drink['strDrink'],
                    'image': drink['strDrinkThumb'],
                    'alcoholic': drink['strAlcoholic'],
                    'instructions': drink.get('strInstructions'),
                    'ingredients': ingredients,
                    'search_count': 1,
                }
            )

            if not created:
                cocktail_obj.search_count += 1
                cocktail_obj.save()

            context = {
                'name': drink['strDrink'],
                'image': drink['strDrinkThumb'],
                'alcoholic': drink['strAlcoholic'],
                'instructions': drink.get('strInstructions'),
                'ingredients': ingredients
            }
            return render(request, 'detail.html', context)

    return render(request, 'detail.html', {'error': 'Drink not found'})

def popular_cocktails(request):
    cocktails = PopularCocktail.objects.order_by('-search_count')
    return render(request, 'popular.html', {'cocktails': cocktails})


def delete_cocktail(request, cocktail_id):
    cocktail = get_object_or_404(PopularCocktail, id=cocktail_id)
    cocktail.delete()
    return redirect('popular cocktails')