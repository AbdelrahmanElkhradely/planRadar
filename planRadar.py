import json
import requests


def make_post_request(url, data=None, headers=None):
    """
    Sends a POST request to the specified URL with optional data and headers.

    :param url: The URL to send the POST request to.
    :param data: The data to include in the POST request.
    :param headers: The headers to include in the POST request.
    :return: The response from the server.
    """
    try:
        response = requests.post(url, data=data, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes
        return response
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"Request Error occurred: {err}")
    except Exception as err:
        print(f"Other error occurred: {err}")
    return None


def execute_requests():
    # Define common headers
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'X-PlanRadar-API-Key': 'f365a50a9c35856da6a58c106befcfc0f605b8d16933b6e87067e7fd5898fb3c7939b0d54b7aaedbb2c610d8bf32db79bc0c2363c330a863835daa639e1dc3775bf8d74ab233d46d84ac2b9d054d78b9',
        'User-Agent': 'PostmanRuntime/7.41.1',
        'Host': 'www.planradar.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'Cache-Control': 'no-cache'
    }

    # First POST request
    url1 = "https://www.planradar.com/api/v1/1319140/projects/1319158/ticket_types_project"
    data1 = json.dumps({
        "data": {
            "attributes": {
                "ticket-type-id": "pokwlmn"
            }
        }
    })

    response1 = make_post_request(url1, data=data1, headers=headers)
    print(response1)
    # Second POST request,
    url2 = "https://www.planradar.com/api/v1/1319140/projects/1319158/components"
    data2 = {'data[][attributes][layers][][page]': '1',
             'data[][attributes][layers][][name]': 'test layer',
             'data[][attributes][layers][][rotation]': '0',
             'data[][attributes][layers][][order]': '1',
             'data[][attributes][layers][][reposition-tickets]': 'true'
             }
    headers["Content-Type"] = 'multipart/form-data;'
    response2 = make_post_request(url2, data=data2, headers=headers)

    if response1 is not None:
        # Third POST request,
        data = json.loads(response2.text)
        url3 = "https://www.planradar.com/api/v2/1319140/projects/1319158/tickets"
        data3 = json.dumps({
            "data": {
                "attributes": {
                    "project-id": "1319158",
                    "ticket-type-id": "pokwlmn",
                    "component-id": data["data"][0]["id"],
                    "subject": "test ticket khradely final using webhook",
                    "status-id": "lm"
                }
            }
        })
        headers["Content-Type"] = 'application/json'
        response3 = make_post_request(url3, data=data3, headers=headers)

        if response3 is not None:
            print("Third request successful.")
            return response1, response2, response3
        else:
            print("Third request failed.")
    else:
        print("request failed.")

    return None, None, None


if __name__ == "__main__":
    response1, response2, response3 = execute_requests()
