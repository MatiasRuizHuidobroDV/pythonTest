"""
Refactor the next function using yield to return the array of objects found by the
`s3.list_objects_v2` function that matches the given prefix.
"""
def get_s3_objects(bucket, prefix=''):
    s3 = boto3.client('s3')

    kwargs = {'Bucket': bucket}
    next_token = None
    if prefix:
        kwargs['Prefix'] = prefix
    object_list = []
    while True:
        if next_token:
            kwargs['ContinuationToken'] = next_token
        resp = s3.list_objects_v2(**kwargs)
        contents = resp.get('Contents', [])
        for obj in contents:
            key = obj['Key']
            if key.startswith(prefix):
                yield obj
        next_token = resp.get('NextContinuationToken', None)

        if not next_token:
            break
    return object_list

"""
Please, full explain this function: document iterations, conditionals, and the
function as a whole
"""
def fn(main_plan, obj, extensions=[]):
    # The function recieves three arguments, main_plan, obj, extensions.
    # The argument extensions has a default value (empty array)
    # main_plan is an object
    # obj is a dictionary of objects
    # extensions is a list of dictionaries.
    items = []
    sp = False
    cd = False 

    ext_p = {}

    for ext in extensions: # It will iterate once per item in the passed variable extensions
        # If extensions is empty, then this wont be executed
        ext_p[ext['price'].id] = ext['qty'] # Saves in the ext_p dictionary.
        # Using as key the price id of the ext variable and as value the quantity.

    for item in obj['items'].data: # Iterates over each item present in the items data property
        product = { # Instanciates the variable (dict) product with the key "id" and associated value "item.id" 
            'id': item.id
        }
        # If the item price id is different from the main plan id and its not present in ext_p, then
        if item.price.id != main_plan.id and item.price.id not in ext_p:
            product['deleted'] = True # assigns the True value to the "deleted" key for the product dict.
            cd = True # sets cd to True
        # If the previous condition was false (the item price id was equal to the main plan id or it was present in ext_p)
        # and the item price id is present in ext_p, then
        elif item.price.id in ext_p:
            qty = ext_p[item.price.id] # qty will be the item's price id
            if qty < 1: # if the item price id is lesser than one, then
                product['deleted'] = True  # assigns the True value to the "deleted" key for the product dict.
            # if the previous condition is false (the item price id is greater or equal to one)
            else:
                product['qty'] = qty # Set the value qty (item's price id) for the product key "qty"
            del ext_p[item.price.id] # delete the item price id from the ext_p dict
        # If none of previous conditions was true (the item price id was equal to the main plan id and it was not present in ext_p)
        # and the item price id is equal to the main_plan id, then
        elif item.price.id == main_plan.id:
            sp = True # sets sp to True


        items.append(product) # Adds to the end of the items list, the current product dict
        # containing the keys id, and either the deleted or qty key.
    # if sp is False which happens when:
    # A) the item price id is different from the main plan id and its not present in ext_p
    # B) the item price id was equal to the main plan id and/or the item price id is present in ext_p
    if not sp:
        items.append({
            'id': main_plan.id,
            'qty': 1
        })  # Adds to the end of the items list, a dict that has the value of the id attribute 
        # of the main_plan object for the "id" key and value 1 for the key "qty"
    # Iterates over the key, value pairs in ext_p dictionary
    # Assigning the keys to the variable price and the values to the variable qty
    for price, qty in ext_p.items():
        # If qty is lesser than 1, then
        if qty < 1:
            continue # skip to the next iteration
        # if qty is greater or equal to 1, then
        items.append({
            'id': price,
            'qty': qty
        }) # Adds to the end of the items list, a dict that has the value price id for the "id" key
        # and value qty for the "qty" key
    
    return items # returns the items list
    """
        This function will iterate over all the "items" present in the data attribut of obj['items']
        For each of this items it will create a "product" that will be appended to a list.
        Each of this products will have a key "id".
        The products that had a "price id" different from the "main_plan" id or that where present
        in the "extensions" list and had a "price id" lesser than one, will have a "deleted" key of value True.
        The products that had a "price id" different from the "main_plan" id or that where present
        in the "extensions" list and had a "price id" greater or equal to one, will have a "qty" key of value item.price.id.
        This list of "products" will be returned.

        If either:
            the item price id is different from the main plan id and its not present in ext_p
            or
            the item price id was equal to the main plan id and/or the item price id is present in ext_p
        Then the list of products will also contain a product of "id" equal to the main_plan's id and
            "qty"  1.
        
        If the extensions list is passed, then the list of returned "products" will contain
        an entry for each of this "items" present in the extensions list
    """


"""
Having the class `Caller` and the function `fn`
Refactor the function `fn` to execute any method from `Caller` using the argument `fn_to_call`
reducing the `fn` function to only one line.
"""
class Caller:
    add = lambda a, b : a + b
    concat = lambda a, b : f'{a},{b}'
    divide = lambda a, b : a / b
    multiply = lambda a, b : a * b

def fn(fn_to_call, *args):
    return getattr(Caller,fn_to_call)(*args)


"""
A video transcoder was implemented with different presets to process different videos in the application. 
The videos should be encoded with a given configuration done by this function. 
Can you explain what this function is detecting from the params and returning based in its conditionals?
"""
def fn(config, w, h):
    # The function expects three arguments.
    # config is a dictionary of lists, with keys "p", "l" and "s". Each of this keys has a list of dictionaries
    # associated, where each dictionary in the list has a key "width" and an associated numerical value
    # w is the width of the video
    # and h is height of the video
    v = None
    ar = w / h # calculate the aspect ratio 

    if ar < 1: # if the aspect ratio is lesser than 1 (its taller than wider)
        v = [r for r in config['p'] if r['width'] <= w] # Collects the r elements of the config value associated to the "p" key that have a width inferior or equal to w
    elif ar > 4 / 3:  # if the aspect ratio is bigger than 4/3 (its much wider than taller)
        v = [r for r in config['l'] if r['width'] <= w] # Collects the r elements of the config value associated to the "l" key that have a width inferior or equal to w
    else: # if the aspect ratio is lesser or equal to 4/3 but bigger or equal to 1 (its wider than taller or square)
        v = [r for r in config['s'] if r['width'] <= w] # Collects the r elements of the config value associated to the "s" key that have a width inferior or equal to w

    return v # returns the r elements of the corresponding config list
        # p if the aspect ratio is taller than wider
        # l if its much wider than taller
        # s if its wider than taller, or squared
    # that have a width lesser or equal to w

"""
Having the next helper, please implement a refactor to perform the API call using one method instead of rewriting the code
in the other methods.
"""
import requests
class Helper:
    DOMAIN = 'http://example.com'
    SEARCH_IMAGES_ENDPOINT = 'search/images'
    GET_IMAGE_ENDPOINT = 'image'
    DOWNLOAD_IMAGE_ENDPOINT = 'downloads/images'

    AUTHORIZATION_TOKEN = {
        'access_token': None,
        'token_type': None,
        'expires_in': 0,
        'refresh_token': None
    }

    def query(self, url, data, protocol):
        token_type = self.AUTHORIZATION_TOKEN['token_type']
        access_token = self.AUTHORIZATION_TOKEN['access_token']

        headers = {
            'Authorization': f'{token_type} {access_token}',
        }

        send = {
            'headers': headers,
            'data': data
        }

        return getattr(request, protocol)(requests, method)(url, **send)

    def search_images(self, **kwargs):
        URL = f'{self.DOMAIN}/{self.SEARCH_IMAGES_ENDPOINT}'

        return self.query(URL, kwargs, "get")
        
    def get_image(self, image_id, **kwargs):
        URL = f'{self.DOMAIN}/{self.GET_IMAGE_ENDPOINT}/{image_id}'

        return self.query(URL, kwargs, "get")

    def download_image(self, image_id, **kwargs):
        URL = f'{self.DOMAIN}/{self.DOWNLOAD_IMAGE_ENDPOINT}/{image_id}'

        return self.query(URL, kwargs, "post")
