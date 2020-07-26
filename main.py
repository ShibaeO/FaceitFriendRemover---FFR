import asyncio
import aiohttp
import json
from colorama import Fore, Back, Style, init

name = ""  # Face it nickname
userId = ""  # Face it userId
cookie = ""  # Face it session cookie

headers = {
    "authority": "api.faceit.com",
    "accept": "application/json",
    "userid": f"{userId}",
    "faceit-referer": "new-frontend",
    "authorization": "",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
    "dnt": "1",
    "origin": "https://api.faceit.com",
    "sec-fetch-site": "same-origin",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "referer": "https://api.faceit.com/proxy.html",
    "cookie": f"{cookie}",
}


async def remove(friendId, userId):

    unfriendUrl = f"https://api.faceit.com/core/v1/users/{userId}/friends/{friendId}"
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.delete(unfriendUrl) as response:
                a = await response.text()
                if response.status == 200:
                    return f"You successfully removed your friend {Fore.GREEN}{friendId}{Style.RESET_ALL}"
                elif response.status == 500:
                    return f"Request Error : {response.status} | Failed to unfriend {Fore.RED}{friendId}{Style.RESET_ALL}"
    except:
        return "request Error"


async def getFriends(nickname):

    unfriendUrl = f"https://api.faceit.com/core/v1/nicknames/{nickname}"

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(unfriendUrl) as response:
            a = await response.text()
            return a, response.status


async def main():
    totalFriends = []
    a = await getFriends(name)
    if a[1] == 200:
        data = json.loads(a[0])
        for i in data["payload"]["friends_ids"]:
            a = await remove(i, userId)
            print(a)
            totalFriends.append(i)
            await asyncio.sleep(3)
    elif a[1] == 500:
        print("failed")
    print(f"[+]     Operation terminated, successfully removed : {Fore.GREEN}{len(totalFriends)}{Style.RESET_ALL} ")


if __name__ == "__main__":
    init()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
