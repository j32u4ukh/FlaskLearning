import sys
import unittest

sys.path.append("..")

from demo5 import app

class Demo5TestCase(unittest.TestCase):
    def setUp(self) -> None:
        # 返回一個測試客戶端對象，可以用來模擬客戶端（瀏覽器）
        self.client = app.test_client()

    def test_get(self):
        response = self.client.get('/data/message')
        data = response.get_json()
        self.assertEqual(5, data["appInfo"]["id"])
        self.assertEqual("Python - Flask", data["appInfo"]["name"])
        self.assertEqual("1.0.1", data["appInfo"]["version"])
        self.assertEqual("author", data["appInfo"]["author"])
        self.assertEqual("Python - Web Framework", data["appInfo"]["remark"])

    def test_post(self):
        response = self.client.post('/data/message', data = {
                'app_id': 5,
                'app_name': "Python - Flask",
                'app_version': "1.0.1",
                'app_author': "author",
                'app_remark': "Python - Web Framework"
            })
        self.assertEqual(200, response.status_code)
        data = response.get_json()
        self.assertEqual("OK", data["result"])


if __name__ == "__main__":
    unittest.main()