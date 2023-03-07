import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    products = search_products(query)
    return jsonify(products)


def get_data_amazon(query):
    url = f"https://www.amazon.in/s?k={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")

    products = []

    for item in soup.select(".s-result-item"):
        try:
            image = item.select_one(".s-image")["src"]
            name = item.select_one(".a-text-normal").text.strip()
            link = "https://www.amazon.in" + item.select_one(".a-link-normal")["href"]
            price = item.select_one(".a-price-whole").text.strip()
            price = int(price.replace(",", ""))
            products.append({
                "source": "Amazon",
                "image": image,
                "name": name,
                "link": link,
                "price": price
            })
        except:
            pass

    return products


def get_data_flipkart(query):
    url = f"https://www.flipkart.com/search?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")

    products = []

    for item in soup.select("._13oc-S, ._1YokD2"):
        try:
            image = item.select_one("._312yBx, .CXW8mj").img["src"]
            name = item.select_one(".IRpwTa, ._4rR01T").text.strip()
            link = "https://www.flipkart.com" + item.select_one("._3bPFwb, ._1fQZEK")["href"]
            price = item.select_one("._30jeq3, _30jeq3").text.strip()
            price = int(price.replace("₹", "").replace(",", ""))
            products.append({
                "source": "Flipkart",
                "image": image,
                "name": name,
                "link": link,
                "price": price
            })
        except:
            pass

    return products


def get_data_paytm(query):
    url = f"https://paytmmall.com/shop/search?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")

    products = []

    for item in soup.select("._1fje"):
        try:
            image = item.select_one("._3nWP").img["src"]
            name = item.select_one(".UGUy").text.strip()
            link = "https://paytmmall.com" + item.select_one("._8vVO")["href"]
            price = item.select_one("._1kMS").span.text.strip()
            price = int(price.replace(",", ""))
            products.append({
                "source": "Paytm Mall",
                "image": image,
                "name": name,
                "link": link,
                "price": price
            })
        except:
            pass

    return products


def search_products(query):
    results = []
    results.extend(get_data_amazon(query))
    results.extend(get_data_flipkart(query))
    results.extend(get_data_paytm(query))
    return results

if __name__ == '__main__':
    app.run(debug=True)