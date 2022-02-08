#  Copyright (c) 2022 @iAruack
# Telegram Ban All Bot 
# Creator - Aruak

import logging
import re
import os
import sys
import asyncio
from telethon import TelegramClient, events
import telethon.utils
from telethon.tl import functions
from telethon.tl.functions.channels import LeaveChannelRequest
from asyncio import sleep
from telethon.tl.types import ChatBannedRights, ChannelParticipantsAdmins, ChatAdminRights
from telethon.tl.functions.channels import EditBannedRequest
from datetime import datetime
from config import config


logging.basicConfig(level=logging.INFO)

print("Starting.....")

Ar = TelegramClient('Ar', config.API_ID, config.API_HASH).start(bot_token=config.BOT_TOKEN)


SUDO_USERS = []
for x in config.SUDO: 
    SUDO_USERS.append(x)

@Ar.on(events.NewMessage(pattern="^/ping"))  
async def ping(e):
    if e.sender_id in SUDO_USERS:
        start = datetime.now()
        text = "Pong!"
        event = await e.reply(text, parse_mode=None, link_preview=None )
        end = datetime.now()
        ms = (end-start).microseconds / 1000
        await event.edit(f"**I'm On** \n\n __Pong__ !! `{ms}` ms")


@Ar.on(events.NewMessage(pattern="^/banall"))
async def testing(event):
  if event.sender_id in SUDO_USERS:
   if not event.is_group:
        Reply = f"Noob !! Use This Cmd in Group."
        await event.reply(Reply, parse_mode=None, link_preview=None )
   else:
       await event.delete()
       Aruack = await event.get_chat()
       Aruackop = await event.client.get_me()
       admin = Aruack.admin_rights
       creator = Aruack.creator
       if not admin and not creator:
           await event.reply("I Don't have sufficient Rights !!")
           return
       await event.reply("hey !! I'm alive")
       everyone = await event.client.get_participants(event.chat_id)
       for user in everyone:
           if user.id == Aruackop.id:
               pass
           try:
               await event.client(EditBannedRequest(event.chat_id, int(user.id), ChatBannedRights(until_date=None,view_messages=True)))
           except Exception as e:
               await event.edit(str(e))
           await sleep(0.3)


@Ar.on(events.NewMessage(pattern="^/leave"))
async def _(e):
    if e.sender_id in SUDO_USERS:
        Aruack = ("".join(e.text.split(maxsplit=1)[1:])).split(" ", 1)
        if len(e.text) > 7:
            bc = Aruack[0]
            bc = int(bc)
            text = "Leaving....."
            event = await e.reply(text, parse_mode=None, link_preview=None )
            try:
                await event.client(LeaveChannelRequest(bc))
                await event.edit("Succesfully Left")
            except Exception as e:
                await event.edit(str(e))   
        else:
            bc = e.chat_id
            text = "Leaving....."
            event = await e.reply(text, parse_mode=None, link_preview=None )
            try:
                await event.client(LeaveChannelRequest(bc))
                await event.edit("Succesfully Left")
            except Exception as e:
                await event.edit(str(e))   
          


@Ar.on(events.NewMessage(pattern="^/restart"))
async def restart(e):
    if e.sender_id in SUDO_USERS:
        text = "__Restarting__ !!!"
        await e.reply(text, parse_mode=None, link_preview=None )
        try:
            await Ar.disconnect()
        except Exception:
            pass
        os.execl(sys.executable, sys.executable, *sys.argv)
        quit()


print("\n\n")
print("Bot Started")

Ar.run_until_disconnected()
