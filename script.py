import json
import urllib
import urllib.request
import time
import asyncio
import json

env_file = open(".env.json")
env = json.load(env_file)
BUSY_SERVER_URL = env["BUSY_SERVER_URL"]
LAZY_SERVER_URL = env["LAZY_SERVER_URL"]
env_file.close()

async def call_api(url, prefix):
    req = urllib.request.Request(url)
    try:
        response = urllib.request.urlopen(req)
        result = response.read()
        print(prefix, result)
        return result
    except urllib.error.HTTPError as error:
        print(prefix, "The request failed with status code: " + str(error.code))
        print(prefix, error.info())
        print(prefix, json.loads(error.read()))
        return error.info()


async def run():
    count = 0
    WAIT_INTERVAL = 6
    while count * WAIT_INTERVAL <= 7200:
      task1 = asyncio.create_task(call_api(BUSY_SERVER_URL, 'busy'))
      if count % 10 == 0:
        task2 = asyncio.create_task(call_api(LAZY_SERVER_URL, 'lazy'))
        await task2
      await task1
      time.sleep(WAIT_INTERVAL)
      count += 1
        

asyncio.run(run())
