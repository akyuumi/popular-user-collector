import tweepy
from config import X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET, X_BEARER_TOKEN

class XService:
    def __init__(self):
        self.client = self._create_client()

    def _create_client(self):
        """Create and return a Twitter API client"""
        try:
            client = tweepy.Client(
                bearer_token=X_BEARER_TOKEN,
                consumer_key=X_API_KEY,
                consumer_secret=X_API_SECRET,
                access_token=X_ACCESS_TOKEN,
                access_token_secret=X_ACCESS_TOKEN_SECRET
            )
            return client
        except Exception as e:
            print(f"Error creating X API client: {str(e)}")
            return None

    def get_user_info(self, username):
        """
        Get user information including bio from X (Twitter)
        
        Args:
            username (str): The X username to fetch information for
            
        Returns:
            dict: User information including bio, followers count, following count, and tweet count
        """
        try:
            if not self.client:
                return None

            # Get user information
            user = self.client.get_user(
                username=username,
                user_fields=['description', 'public_metrics', 'created_at']
            )

            if not user.data:
                return None

            # Extract user data
            user_data = user.data
            metrics = user_data.public_metrics

            return {
                'username': username,
                'bio': user_data.description,
                'followers': metrics['followers_count'],
                'following': metrics['following_count'],
                'tweets': metrics['tweet_count'],
                'created_at': user_data.created_at.isoformat() if user_data.created_at else None
            }

        except Exception as e:
            print(f"Error fetching X user info: {str(e)}")
            return None 