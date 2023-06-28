import sys
import unittest

sys.path.append("..")

from demo8.app import app

class Demo8TestCase(unittest.TestCase):
    def setUp(self) -> None:
        app.testing = True
        # 返回一個測試客戶端對象，可以用來模擬客戶端（瀏覽器）
        self.client = app.test_client()

    def test_index(self):
        # 發送 GET 請求到根路由
        response = self.client.get('/')
        
        # 檢查響應狀態碼是否為 200
        self.assertEqual(response.status_code, 200)
        
        # 檢查 session 中的值是否正確
        with self.client.session_transaction() as sess:
            self.assertEqual(sess.get('username'), 'name')
            
        # 檢查響應內容是否為 'ok'
        self.assertEqual(response.get_data(as_text=True), 'ok')

    def test_set_cookie(self):
        response = self.client.get('/set')
        # 檢查回應狀態碼是否為 200
        self.assertEqual(response.status_code, 200)
        # 檢查回應內容是否包含特定字串
        self.assertIn(b'Setting cookie!', response.data)
        # 檢查回應的 Set-Cookie 標頭是否存在
        self.assertTrue('Set-Cookie' in response.headers)

    def test_get_cookie(self):
        self.client.get('/set')
        response = self.client.get('/get')
        # 檢查回應狀態碼是否為 200
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        # 檢查回應內容是否包含特定字串
        self.assertEqual("flask", data["framework"])

    # 'delete cookies'
    def test_del_cookie(self):
        response = self.client.get('/del')
        # 檢查回應狀態碼是否為 200
        self.assertEqual(response.status_code, 200)
        # 檢查回應內容是否包含特定字串
        self.assertIn(b'delete cookies', response.data)
       
if __name__ == '__main__':
    unittest.main()