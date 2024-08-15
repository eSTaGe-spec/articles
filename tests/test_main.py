import unittest
from fastapi.testclient import TestClient

from app.main import app


class TestUserCreate(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_create_user(self):
        data = {'username': 'testUser', 'password': '123'}
        response = self.client.post('/register', json=data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['username'], 'testUser')


class TestUserCreateWith422Error(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_create_user(self):
        data = {'username': 'admin_1', 'password': '123'}
        response = self.client.post('/register', json=data)

        self.assertEqual(response.status_code, 422)


if __name__ == '__main__':
    unittest.main()