import unittest
import sys
import os


# 取得當前執行腳本的路徑
current_dir = os.path.dirname(os.path.abspath(__file__))
print(f"current_dir: {current_dir}")

# 構建相對路徑
relative_path = os.path.join(current_dir, '../demo1')
print(f"relative_path: {relative_path}")

# 將相對路徑加入 sys.path
sys.path.append(relative_path)

for path in sys.path:
    print(path)


from app import app
class Demo1TestCase(unittest.TestCase):
    def setUp(self) -> None:
        # 返回一個測試客戶端對象，可以用來模擬客戶端（瀏覽器）
        self.client = app.test_client()

    def test_hello(self):
        response = self.client.get('/')
        self.assertEqual("Hello, World!", response)