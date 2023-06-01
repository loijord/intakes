#basic calculations could be done online

from nutritionix import Nutritionix
nix = Nutritionix(app_id="123456789", api_key="XXXYYYZZZ")

meal_search = nix.search("chocolate milkshake", results='0:50').json() #results="0:1"
meal_ids = (n['_id'] for n in meal_search['hits'])
for key, val in meal_search.items():
    if key != 'hits':
        print(f'{key}: {val}')
    else:
        print('hits:')
        for id in meal_ids:
            item = nix.item(id=id).json()
            for key, val in item.items():
                print(f'    {key}: {val}')
            print('-' * 50)





'''
brand_search = nix.brand().search(query="mcdonalds").json()
brand_ids = (n['_id'] for n in brand_search['hits'])
for key, val in brand_search.items():
    if key != 'hits':
        print(f'{key}: {val}')
    else:
        print('hits:')
        for id in brand_ids:
            item = nix.brand(id).json()
            for key, val in item.items():
                print(f'    {key}: {val}')
            print('-' * 50)
'''
