import requests,json
def transferToFembed(links:list):
    id = requests.post(
        "https://www.fembed.com/api/transfer",
        data={
            "client_id": '379944',
            "client_secret":"f5b3cfea094560e2",
            "links":json.dumps(links),
        },
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        ).json()["data"][0]
    return getURL(id)
def freeSlot(remove_id):
    return requests.post(
    "https://www.fembed.com/api/transferring",
    data={
        "client_id": '379944',
        "client_secret":"f5b3cfea094560e2",
        "remove_ids":json.dumps([remove_id,])
    },
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    ).json()
def getURL(id):
    resp = requests.post(
    "https://www.fembed.com/api/transferring",
    data={
        "client_id": '379944',
        "client_secret":"f5b3cfea094560e2",
        "task_id":id,
    },
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    ).json()
    for data in resp["data"]:
        if data["status"] == "Waiting for available server":
            return getURL(id)
        elif data["id"] == id and data["file_id"]:
            freeSlot(data["id"])
            return f'https://fembed.com/v/{data["file_id"]}'
if __name__ == "__main__":
    print(transferToFembed(["https://fembed-hd.com/v/y2zjdheggyd71kg",]))