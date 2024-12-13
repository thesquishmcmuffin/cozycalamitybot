import subprocess
import configparser
import json
import os
import twitchio
import asyncio
from twitchio.ext import pubsub
from twitchAPI.pubsub import PubSub
from twitchAPI.twitch import Twitch
from twitchAPI.helper import first
from twitchAPI.type import AuthScope
from twitchAPI.oauth import UserAuthenticator
import asyncio
from pprint import pprint
from uuid import UUID
import authorize as auth
import launch_ui as updateUI

config = configparser.ConfigParser()
config.read('config/config.toml')

APP_ID = config.get('twitch.auth', 'client_id')
APP_SECRET = config.get('twitch.auth', 'client_secret')
USER_SCOPE = [AuthScope.CHANNEL_READ_REDEMPTIONS]
TARGET_CHANNEL = config.get('twitch.info', 'channel_id')

with open('tokens/token_bot.json') as f:
    config = json.load(f)

token = config['access_token']

hydration_level = 0

async def callback_redeems(uuid: UUID, data: dict) -> None:
    print('got callback for UUID ' + str(uuid))
    pprint(data)
    title = data["data"]["redemption"]["reward"]["title"]

    print(title)  # Output: Hydrate!

    global hydration_level
    if title == "Hydrate!" :
        updateUI.draw_hydration_meter(hydration_level)
        print("adding water to the hydrate queue")
        hydration_level += 1
        print(hydration_level)

async def displayUI():
    display = subprocess.Popen(['python3', 'launch_ui.py'])
    await display.wait()

async def listener():
    # setting up Authentication and getting your user id
    twitch = await Twitch(APP_ID, APP_SECRET)
    auth = UserAuthenticator(twitch, [AuthScope.CHANNEL_READ_REDEMPTIONS], force_verify=False)
    token, refresh_token = await auth.authenticate()
    # you can get your user auth token and user auth refresh token following the example in twitchAPI.oauth
    await twitch.set_user_authentication(token, [AuthScope.CHANNEL_READ_REDEMPTIONS], refresh_token)
    user = await first(twitch.get_users(logins=[TARGET_CHANNEL]))

    # starting up PubSub
    pubsub = PubSub(twitch)
    pubsub.start()
    # you can either start listening before or after you started pubsub.
    #uuid = await pubsub.listen_whispers(user.id, callback_whisper)
    uuid = await pubsub.listen_channel_points(TARGET_CHANNEL, callback_redeems)

    asyncio.create_task(displayUI())

    input('press ENTER to close...')

    # you do not need to unlisten to topics before stopping but you can listen and unlisten at any moment you want
    await pubsub.unlisten(uuid)
    pubsub.stop()
    await twitch.close()

asyncio.run(listener())



