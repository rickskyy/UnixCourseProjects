import base64
import time

import requests
from requests.auth import HTTPBasicAuth


class SimpleClient:

    @staticmethod
    def test(username, password):
        for _ in range(5):
            try:
                res = requests.get('http://localhost:8000', auth=HTTPBasicAuth(username, password))
                print(res.headers)
                if res.status_code == 200:
                    print(res.text)
                else:
                    print(base64.b64decode(res.text.encode()))
            except Exception as err:
                print(err)

            time.sleep(2)


SimpleClient.test(username='test', password='1234')
