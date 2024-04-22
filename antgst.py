import requests
import json
import time
import pandas as pd

if __name__ == "__main__":

    url_checkKey = "https://web.antgst.com/antgst/sys/getCheckCode?_t=" + str(
        int(time.time())
    )

    headers = {"Content-Type": "application/json"}

    response = requests.get(url_checkKey, headers=headers)

    data = json.loads(response.text)
    code = data.get("result").get("code")
    key = data.get("result").get("key")

    headers = {"Content-Type": "application/json"}

    response = requests.get(url_checkKey, headers=headers)

    # Define the URL for the POST request
    url_login = "https://web.antgst.com/antgst/sys/login"

    # Define the headers for the POST request
    headers = {"Content-Type": "application/json"}

    # Define the data for the POST request
    data = {
        "username": "ANT_JYB",
        "password": "321987qq",
        "remember_me": True,
        "captcha": code,
        "checkKey": key,
    }

    # Send the POST request
    response = requests.post(url_login, headers=headers, data=json.dumps(data))
    data = json.loads(response.text)
    token = data.get("result").get("token")

    def http_spider(url):
        # eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MTIwNDc1OTAsInVzZXJuYW1lIjoiQU5UX0pZQiJ9.6UxzDGMqYrdJC58ezON_Wb2qgjEUjT7o5YMbb94c8Gs
        headers = {"X-Access-Token": token}
        response = requests.get(url, headers=headers)

        return response.text  # print the response content

    # Use the spider on a specific website
    response = http_spider(
        "https://web.antgst.com/antgst/sms/marketing/sendRecordList?_t=1712040322&day=2024-04-22++&column=createTime&order=desc&field=smsTo,sendTime&pageNo=1&pageSize=10000"
    )

    # Assuming response is a JSON string
    json_str = response

    # Convert JSON string to Python object
    data = json.loads(json_str)

    print(f'get number item :{len(data.get("result").get("records"))}')

    # Assuming data is a dictionary containing the result and records
    records = data.get("result").get("records")

    # Initialize lists to store smsTo and sendTime values
    sms_to_list = []
    send_time_list = []

    # Loop over the records
    for record in records:
        sms_to_list.append(record.get("smsTo"))
        send_time_list.append(record.get("sendTime"))

    # Create a DataFrame from the lists
    df = pd.DataFrame({"smsTo": sms_to_list, "sendTime": send_time_list})

    # Write the DataFrame to an Excel file
    df.to_csv("output.csv", index=False)
