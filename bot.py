from game import *
from token import token
token = token
import numpy as np
length = 100
class Michisor(discord.Client):
        def __init__(self):
            super().__init__()
            self.games = [[] for _ in range(length)]

        async def on_ready(self):
                print('Logged on as', self.user)

        async def on_message(self, message):
            if message.author == self.user:
                return

            gid = message.guild.id
            gpos = gid % length
            glist = [x[0] for x in self.games[gpos]]
            if gid not in glist:
                if message.content.startswith("MICHISOR"):
                    self.games[gpos].append((gid, Michigame()))
                    await self.games[gpos][-1][1].send_text(message)
                    return
                else:
                    return
            gkey = glist.index(gid)
            await self.games[gpos][gkey][1].send_text(message) 
            
            
            
            

jhonny = Michisor()
jhonny.run(token)
