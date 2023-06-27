import sys
import unittest

sys.path.insert(0, '../demo1') 

from app import app


class Demo1TestCase(unittest.TestCase):
    def setUp(self) -> None:
        # 返回一個測試客戶端對象，可以用來模擬客戶端（瀏覽器）
        self.client = app.test_client()

    def test_hello(self):
        response = self.client.get('/')
        data = response.get_data(as_text=True)
        self.assertIn("Hello, World!", data)
        self.assertEqual(200, response.status_code)

if __name__ == "__main__":
    unittest.main()