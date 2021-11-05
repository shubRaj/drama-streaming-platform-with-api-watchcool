import aiohttp
import asyncio
import json
import urllib.parse
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from bs4 import BeautifulSoup
import re
import base64
from operator import itemgetter
def get_ua():
    
    software_names = [SoftwareName.CHROME.value,SoftwareName.FIREFOX.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value,OperatingSystem.ANDROID.value]   
    
    user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)

    # Get Random User Agent String.
    user_agent = user_agent_rotator.get_random_user_agent()
    return user_agent
class PlayDrive:
    def __init__(self,api_key=None):
        self.api_key = api_key
        self.BASE_URL = f"https://player.watchcool.in/api/v1/?api_key={api_key}&link="
    def parse(self,content):
        soup = BeautifulSoup(content,"html.parser")
        return soup
    async def request(self,url,headers:dict=None,get="text"):
        if not headers:
            headers = {
                "User-Agent":get_ua()
                }
        headers["Accept"]="text/html" if get=="text" else "application/json"
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    if get=="text":
                        return await resp.text()
                    else:
                        try:
                            data= await resp.json()
                        except Exception as e:
                            data = json.loads(await resp.text())
                        finally:
                            return data
    
    async def getDirectLinks(self,url):
        content = await self.request(url)
        soup = self.parse(content)
        scripts = soup.find("body").find_all("script")
        for script in scripts:
            if script.text.strip().startswith('$("#generate")'):
                links = [ base64.b64decode(f'{link.split("/")[-1]}=='.encode("ascii")).decode('ascii') for link in re.findall("/[\w/]{30,}",script.text.strip())]
                direct_links = []
                for link in links:
                    direct_links.append({
                        "link":link,
                        "quality":link.split("/")[-2],
                    })
                return direct_links
    async def getLinks(self,source):
        data = await self.upload(source)
        if data:
            slug = data.get("slug")
            if slug:
                download_link = data.get("download_link")
                title =  data.get("title")
                source = data.get("source")
                direct_links = await self.getDirectLinks(download_link)
                return {"slug":slug,"source":source,"title":title,"direct_links":direct_links}
    async def upload(self,source):
        url = f"{self.BASE_URL}{source}"
        data = await self.request(url,get="json")
        return data.get("data")
if __name__ == '__main__':
    print(asyncio.run(PlayDrive("bW92aWVzcXVpY2XubmV0QPdtYWlsLmNvbS0xNDg4Mw").getDirectLinks("https://player.watchcool.in/d/IUx1mlffgrKLcZJ/")))