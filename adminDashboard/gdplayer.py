from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
import requests
def get_ua():
    
    software_names = [SoftwareName.CHROME.value,SoftwareName.FIREFOX.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value,OperatingSystem.ANDROID.value]   
    
    user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)

    # Get Random User Agent String.
    user_agent = user_agent_rotator.get_random_user_agent()
    return user_agent
class GDPlayer:
    def __init__(self):
        self.base_url = "https://gdplayer.top/api/?id={url}"
    def request(self,url,auth):
        return requests.get(self.base_url.format(url=url),headers={"User-Agent":get_ua(),"Authorization":f"Basic {auth}"}).json()
    def get_slug(self,url,auth):
        return self.request(url,auth).get("key")
if __name__ == '__main__':
    print(GDPlayer().get_slug("https://www.fembed.com/v/qgl1-fee-e-nrry","c2hlYmFuZzpzaHV2cmFqbA=="))