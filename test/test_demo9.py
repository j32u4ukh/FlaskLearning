import sys
import unittest

sys.path.append("..")

from demo9.app import app

class Demo9TestCase(unittest.TestCase):
    def setUp(self) -> None:
        app.testing = True
        # 返回一個測試客戶端對象，可以用來模擬客戶端（瀏覽器）
        self.client = app.test_client()

    def login(self):
        data = {"username": "test", "password": "test"}
        response = self.client.post("/login", json=data)
        return response
    
    def test_login(self):
        response = self.login()
        
        # 檢查響應狀態碼是否為 200
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"access_token", response.get_data())

    def test_protected(self):
        response = self.login()
        access_token = response.get_json()["access_token"]
        headers = {'Authorization': f'Bearer {access_token}'}
        response = self.client.post("/protected", headers=headers)
        data = response.get_json()
        self.assertEqual("ok", data["msg"])
        
if __name__ == '__main__':
    unittest.main()