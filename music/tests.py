from django.test import TestCase
from django.core.cache import cache
from rest_framework.test import APITestCase
from rest_framework import status

class MusicDiscoveryComprehensiveTests(APITestCase):

    def setUp(self):
        """Set up initial mock data for testing dependent endpoints."""
        self.user_data = {
            "name": "Rutuja Kenjalkar",
            "email": "rutuja@example.com",
            "favorite_genres": ["pop", "rock"],
            "favorite_artists": ["Coldplay"],
            "moods": ["energetic"]
        }
        response = self.client.post('/users/', self.user_data, format='json')
        self.user_id = response.data.get('id', 1)
        self.non_existent_id = 99999

   
    def test_create_user_profile_proper(self):
        """Happy Path: Test creating a new user profile with valid data."""
        url = '/users/'
        data = {
            "name": "Alex Smith",
            "email": "alex@example.com",
            "favorite_genres": ["jazz"],
            "favorite_artists": ["Miles Davis"],
            "moods": ["chill"]
        }
        response = self.client.post(url, data, format='json')
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_201_CREATED])

    def test_create_user_profile_improper(self):
        """Negative Path: Test creating a user profile with missing/invalid fields."""
        url = '/users/'
        invalid_data = {
            "name": "",  # Empty name
            "email": "not-a-valid-email"  # Bad email format
        }
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_user_profile_proper(self):
        """Happy Path: Test retrieving an existing user profile."""
        url = f'/users/{self.user_id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('email'), self.user_data['email'])

    def test_get_user_profile_improper(self):
        """Negative Path: Test retrieving a user profile that does not exist."""
        url = f'/users/{self.non_existent_id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_refresh_recommendations_proper(self):
        """Happy Path: Test triggering a recommendation refresh for an existing user."""
        url = f'/recommendations/{self.user_id}/refresh/'
        response = self.client.post(url)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_202_ACCEPTED, status.HTTP_201_CREATED])

    def test_refresh_recommendations_improper(self):
        """Negative Path: Test refreshing recommendations for a non-existent user."""
        url = f'/recommendations/{self.non_existent_id}/refresh/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_get_recommendations_proper(self):
        """Happy Path: Test retrieving cached recommendations for a valid user."""
        cache_key = f"recommendations_{self.user_id}"
        # Seed mock tracks into Redis cache to simulate a completed background task
        mock_tracks = [{"track_name": "Yellow", "artist_name": "Coldplay"}]
        cache.set(cache_key, mock_tracks)

        url = f'/recommendations/{self.user_id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('source'), 'redis_cache')


    def test_get_recommendations_improper(self):
        """Negative Path: Test retrieving recommendations for a non-existent user."""
        url = f'/recommendations/{self.non_existent_id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_record_user_activity_proper(self):
        """Happy Path: Test recording a valid user interaction."""
        url = '/activity/'
        activity_data = {
            "user_id": self.user_id,
            "track_name": "Yellow",
            "artist_name": "Coldplay",
            "action": "play"
        }
        response = self.client.post(url, activity_data, format='json')
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_201_CREATED])

    def test_record_user_activity_improper(self):
        """Negative Path: Test recording an activity with missing fields or invalid user ID."""
        url = '/activity/'
        invalid_activity = {
            "user_id": 99999,  # Non-existent user
            "track_name": "",
            "action": "invalid_action_type"
        }
        response = self.client.post(url, invalid_activity, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_analytics_summary_proper(self):
        """Happy Path: Test retrieving overall platform analytics summary."""
        url = '/analytics/summary/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)




    def test_analytics_trends_proper(self):
        """Happy Path: Test retrieving trending genres or artists."""
        url = '/analytics/trends/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)



    def test_user_analytics_summary_proper(self):
        """Happy Path: Test retrieving a specific valid user's analytics summary."""
        url = f'/analytics/user/{self.user_id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_analytics_summary_improper(self):
        """Negative Path: Test retrieving analytics for a non-existent user."""
        url = f'/analytics/user/{self.non_existent_id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)