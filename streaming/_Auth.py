from tweepy import OAuthHandler
from streaming import twitter_dev_keys as K

class Auth():
    """
    Classe per autenticare le chiavi a twitter
    """
    def authenticate(self):
        auth = OAuthHandler(K.API_KEY, K.API_SECRET_KEY)
        auth.set_access_token(K.ACCESS_TOKEN, K.ACCESS_TOKEN_SECRET)
        return auth
