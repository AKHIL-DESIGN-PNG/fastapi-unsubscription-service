import unittest
import requests

BASE_URL = "http://127.0.0.1:8000"  

class TestAPIEndpoints(unittest.TestCase):
    """Test suite for API endpoints"""

    def test_unsubscribe_email_endpoint(self):
        """Test the /unsubscribe/unsubscribe-email POST endpoint for expected 404"""
        response = requests.post(
            BASE_URL + "/unsubscribe/unsubscribe-email",
            json={
                "username": "test",
                "email": "test@example.com",
                "reason": "test"
            }
        )
        self.assertEqual(
            response.status_code, 404,
            f"Expected 404, but got {response.status_code}. Response: {response.text}"
        )

    def test_subscriptions_list_endpoint(self):
        """Test the /subscriptions/list GET endpoint for expected 404"""
        response = requests.get(BASE_URL + "/subscriptions/list")
        self.assertEqual(
            response.status_code, 404,
            f"Expected 404, but got {response.status_code}. Response: {response.text}"
        )

    def test_unsubscribed_users_endpoint(self):
        """Test the /unsubscribed-users GET endpoint for expected 404"""
        response = requests.get(BASE_URL + "/unsubscribed-users")
        self.assertEqual(
            response.status_code, 404,
            f"Expected 404, but got {response.status_code}. Response: {response.text}"
        )

    def test_search_endpoint(self):
        """Test the /search GET endpoint for expected 404"""
        response = requests.get(BASE_URL + "/search")
        self.assertEqual(
            response.status_code, 404,
            f"Expected 404, but got {response.status_code}. Response: {response.text}"
        )

    def test_unsubscribe_email(self):
        """Test the unsubscribe email endpoint with valid data"""
        test_data = {
            "username": "test_user",
            "email": "test@example.com",
            "reason": "too many emails",
            "comments": "please unsubscribe me"
        }

        response = requests.post(
            BASE_URL + "/unsubscribe/unsubscribe-email",
            json=test_data
        )

        self.assertLess(
            response.status_code, 500,
            f"Unsubscribe endpoint returned server error: {response.status_code}"
        )

        if response.status_code < 400:
            response_data = response.json()
            self.assertIn("message", response_data)
            self.assertIn("data", response_data)
            self.assertEqual(response_data["data"]["username"], test_data["username"])
            self.assertEqual(response_data["data"]["email"], test_data["email"])

if __name__ == "__main__":
    unittest.main()
