from rest_framework.throttling import SimpleRateThrottle

class LoginThrottle(SimpleRateThrottle):
    """
    Limite les tentatives de connexion
    """
    scope = 'login'
    rate = '5/minute'

class RegisterThrottle(SimpleRateThrottle):
    """
    Limite les tentatives d'inscription
    """
    scope = 'register'
    rate = '3/hour'

class APIThrottle(SimpleRateThrottle):
    """
    Limite générale pour l'API
    """
    scope = 'api'
    rate = '500/hour'