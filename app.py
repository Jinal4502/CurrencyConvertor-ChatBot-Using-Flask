from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
    data = request.get_json()
    initial_currency = data['queryResult']['parameters']['unit-currency']['currency']
    amount = data['queryResult']['parameters']['unit-currency']['amount']
    final_currency = data['queryResult']['parameters']['currency-name']
    print(initial_currency)
    print(amount)
    print(final_currency)
    cf = fetch_conversion_factor(initial_currency, final_currency)
    converted_amount = round(amount * cf, 2)
    print(converted_amount)
    reponse = {
        'fulfillmentText' : f"{amount} {initial_currency} is {converted_amount} {final_currency}"
    }
    return jsonify(reponse)


def fetch_conversion_factor(initial, final):
    url = f"https://free.currconv.com/api/v7/convert?q={initial}_{final},{final}_{initial}&compact=ultra&apiKey=567417c7f94237399366"
    response = requests.get(url=url)
    response = response.json()
    print(response)
    return response[f'{initial}_{final}']

if __name__ == "__main__":
    app.run(debug=True)