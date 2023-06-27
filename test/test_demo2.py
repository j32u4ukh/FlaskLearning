import sys
import unittest
import sys
sys.path.append("..")

from demo2 import app as app1
from demo2.routing import app as app2


class Demo2TestCase(unittest.TestCase):
    def setUp(self) -> None:
        # 返回一個測試客戶端對象，可以用來模擬客戶端（瀏覽器）
        self.client1 = app1.test_client()
        self.client2 = app2.test_client()

    def test_index(self):
        response = self.client1.get("/")
        data = response.get_data(as_text=True)
        self.assertIn("Hello, World!", data)
        self.assertEqual(200, response.status_code)

    def test_hello(self):
        response = self.client1.get("/hello")
        data = response.get_data(as_text=True)
        self.assertIn("Hello, World!", data)
        self.assertEqual(200, response.status_code)

    def test_name(self):
        response = self.client2.get("/data/appInfo/Tom")
        data = response.get_data(as_text=True)
        self.assertIn("String => Tom", data)
        self.assertEqual(200, response.status_code)

    def test_id(self):
        response = self.client2.get("/data/appInfo/id/9527")
        data = response.get_data(as_text=True)
        self.assertIn("int => 9527", data)
        self.assertEqual(200, response.status_code)

    def test_name(self):
        response = self.client2.get("/data/appInfo/version/3.14")
        data = response.get_data(as_text=True)
        self.assertIn("float => 3.14", data)
        self.assertEqual(200, response.status_code)


if __name__ == "__main__":
    unittest.main()