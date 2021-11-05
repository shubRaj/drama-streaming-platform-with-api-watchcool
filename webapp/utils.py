import requests
from .models import Configuration
def verifyCaptcha(response:str) -> bool:
    config = Configuration.objects.filter(id=1)
    if config.exists():
        secret_key = config.first().recaptcha_secret_key
        resp = requests.post("https://www.google.com/recaptcha/api/siteverify",data={
            "secret":secret_key,
            "response":response
        }).json()
        return resp["success"]