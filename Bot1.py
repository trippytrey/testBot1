import requests
import random
from bs4 import BeautifulSoup as bs

session = requests.session()        #Creates new Session object


def get_sizes_in_stock():
    global session      #accesses session
    endpoint = "http://www.jimmyjazz.com/mens/footwear/nike-vapormax-flyknit/849558-009?color=Black"    #Shoe URL
    response = session.get(endpoint)        #goes to the endpoint, creates a get request, and returns in to the response variable

    soup = bs(response.text, "html.parser")      #goes to the reponse text and parses the HTML
    div = soup.find("div", {"class": "box_wrapper"})       #Finding a 'div' of class 'box_wrapper' (View page source for better understanding)
    find_all_sizes = div.find_all("a")      #Finds all 'a' tabs within 'box_wrapper'

    sizes_in_stock = []
    for size in find_all_sizes:     #for loop that runs through the 'find_all_sizes' variable
        if "piunavailable" not in size["class"]:        #if statement that checks to see if the size is available, if so then do whats underneath
            size_id = size["id"]        #sets size_id to the contents equal to 'id' in the page source
            sizes_in_stock.append(size_id.split("_")[1])       #splits the information after the underscore in size id into 2 elements, the word 'itemcode' and the numerical value for the id then chooses the second element and stores it in size_id

    return sizes_in_stock       #returns sizes in stock

##print get_sizes_in_stock()        #prints sizes in stock

def add_to_cart():
    global session
    sizes_in_stock = get_sizes_in_stock()       #sets variable sizes_in_stock to the function get_sizes_in_stock
    random_size = random.choice(sizes_in_stock)     #chooses random size in stock

    endpoint = "http://www.jimmyjazz.com/cart-request/cart/add/%s/1"%(random_size)  #URL for the atc, the '%s" and '%(random_size)' adds a random size to cart
    response = session.get(endpoint)

    ##return '"success":1' in response.text         #prints out true or false depending on if the add to cart is successful based on the response text

def checkout():
    global session

    endpoint0 ="https://www.jimmyjazz.com/cart/checkout"
    response0 = session.get(endpoint0)

    soup = bs(response0.text, "html.parser")

    inputs = soup.find_all(input, {"name": "form_build_id"})       #finds the tag with the header input, that includes the words 'name' and 'form_build_id'
    form_build_id = inputs[1]["value"]      #gives the second form_build_id value since we have 2, takes the contens from the attribute 'value' and store in form_build_id


    endpoint1 = "https://www.jimmyjazz.com/cart/checkout"
    payload1 = {
        "billing_email": "treyoung12@yahoo.com",
        "billing_email_confirm": "treyoung12@yahoo.com",
        "billing_phone": "3015354949",
        "email_opt_in": "1",
        "shipping_first_name": "Trey",
        "shipping_last_name": "Young",
        "shipping_address_1": "707 Milton St.",
        "shipping_address_2": "",
        "shipping_city": "Greensboro",
        "shipping_state": "NC",
        "shipping_zip": "33647",
        "shipping_method": "0",
        "signature_required": "0",
        "billing_same_as_shipping": "1",
        "billing_first_name": "",
        "billing_last_name": "",
        "billing_country": "US",
        "billing_address_1": "",
        "billing_address_2": "",
        "billing_city": "",
        "billing_state": "",
        "billing_zip": "",
        "cc_type": "Visa",
        "cc_number": "4859 1027 3205 1592",
        "cc_exp_month": "04",
        "cc_exp_year": "21",
        "cc_cvv": "470",
        "gc_num": "",
        "form_build_id": form_build_id,
        "form_id": "cart_checkout_form"
    }
    response1 = session.post(endpoint1)



