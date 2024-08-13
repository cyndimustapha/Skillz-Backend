from flask import Flask, request, jsonify
#import requests
import base64
from datetime import datetime
from flask_restful import Resource
app = Flask(__name__)

class PaymentResource(Resource):

 def get_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    consumer_key = "m8JMckxJn0aRtrqnoqD7ey4jH1w2WYbyhGe4tXGqMF9GxOGC" 
    consumer_secret = "NfRXzw0qDCzXdu01TZqB8ojBobIknXCQ5E2BUCAKSEezF2dwrrCUmR4mN9GBk4Ze"  
    auth = base64.b64encode(f"{consumer_key}:{consumer_secret}".encode()).decode()

    headers = {
        "Authorization": f"Basic {auth}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get("access_token")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

@app.route('/getToken', methods=['GET'])
def get_token_route():
    token = get_token()
    if token:
        return jsonify({"access_token": token})
    else:
        return jsonify({"error": "Unable to get token"}), 500

@app.route('/sendSTKPush', methods=['POST'])
def send_stk_push():
    short_code = 174379
    phone = "705332395"
    amount = "10"
    passkey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

    token = get_token()
    if not token:
        return jsonify({"error": "Unable to get token"}), 500

    date = datetime.now()
    timestamp = date.strftime("%Y%m%d%H%M%S")
    password = base64.b64encode(f"{short_code}{passkey}{timestamp}".encode()).decode()
    
    data = {
        "BusinessShortCode": short_code,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": f"254{phone}",
        "PartyB": short_code,
        "PhoneNumber": f"254{phone}",
        "CallBackURL": "https://mydomain.com/path",
        "AccountReference": "Mpesa Test",
        "TransactionDesc": "Testing stk push"
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return jsonify({"error": "Unable to process STK push"}), 400

#if __name__ == "__main__":
   # app.run(debug=True)
