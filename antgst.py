from datetime import date
from urllib.parse import urlencode
import requests
import json
import time
import pandas as pd
import os


def get_auth_code():
    """
    Retrieves the authentication code and key from the antgst website.

    Returns:
        tuple: A tuple containing the authentication code and key.
    """
    url_checkKey = "https://web.antgst.com/antgst/sys/getCheckCode?_t=" + str(
        int(time.time())
    )

    headers = {"Content-Type": "application/json"}

    response = requests.get(url_checkKey, headers=headers)

    data = json.loads(response.text)
    code = data.get("result").get("code")
    key = data.get("result").get("key")
    return code, key


def login(code, key, options={}):
    # Define the URL for the POST request
    url_login = "https://web.antgst.com/antgst/sys/login"

    # Define the headers for the POST request
    headers = {"Content-Type": "application/json"}

    # Define the data for the POST request
    # TODO: need to change the username and password by user. no hard code
    data = {
        "username": "ANT_JYB",
        "password": "321987qq",
        "remember_me": True,
        "captcha": code,
        "checkKey": key,
    }

    data.update(options)

    # Send the POST request
    response = requests.post(url_login, headers=headers, data=json.dumps(data))
    data = json.loads(response.text)
    token = data.get("result").get("token")
    return token


def fetch_data(
    token,
    option={},
    base_url="https://web.antgst.com/antgst/sms/marketing/sendRecordList",
):
    timestamp = int(time.time())
    today = date.today()
    base_query = {
        "_t": timestamp,
        "day": today,
        "column": "createTime",
        "order": "desc",
        "gatewayDr": "000",
        "field": "countryName,smsTo,sendTime",
        "pageNo": 1,
        "pageSize": 1000,
    }
    # Combine the dictionaries
    query = {**base_query, **option}

    # Create the URL
    url = f"{base_url}?{urlencode(query)}"
    print(url)
    headers = {"X-Access-Token": token}
    response = requests.get(url, headers=headers)

    return response.text


def save_data(response):
    # Assuming response is a JSON string
    json_str = response

    # Convert JSON string to Python object
    data = json.loads(json_str)

    # Assuming data is a dictionary containing the result and records
    records = data.get("result").get("records")
    # if records is none, return
    if len(records) == 0:
        return

    df = pd.DataFrame(records)

    def get_unique_filename(base_filename, extension):
        counter = 1
        while os.path.isfile(f"{base_filename}{counter}.{extension}"):
            counter += 1
        return f"{base_filename}{counter}.{extension}"

    # if not os.path.exists the folder, create it
    if not os.path.exists("./data"):
        os.makedirs("./data")
    # Save the data frame to a CSV file
    csv_filename = get_unique_filename("./data/output", "csv")
    df.to_csv(csv_filename, index=False)


if __name__ == "__main__":
    code, key = get_auth_code()
    user = {"username": "ANT_JYB", "password": "321987qq"}
    token = login(code, key, user)
    option = {"pageSize": 2000}
    response = fetch_data(token, option)
    save_data(response)
