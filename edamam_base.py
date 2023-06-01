#go to https://developer.edamam.com/admin/applications and see your app_id & app_key

#SOURCE FOR QUERY OF NUTRITION DETAILS: https://developer.edamam.com/edamam-docs-nutrition-data-api

#demo of recipes: https://www.edamam.com/results/recipes/?search=butternut%20squash%20curry
#demo of nutrition details api: https://developer.edamam.com/edamam-nutrition-api-demo
#dashboard of nutritionix: https://www.nutritionix.com/dashboard

import requests
import json
import pandas as pd

#I PUT MY WRAPPERS FOR 3 APIs HERE:

def recipe_search(ingredient, app_id = '06d214b7', app_key = 'aa13fd9849c50147db6825a20c992dac'):
    '''query for recipe search api'''
    result = requests.get('https://api.edamam.com/search?q={}&app_id={}&app_key={}'.format(ingredient, app_id, app_key))
    data = result.json()
    return data#['hits']
#print(json.dumps(recipe_search('1%20butternut%20squash'), indent=4))

def food_database(ingredient, app_id = 'ff645722', app_key = 'bb33b6fafc32f853d2310b2100ff7540'):
    '''query for food database api'''
    result = requests.get('https://api.edamam.com/api/food-database/v2/parser?ingr={}&app_id={}&app_key={}'.format(ingredient, app_id, app_key))
    data = result.json()
    return data#['hits']

def nutrition_details(ingredient, app_id = '9a1286ed', app_key = 'fa2b2b31f4a34a334a4ef84291dd8f59 '):
    '''query for nutrition details api'''
    result = requests.get('https://api.edamam.com/api/nutrition-data?ingr={}&app_id={}&app_key={}'.format(ingredient, app_id, app_key))
    data = result.json()
    return data#['hits']

#------------------------------------------------------------------------
def get_nutrition(product):
    '''get final df of specific PRODUCT nutrition'''
    product = product.replace(' ', '%20')
    nd = nutrition_details(product)
    weight_val = nd["totalWeight"]
    d = {'_WEIGHT': {'label': 'Weight', 'quantity': weight_val, 'unit': 'g'}}
    df = pd.DataFrame.from_records({**d, **nd["totalNutrients"]}).T
    return df

#ensure every individual ingredient has a proper output:
#df = get_nutrition('150g canned choped peeled tomatoes')
#print(df)

def get_recipe_nutrition(recipe):
    '''get full df of specific RECIPE nutrition + metadata'''
    ingredients = recipe.split('\n')
    name = ingredients[0]
    _df = get_nutrition(name)
    init_df = pd.DataFrame({name: _df.quantity})
    init_df_meta = _df.drop(columns='quantity')
    for name in ingredients[1:]:
        _df = get_nutrition(name)
        init_df_meta = pd.merge(init_df_meta.reset_index(),
                                _df.drop(columns='quantity').reset_index(),
                                how='outer').set_index('index')
        init_df = pd.merge(init_df.reset_index(),
                           pd.DataFrame({name: _df.quantity}).reset_index(),
                           how='outer').set_index('index')
    return init_df.astype(float), init_df_meta


def get_recipe_prices(recipe, file='recipes/chicken_with_curry/prices.json'):
    '''get full df of specific RECIPE prices'''
    with open(file, 'r') as f:
        shop = json.load(f)["ingredients"]
        _shop_data = [nutrition_details(x["nutr_name"]) for x in shop]
        shop_set_weights = {x['ingredients'][0]['parsed'][0]['food']: x["totalWeight"] for x in _shop_data}
        shop_set_prices = {x['ingredients'][0]['parsed'][0]['food']: y['price'] for x, y in zip(_shop_data, shop)}

        recipe_set = recipe.split('\n')
        _recipe_data = [nutrition_details(x) for x in recipe_set]
        recipe_set_weights = {x['ingredients'][0]['parsed'][0]['food']: x["totalWeight"] for x in _recipe_data}
        recipe_set_prices = {
            x: shop_set_prices[x] * recipe_set_weights[x] / shop_set_weights[x] if x in shop_set_weights else None for x
            in recipe_set_weights}

    return pd.DataFrame(recipe_set_prices, index=[0])

def get_intakes(idx):
    with open('daily_intakes.json', 'r') as f:
        data = json.load(f)["daily_intakes"]
        df = pd.DataFrame.from_records(data).set_index('tag')
    return df.reindex(idx).quantity

recipe = \
'''1 spoon butter ghee
250g butternut squash
1 red onion
5g curry
1 teaspoon ground hot peppers
200g chicken fillet
200g boiled chickpeas
150g canned tomatoes
150ml coconut milk
100g spinach'''


#nutr_df, nutr_df_meta = get_recipe_nutrition(recipe)
#price_df = get_recipe_prices(recipe)
#intake_df = get_intakes(nutr_df_meta.index)
#x = price_df






