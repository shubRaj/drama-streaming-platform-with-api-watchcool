import requests
def getSource(id):
    return requests.get(f"https://api.asiaflix.app/api/v2/utility/get-stream-links?url=https://embed.watchasian.to/ajax.php?id={id}").json()
if __name__ == '__main__':
    print(getSource("Mjc4MjEy"))