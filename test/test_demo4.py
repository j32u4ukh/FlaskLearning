import sys
import unittest

sys.path.append("..")

from demo4 import app


class Demo4TestCase(unittest.TestCase):
    def setUp(self) -> None:
        # 返回一個測試客戶端對象，可以用來模擬客戶端（瀏覽器）
        self.client = app.test_client()

    def test_submit_post(self):
        response = self.client.post('/submit', data={'user': 'John'}, follow_redirects=True)
        self.assertEqual(response.request.path, "/success/post/John")

    def test_submit_get(self):
        response = self.client.get('/submit?user=John', follow_redirects=True)
        self.assertEqual(response.request.path,  "/success/get/John")

    def test_post_success(self):
        response = self.client.get("/success/post/John")
        self.assertEqual(response.status_code, 200)
        self.assertEqual('post : Welcome John ~ !!!', response.get_data(as_text=True))

    def test_get_success(self):
        response = self.client.get("/success/get/John")
        self.assertEqual(response.status_code, 200)
        self.assertEqual('get : Welcome John ~ !!!', response.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()