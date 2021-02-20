
import discord
from random import getrandbits
import minimax as mm
import threading as th

#plus = ':heavy_plus_sign:'
#minus = ':heavy_minus_sign:'
#empty = ':orange_square:'
#
#
#up  = "⬆️"
#down = "⬇️"
#left = "⬅️"
#right = "➡️"
#dleft = "↙️"
#uleft = "↖️" 
#uright = "↗️" 
#dright = "↘️"
#center = "⏺️"
sandshit = "⏳"
check = "✅"


def board_to_string(board):
    out = ""
    for row in board:
        for i in row:
            if i == ' ': out += '   '
            elif i == 'X': out += ' X '
            elif i == 'O': out += ' O '
            out += '|'
        out = out[:-1]
        out += '\n-----------\n'
    return out[:-12]

class Michigame: 

    def __init__(self):
        self.ai = [-1,-1]
        self.ai = [-1,-1]
        self.player = [-1,-1]           
        self.board = [[' ',' ',' '],
                      [' ',' ',' '],
                      [' ',' ',' ']]
        self.current_user = -1
        self.current_guild = -1
        self.turn = bool(getrandbits(1)) ### turn 1 ai turn -1 player
        self.flag = False
        self.last_msg = -1
        self.reset_count = 0
        self.player = [-1,-1]           
        self.board = [[' ',' ',' '],
                      [' ',' ',' '],
                      [' ',' ',' ']]
    def reset_atr(self):
        self.ai = [-1,-1]
        self.player = [-1,-1]           
        self.board = [[' ',' ',' '],
                      [' ',' ',' '],
                      [' ',' ',' ']]
        self.current_user = -1
        self.current_guild = -1
        self.turn = bool(getrandbits(1)) ### turn 1 ai turn -1 player
        self.flag = False
        self.last_msg = -1
        self.reset_count = 0
        return

    async def send_text(self, message):
        if message.content.startswith('!RESET!'):
            if self.current_user != -1:
                await message.channel.send("<@!" + str(self.current_user) + "> me van a reiniciar, welve")
                self.reset_count += 1
                if self.reset_count > 1:
                    await message.channel.send("Bueno parece que <@!" + str(self.current_user) + "> me abandonó :(")
                    self.reset_atr()

        if message.content.startswith('MICHIRESET'):
            await message.channel.send("Reseteando Ga")
            self.reset_atr()
            return
            
        if message.content.startswith('MICHISOR') or (self.flag and len(message.content) < 5):
            if message.content.startswith('MICHISOR') and self.current_user != -1:
                if message.author.id == self.current_user: return
                else: await message.channel.send("Estoy jugando con <@!" + str(self.current_user) + ">")
                return
            if self.flag:
                self.player = [int(x) for x in message.content.split()]
                if mm.valid_move(self.board,self.player): 
                    self.board[self.player[0]][self.player[1]] = 'X'
                    if mm.check_winner(self.board) == (False, 0):
                        header = "Te has movido a " + str(self.player) 
                        output = "```\n"
                        output += board_to_string(self.board)
                        output += "```"
                        embedVar = discord.Embed(title=header, description=output, color=0x00ff00)
                        embedVar.add_field(name="EMPATARON PORQUE NADIE LE GANA AL MICHISOR", value="noob", inline=False)
                        self.last_msg = await message.channel.send(embed=embedVar)
                        self.reset_atr()     
                        return
                else: 
                    if mm.check_winner(self.board) == (False, 0):
                        await message.channel.send("EMPATARAON PORQUE NADIE LE GANA AL MICHISOR")
                        self.reset_atr()
                    return

            if not self.flag: 
                    self.flag = False
                    self.turn = bool(getrandbits(1))
                    header = "Es el turno de michisor" if self.turn != 1 else "Es tu turno" 
                    header += "\nTienes que enviar [fila] [columna]" if self.turn == 1 else ""
                    output = "```\n"
                    output += board_to_string(self.board)
                    output += "```"
                    embedfirst = discord.Embed(title=header, description=output, color=0x00ff00)
                    if self.turn == 1: await message.channel.send(embed=embedfirst)

            while mm.check_winner(self.board)[0]:
                self.current_user = message.author.id
                self.current_guild = message.guild.id
                if self.turn:
                        if not self.flag:
                                self.flag = True
                                return
                        self.flag = False
                else:
                        self.ai = mm.get_best_move(self.board)
                        if mm.valid_move(self.board,self.ai): 
                                self.board[self.ai[0]][self.ai[1]] = 'O'
                        else: self.turn = not self.turn
                
                
                w = mm.check_winner(self.board)
                self.turn = not self.turn
                header = {True:"Michisor se ha movido a " + str(self.ai), False: "Te has movido a " + str(self.player)}[self.turn == 1] 
                output = "```\n"
                output += board_to_string(self.board)
                output += "```"
                embedVar = discord.Embed(title=header, description=output, color=0x00ff00)
                if w[0] == False: 
                    header2 = "EMPATARON PORQUE NADIE LE GANA AL MICHISOR"
                    if w[1] == -1: header2 = "Ganó el michisor GAAAA" 
                    elif w[1] == 1: header2 = "WTF está mal el codigo"
                    embedVar.add_field(name=header2, value="noob", inline=False)
                else:
                    if self.turn == 1:
                        embedVar.add_field(name = "Te toca, muebete gaaa", value="Toy cargando " + sandshit, inline=False)
                    if self.turn == -1:
                        embedVar.add_field(name = "Le toca al Michi", value="Ta pensando mi bb", inline=False)
                self.last_msg = await message.channel.send(embed=embedVar)

                if self.turn == 1:
                    embedVar.insert_field_at(0, name = "Te toca, muebete gaaa", value= "Tienes que enviar [fila] [columna] " + check, inline=False)
                    embedVar.remove_field(1)
                    await self.last_msg.edit(embed=embedVar)

                if w[0] == False:
                    embedVar.insert_field_at(0, name = "Ha terminado el juego", value=mm.print_winner(w[1]) + "Nub", inline=False)
                    embedVar.remove_field(1)
                    await self.last_msg.edit(embed=embedVar)
                    self.current_user = -1
                    self.current_guild = -1
                    self.being_michi = False        
                    self.reset_atr()
                    return


