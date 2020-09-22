import discord
import os
import random
import json
import shelve
import time
import shutil
import asyncio
from game_module import *
from discord.ext import commands

##Setting up the bot##

client = commands.Bot(command_prefix = "cae ")
Token = "NzQ2MzA3MDAzNjMwMDkyMzI4.Xz-ajw.MhiQl8TNfcHVy7ZHonO7OIMOkGA"

@client.event         #Checking a bot if it's online
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game("cae help"))
    print("bot is ready")
client.remove_command("help")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error,discord.ext.commands.CommandNotFound):
        embed = discord.Embed(
            title="Commmand doesn't exist",
            colour=discord.Color.red())
        await ctx.send(embed=embed)
        return
    raise error

##Creating a help command##
@client.command()
async def help(ctx):
    embed = discord.Embed(color=discord.Color.orange())

    embed.set_author(name="Non-combat commands:")
    embed.add_field(name="introduce", value="Get to know the bot.", inline=False)
    embed.add_field(name="how", value="How to play the game.", inline=False)
    embed.add_field(name="begin", value="Register yourself to the game.",inline=False)
    embed.add_field(name="buy [character id; e.g. 001]", value="Buy a character.", inline=False)
    embed.add_field(name="inv", value="See your inventory.")
    embed.add_field(name="des [character id; e.g. 001]", value="See the description of a character", inline=False)
    embed.add_field(name="select [1st character id] [2nd character id] [3rd character id]",
                    value="Select three characters in your inventory into your team.", inline=False)
    embed.add_field(name="team", value="See the selected members or your current team",inline=False)

    embed0 = discord.Embed(colour=discord.Color.orange())

    embed0.set_author(name="Combat commands:")
    embed0.add_field(name="fight [username; e.g. @user]", value="Mention a user you want to challenge", inline=False)
    embed0.add_field(name="accept", value="Accepts the awaiting fight request.", inline=False)
    embed0.add_field(name="deny", value="Denies the awaiting fight request", inline=False)
    embed0.add_field(name="turn [position of ally character on ally team; e.g. 1]"
                          " [position of enemy character on enemy team; e.g. 1]", value="Initiate your turn.", inline=False)
    embed0.add_field(name="surrender", value="Surrenders the current battle you are in.", inline=False)


    await ctx.send(embed=embed)
    await ctx.send(embed =embed0)

##########################################################Bot is finished setting up here##

##Important strings. Stored for easy manipulation##
pls_register_first = ("Please begin the game first by using \"cae begin\".")
bot_intro = ("I am a bot created by the almighty Ninroot_Eater#8390. I am written in Python.\n\n"
             "More about me:\n"
             "I am a game bot set in a school called CAE (the school that Ninroot attended). "
             "The characters in the game are either teachers or students in that school.\n\n "
             "My command prefix is \"cae \"."
             " Make sure that you put a space after that!")
not_in_battle = "You are not in a battle. Please start one by using 'cae fight [username]'."
not_on_turn = "It's not your turn yet."

##Main bot commands##

@client.command()
async def introduce(ctx):
    #The introduction command for the bot
    embed = discord.Embed(
        description=(bot_intro),
        colour=discord.Color.dark_blue())
    await ctx.send(embed= embed)

##Important functions. Stored for easy manipulation##
##The function for checking if a player has already registered##
def started(msg_auth):
    if os.path.exists(f"Player databases\\{msg_auth.id}"):
        return True
    return False

def identical_present(lst):
    if len(lst) == len(set(lst)):
        return False
    return True

def can_afford(player:Player, item:Character):
    if int(player.gold) >= int(item.cost):
        return True
    return False
def lst_empty(lst):
    for i in lst:
        if i is None:
            return True
    return False


def check(author, check_list):
    def inner_check(message):
        return message.author == author and message.content in check_list

    return inner_check

def lose(fattk, fdefn):
    tem1 = fattk['inv']
    tem2 = fdefn['inv']

    tem1.in_battle = False
    tem2.in_battle = False

    tem1.on_turn = False
    tem2.on_turn = False

    tem1.battle_with['key'] = None
    tem2.battle_with['key'] = None

    tem1.p = None
    tem2.p = None

    tem1.first_turn = True
    tem2.first_turn = True

    fattk['inv'] = tem1
    fdefn['inv'] = tem2


##Creating a dedicated save file for a user##
@client.command()
async def begin(ctx):
    msg_auth = ctx.message.author  ##Denying to create the file again if it's already been existing##
    if started(msg_auth):
        embed = discord.Embed(
            title=("You have already started the game."),
            colour=discord.Color.red())
        await ctx.send(embed=embed)


    else:
        os.makedirs(f"Player databases\\{msg_auth.id}")
        with shelve.open(f"Player databases\\{msg_auth.id}\\playerinv") as f:
            f["inv"] = Player(f"{msg_auth.id}")
            f["name"] = (f"{msg_auth.name}")
            embed = discord.Embed(
                title=("Your journey begins!"),
                colour=discord.Color.green())
            await ctx.send(embed=embed)



##Buying a character##
@client.command()
async def buy(ctx, idx):
    msg_auth = ctx.message.author


    if not started(msg_auth):   ##Checking if the user has registered or not##
            embed = discord.Embed(
                description=(pls_register_first),
                colour=discord.Color.red())
            await ctx.send(embed=embed)

    else:
            with shelve.open(f"Player databases\\{msg_auth.id}\\playerinv") as f:  ##Checking if the user has enough gold##
                affordobility = can_afford(f["inv"], Character.dict_of_cha[idx])
                if affordobility == False:
                    embed = discord.Embed(
                    description=("You do not have enough gold to purchase this character."),
                    colour=discord.Color.red())
                    await ctx.send(embed=embed)

                elif idx in list(f["inv"].cha_dict.keys()): ##checking if the user has already owned the character##
                    embed = discord.Embed(
                    title=("You already own this character."),
                    colour=discord.Color.red())
                    await ctx.send(embed=embed)

                else:

                    tem = f["inv"]
                    tem.gold = int(tem.gold) - int((Character.dict_of_cha[idx]).cost)
                    tem.cha_dict[Character.dict_of_cha[idx].id] = (Character.dict_of_cha[idx])
                    f["inv"] = tem
                    await ctx.send("Character successfully bought.")

                    embed = discord.Embed(
                    title=(Character.dict_of_cha[idx].name),
                    description=(Character.dict_of_cha[idx].description()),
                    color=discord.Color.blue())
                    file = discord.File(f"images\\{Character.dict_of_cha[idx].image_file}",
                    filename=Character.dict_of_cha[idx].image_file)
                    embed.set_image(url=f"attachment://{Character.dict_of_cha[idx].image_file}")
                    await ctx.send(file=file, embed=embed)
                    await ctx.send(f"Your gold: {f['inv'].gold}")
                    print(f["inv"].cha_dict)

##Character description command##

@client.command()
async def des(ctx, idx):
    embed = discord.Embed(
        title=(Character.dict_of_cha[idx].name),
        description=(Character.dict_of_cha[idx].description()),
        color=discord.Color.dark_blue()
    )
    file = discord.File(f"images\\{Character.dict_of_cha[idx].image_file}", filename=Character.dict_of_cha[idx].image_file)
    embed.set_image(url=f"attachment://{Character.dict_of_cha[idx].image_file}")
    await ctx.send(file = file,embed= embed)

##Explaining the game's concepts##
@client.command()
async def how(ctx):
    embed = discord.Embed(
        title="How to Play",color=discord.Color.orange())
    embed.add_field(name="Overview",value="This is a multiplayer turn-based strategy game."
                                          "And is very similar to the Teamfight Tactics gamemode of the MOBA game"
                                          "League of Legends. You would have to make a team of three from a large variety"
                                          "of 'character'.", inline=False)
    embed.add_field(name="Preparation", value="When you started out the game, 40 gold will be automatically given."
                                              " You can use this gold to buy characters which cost 10 gold each. After"
                                              " buying your desired characters, you will have to make a team. A team must"
                                              " consists of at least 3 characters. If you win a multiplayer game, you "
                                              "will be awarded with 10 gold. Make sure to spend those golds wisely. ")
    embed.add_field(name="Combat Mechanics", value="Each game consists of ten rounds. After each round, the player must"
                                                   "choose one out of three randomly generated characters and add to his"
                                                   "team. During the battle phase, a player team's can contain as much as"
                                                   "8 characters including the original three. At the end of the final round,"
                                                   "the hp of all the members of each team would be added. The team with"
                                                   " the higher hp score will become the winner.", inline=False)
    embed.add_field(name="Synergies", value="Synergies play a big role in this game. Currently, a total of 6 'Personalities'"
                                            " and 6 'Appearances' are present in the game. When you have 2 or 3 characterss"
                                            " with the same synergies, you will get the synergy bonuses. Choosing the right"
                                            "characters with right synergies is the key to victory. You can learn more about"
                                            " synergies and their bonuses in the character descriptions.", inline=False)
    await ctx.send(embed = embed)

##Making a command that returns author's inventory##
@client.command()
async def inv(ctx):
    msg_auth = ctx.message.author  ##Checking if the user has started the game or not##
    if not started(msg_auth):
        await ctx.send(pls_register_first)

    else:
        with shelve.open(f"Player databases\\{msg_auth.id}\\playerinv") as db:
            gold = db["inv"].gold
            embed = discord.Embed(
                colour=discord.Color.dark_gray(),
                title=f"Inventory of {msg_auth}",
                description=f"Your gold = {gold}"
            )
            embed.add_field(name="These are your characters. Use \"cae buy\" to buy more.",
                            value="###################################", inline=False)
            for k in db["inv"].cha_dict.values():
                embed.add_field(name=f"{k.name}", value=f"Character id = {k.id}\n({k.first_attr}, {k.second_attr})", inline=False)
            embed.add_field(name=db["inv"].cha_num(), value="###########",inline=False)

            await ctx.send(embed=embed)

@client.command()
async def select(ctx,idx1,idx2,idx3):
    input_list = [idx1, idx2, idx3]
    msg_auth = ctx.message.author
    cha_owned = True
    with shelve.open(f"Player databases\\{msg_auth.id}\\playerinv") as f:
        for i in input_list:
            if i not in (f["inv"].cha_dict.keys()):
                cha_owned = False
    id_present = identical_present(input_list)

    if not started(msg_auth):   ##Checking if the user has started the game or not##
        embed = discord.Embed(
            description=(pls_register_first),
            colour=discord.Color.red())
        await ctx.send(embed=embed)
    elif cha_owned == False:
        embed = discord.Embed(
            title="Please select only the characters you owned.",
            color=discord.Colour.red())
        await ctx.send(embed = embed)

    elif id_present == True:    ##Checking if a character is present multiple time in the team##
        embed = discord.Embed(
            title="You cannot choose the same character multiple times.",
            color=discord.Colour.red())
        await ctx.send(embed=embed)

    elif cha_owned == True and id_present == False:  ##This condition is met only if the user chooses owned characters
                                                     ##and if all members are unique##

        with shelve.open(f"Player databases\\{msg_auth.id}\\playerinv") as f:
            tem = f["inv"]

            for i in [1,2,3]:
                tem.selected_cha[str(i)] = Character.dict_of_cha[input_list[i-1]]
            f["inv"] = tem
            embed = discord.Embed(title=f"{msg_auth.name}'s team consists of:",
                color=discord.Color.gold())

            count = 1
            for v in f["inv"].selected_cha.values():
                embed.add_field(name=f"{count}. {v.name}",
                                value=f"character id = {v.id}\ngender = {v.gender}\nhp = {v.hp}")

                count += 1
            await ctx.send(embed=embed)

@client.command()
async def team(ctx):   ##Displaying one's team##
    msg_auth = ctx.message.author
    if started(msg_auth):
        with shelve.open(f"Player databases\\{msg_auth.id}\\playerinv") as f:
            if lst_empty(f["inv"].selected_cha.values()):
                    embed = discord.Embed(
                        title=("Please select members for our team first by using\"cae select\"."),
                        color=discord.Color.red())
                    await ctx.send(embed=embed)

            elif f['inv'].in_battle == True:
                with shelve.open(f"battle_files\\{int(f['inv'].battle_with['key'].name) + int(msg_auth.id)}\\combat") as btf:

                    embed = discord.Embed(title=f"{msg_auth.name}'s battle-team consists of:",
                                          color=discord.Color.gold())

                    count = 1
                    for v in btf[str(f['inv'].p)].values():
                        embed.add_field(name=f"{count}. {v.name}",
                                        value=f"character id = {v.id}\ngender = {v.gender}\n\n"
                                              f"({v.first_attr}, {v.second_attr})\n\n"
                                              f"hp = {v.hp}\nattack = {v.attk}\ndefense = {v.defn}")

                        count += 1
                    await ctx.send(embed=embed)



            else:
                embed = discord.Embed(title=f"{msg_auth.name}'s team consists of:",
                                          color=discord.Color.gold())

                count = 1
                for v in f["inv"].selected_cha.values():
                    embed.add_field(name=f"{count}. {v.name}",
                                        value=f"character id = {v.id}\ngender = {v.gender}\n\n"
                                              f"({v.first_attr}, {v.second_attr})\n\n"
                                              f"hp = {v.hp}\nattack = {v.attk}\ndefense = {v.defn}")

                    count += 1
                await ctx.send(embed=embed)

    else:
        embed = discord.Embed(
            title=(pls_register_first),
            colour=discord.Color.red())
        await ctx.send(embed=embed)

@client.command()
async def set_gold(ctx, gold:int):
    msg_auth = ctx.message.author
    with shelve.open(f"Player databases\\{msg_auth.id}\\playerinv") as f:
        tem = f["inv"]
        tem.gold = gold
        f["inv"] = tem
        await ctx.send(f["inv"].gold)

@client.command()
async def fight(ctx, defender:discord.User):
    msg_auth = ctx.message.author

    if str(msg_auth.name) == f"{defender.name}":
        await ctx.send(embed= discord.Embed(
            title="You cannot battle yourself.",
            color=discord.Color.red()))

    elif started(msg_auth) and started(defender):
        fattk = shelve.open(f"Player databases\\{msg_auth.id}\\playerinv")
        fdefn = shelve.open(f"Player databases\\{defender.id}\\playerinv")
        if lst_empty(fattk["inv"].selected_cha.values()) or lst_empty(fdefn["inv"].selected_cha.values()):
            embed = discord.Embed(
                title=("Team error"),
                description="Either you or the user you are trying to battle "
                            "hasn't selected characters for the battle team yet.",
                colour=discord.Color.red())
            await ctx.send(embed=embed)
        elif fdefn["inv"].in_battle:
            await ctx.send(embed = discord.Embed(
                title=f"{defender.name} is currently in another battle.",
                color=discord.Color.red()))

        elif fattk['inv'].in_battle == True:
            await ctx.send(embed = discord.Embed(
                title=f"You are currently in another battle.",
                color=discord.Color.red()))

        else:
            tam1 = fdefn["inv"]
            tam1.challenger["key"] = fattk["inv"]
            fdefn["inv"] = tam1

            embed = discord.Embed(
                title=f"Fight request from {msg_auth.name}.",
                color=discord.Color.orange(),
                description=f"{defender.mention}, do you accept? Or are you a lil b#$!*# ?"
            )
            await ctx.send(embed = embed)

        fattk.close()
        fdefn.close()

    else:
        embed = discord.Embed(
            title=("Resgisration error"),
            description="Either you or the user you are trying to battle "
                        "hasn't registered for the game yet.",
            colour=discord.Color.red())
        await ctx.send(embed=embed)

@client.command()
async def accept(ctx):
    msg_auth = ctx.message.author
    fdefn = shelve.open(f"Player databases\\{msg_auth.id}\\playerinv")

    if fdefn["inv"].in_battle == True:
        await ctx.send(embed = discord.Embed(
            title="You are already in a battle.",
            color=discord.Color.red()
        ))

    elif fdefn["inv"].challenger["key"] == None :
        await ctx.send(f"You don't have any fight request to accept.")
        print(fdefn["inv"].challenger["key"])


    else:
        fattk = shelve.open(f"Player databases\\{fdefn['inv'].challenger['key'].name}\\playerinv")
        tem1 = fdefn["inv"]
        tem1.in_battle = True
        tem1.battle_with["key"] = fattk["inv"]
        tem1.first_turn = True
        tem1.p = 2
        tem1.challenger["key"] = None
        fdefn["inv"] = tem1

        tem2 = fattk["inv"]
        tem2.in_battle = True
        tem2.on_turn = True
        tem2.battle_with["key"] = fdefn["inv"]
        tem2.challenger["key"] = None
        tem2.p = 1
        tem2.first_turn = True
        fattk["inv"] = tem2

        if not os.path.exists(f"battle_files\\{int(fdefn['inv'].battle_with['key'].name) + int(fattk['inv'].battle_with['key'].name)}\\combat)"):
            os.makedirs(f"battle_files\\{int(fdefn['inv'].battle_with['key'].name) + int(fattk['inv'].battle_with['key'].name)}\\combat)")
            battle_file = shelve.open(f"battle_files\\{int(fdefn['inv'].battle_with['key'].name) + int(fattk['inv'].battle_with['key'].name)}\\combat")
            ct = 1
            battle_file["1"] = {}
            tem = battle_file['1']
            for i in fattk['inv'].selected_cha.values():
                tem[ct] = i
                ct+= 1

            battle_file['1'] = tem

            ct = 1
            battle_file["2"] = {}
            tem = battle_file['2']
            for i in fdefn['inv'].selected_cha.values():
                tem[ct] = i
                ct += 1

            battle_file['2'] = tem

            battle_file['turn_count'] = {}
            tam = battle_file['turn_count']
            tam['turn'] = 0
            battle_file["turn_count"] = tam


            battle_file.close()

        embed = discord.Embed(
            title=f"{msg_auth.name}  VS  {fattk['name']}",
            color=discord.Color.blurple())

        embed.add_field(name=f"{msg_auth.name}'s Team:", value="####", inline=False)
        count = 1

        for v in fattk["inv"].selected_cha.values():
            embed.add_field(name=f"{count}. {v.name}",
                            value=f"character id = {v.id}\ngender = {v.gender}\n\n"
                                  f"({v.first_attr}, {v.second_attr})\n\n"
                                  f"hp = {v.hp}\nattack = {v.attk}\ndefense = {v.defn}")
            count += 1

        embed.add_field(name=f"{fattk['name']}'s Team:", value="####", inline=False)
        count = 1

        for v in fdefn["inv"].selected_cha.values():
            embed.add_field(name=f"{count}. {v.name}",
                            value=f"character id = {v.id}\ngender = {v.gender}\n\n"
                                  f"({v.first_attr}, {v.second_attr})\n\n"
                                  f"hp = {v.hp}\nattack = {v.attk}\ndefense = {v.defn}")
            count += 1
        await ctx.send(embed=embed)

        fattk.close()
    fdefn.close()


@client.command()
async def deny(ctx):
    msg_auth = ctx.message.author
    fdefn = shelve.open(f"Player databases\\{msg_auth.id}\\playerinv")

    if fdefn["inv"].in_battle == True:
        await ctx.send(embed = discord.Embed(
            title=("You are already in a battle. Too late to deny."),
            colour=discord.Color.red()))

    elif fdefn["inv"].challenger["key"] == None:
        await ctx.send(embed = discord.Embed(
            title=("No fight request to deny."),
            colour=discord.Color.red()))
        print(fdefn["inv"].challenger["key"])

    else:
        tem = fdefn["inv"]
        tem.challenger["key"] = None
        fdefn["inv"] = tem
        await ctx.send(embed = discord.Embed(
            title=("Request denied."),
            colour=discord.Color.green()))
        print (fdefn["inv"].challenger["key"])
    fdefn.close()


##Combat commands##
@client.command()
async def turn(ctx, ally_cha, enemy_cha):
    msg_auth = ctx.message.author
    if started(msg_auth) == False:
        await ctx.send(embed = discord.Embed(title = (pls_register_first), colour = discord.Color.red())) ##Checking the user's registration##
    else:
        fattk = shelve.open(f"Player databases\\{msg_auth.id}\\playerinv")
        if fattk["inv"].in_battle == False:
            await ctx.send(embed = discord.Embed(title = (not_in_battle), color = discord.Color.red())) ##Checking if the user is in a battle or not##

        elif fattk["inv"].on_turn == False:
            await ctx.send(embed = discord.Embed(title = (not_on_turn), colour = discord.Color.red())) ##Checking if it's the user's turn or not##

        else:
            fdefn = shelve.open(f"Player databases\\{fattk['inv'].battle_with['key'].name}\\playerinv") ##All conditions were satisfied##
            battle_file = shelve.open(f"battle_files\\{int(fdefn['inv'].battle_with['key'].name) + int(fattk['inv'].battle_with['key'].name)}\\combat")

            attacker = (fattk['inv'].p)
            defender = (fdefn['inv'].p)  ##Opening appropriate files and start counting the turn_count##

            tem = battle_file['turn_count']
            tem["turn"] += 1
            battle_file['turn_count'] = tem


            if fattk['inv'].first_turn == True:
                tem = fattk['inv']
                tem.first_turn = False
                fattk['inv'] = tem


            if battle_file[str(attacker)][int(ally_cha)].status == "dead":  ##Checking if the target is dead or not##
                await ctx.send(embed=discord.Embed(
                    title="You cannot attack with a dead character.",
                    colour=discord.Color.red()))

            if battle_file[str(defender)][int(enemy_cha)].status == "dead":
                await ctx.send(embed=discord.Embed(
                    title="You cannot attack a dead character.",
                    colour=discord.Color.red()))

            else:

                if battle_file[str(attacker)][int(ally_cha)].attk - battle_file[str(defender)][int(enemy_cha)].defn <= 0:
                    tem = battle_file[str(defender)] ##No damage will be dealt if armor is greater than the attack##
                    tem[int(enemy_cha)].hp = tem[int(enemy_cha)].hp
                    battle_file[str(defender)] = tem
                    damage = 0

                else: ##The attacking phase##
                    tema = battle_file[str(attacker)]
                    temd = battle_file[str(defender)]
                    temd[int(enemy_cha)].hp = temd[int(enemy_cha)].hp - (tema[int(ally_cha)].attk - temd[int(enemy_cha)].defn)
                    damage = tema[int(ally_cha)].attk - temd[int(enemy_cha)].defn

                    battle_file[str(attacker)] = tema
                    battle_file[str(defender)] = temd

                attack_embed = discord.Embed( ##Who attacked who##
                    title=f"{fattk['name']}'s turn",
                    description=f"{fattk['name']}'s {battle_file[str(attacker)][int(ally_cha)].name} dealt "
                                f"{damage} damage to "
                                f"{fdefn['name']}'s {battle_file[str(defender)][int(enemy_cha)].name}.",
                    color=discord.Color.greyple())

                result_embed = discord.Embed(
                    title=f"{fdefn['name']}'s team",
                    colour=discord.Color.greyple())

                count = 1 ##Displaying the enemy tema's after the attack##

                for i in battle_file[str(defender)].values():
                    result_embed.add_field(name=f"{count}.{i.name}", value=f"({i.first_attr}, {i.second_attr})"
                                                                           f"hp = {battle_file[str(defender)][count].hp}\n"
                                                                    f"attack = {battle_file[str(defender)][count].attk}\n"
                                                                    f"defense = {battle_file[str(defender)][count].defn}")

                    count += 1

                await ctx.send(embed=attack_embed)
                await ctx.send(embed=result_embed) ##Attacking phases completes##



                temp = battle_file[str(attacker)] ##Checking the synergies and updating the attributes##
                tamp = battle_file[str(defender)]

                try:
                    await ctx.send(embed=value_increase(temp.values(), "Friendly", "hp", 3, 2, "increased"))
                    await ctx.send(embed=value_increase(temp.values(), "Nice", "attk", 3, 2, "increased"))
                    await ctx.send(embed=value_increase(temp.values(), "Antisocial", "defn", 3, 2, "increased"))
                    await ctx.send(
                        embed=value_increase(temp.values(), "Thin", "hp", 3, 2, "increased", conditional=True))
                    await ctx.send(embed=value_increase(temp.values(), "Without glasses", "attk", 3, 2, "increased",
                                                        conditional=True))
                    await ctx.send(
                        embed=value_increase(temp.values(), "Short", "defn", 3, 2, "increased", conditional=True))

                    await ctx.send(embed=value_increase(temp.values(), "Annoying", "hp", 3, 2, "decreased",
                                                        enemy_list=tamp.values()))
                    await ctx.send(embed=value_increase(temp.values(), "Funny", "attk", 3, 2, "decreased",
                                                        enemy_list=tamp.values()))
                    await ctx.send(embed=value_increase(temp.values(), "Intelligent", "defn", 3, 2, "decreased",
                                                        enemy_list=tamp.values()))
                    await ctx.send(embed=value_increase(temp.values(), "Fat", "hp", 3, 2, "decreased", conditional=True,
                                                        enemy_list=tamp.values))
                    await ctx.send(
                        embed=value_increase(temp.values(), "With glasses", "attk", 3, 2, "decreased", conditional=True,
                                             enemy_list=tamp.values()))
                    await ctx.send(
                        embed=value_increase(temp.values(), "Tall", "defn", 3, 2, "decreased", conditional=True,
                                             enemy_list=tamp.values()))
                except discord.errors.HTTPException:
                    pass






                battle_file[str(attacker)] = temp
                battle_file[str(defender)] = tamp

                tem = battle_file[str(defender)] ##Checking if a character is killed or not##
                for i in tem.values():
                    if i.hp <= 0:
                        i.status = "dead"
                battle_file[str(defender)] = tem


                for i in battle_file[str(defender)].values(): ##Displaying the killed character##
                    if i.status == "dead":
                        await ctx.send(embed = discord.Embed(
                            title=f"{i.name} was killed.",
                            color=discord.Color.green()))


                ##Ending the game##
                print(battle_file['turn_count'])
                if battle_file['turn_count']['turn'] >= 10:
                    attk_score = 0
                    for i in battle_file[str(attacker)].values():
                        attk_score += i.hp
                    defn_score = 0
                    for i in battle_file[str(defender)].values():
                        defn_score += i.hp

                    embed = discord.Embed(title="The Results:",color= discord.Color.blue())
                    embed.add_field(name=f"{fattk['name']}",value=f"Points = {attk_score}.")
                    embed.add_field(name=f"{fdefn['name']}",value=f"Points = {defn_score}.")

                    await ctx.send(embed= embed)
                    if attk_score >defn_score:
                        tem = fattk['inv']
                        tem.gold += 10
                        fattk['inv'] = tem

                        attk_embed = discord.Embed(title=f"{fattk['name']} defeated {fdefn['name']}.",color= discord.Color.gold())
                        await ctx.send(embed = attk_embed)

                    elif defn_score>attk_score:
                        tem = fdefn['inv']
                        tem.gold += 10
                        fdefn['inv'] = tem

                        defn_embed = discord.Embed(title=f"{fdefn['name']} defeated {fattk['name']}.", color=discord.Color.gold())
                        await ctx.send(embed= defn_embed)
                    battle_file.close()
                    lose(fattk,fdefn)

                    shutil.rmtree(f"battle_files\\{int(msg_auth.id) + int(fdefn['inv'].name)}")

                else:
                    ##Choosing another character (if the game hasnt finished yet)##
                    addidtional_cha_embed = discord.Embed(
                        title="Please choose another character to add to your battle-team."
                              " You need to write the id of your desired character.",
                        color=discord.Color.greyple())

                    addidtional_cha = []
                    for i in range(3):
                        addidtional_cha.append(random.choice([x for x in Character.dict_of_cha.values()]))
                    valid_ids = [v.id for v in addidtional_cha]
                    for v in addidtional_cha:
                        addidtional_cha_embed.add_field(name=f"{count}. {v.name}",
                                                        value=f"character id = {v.id}\ngender = {v.gender}\n\n"
                                                              f"hp = {v.hp}\nattack = {v.attk}\ndefense = {v.defn}",
                                                        inline=False)
                        count += 1

                    await ctx.send(embed=addidtional_cha_embed)

                    try:  ##Adding the chosen charater##
                        reply = await client.wait_for('message', check=check(msg_auth, valid_ids), timeout=30.0)
                        new_cha = Character.dict_of_cha[reply.content]
                        tem = battle_file[str(attacker)]
                        tem[len(tem.values()) + 1] = new_cha
                        battle_file[str(attacker)] = tem
                        print(battle_file[str(attacker)])

                        await ctx.send(embed = discord.Embed(title=f"{new_cha.name} has been added to your battle-team.",
                                                             colour=discord.Color.green()))

                    except asyncio.TimeoutError:  ##If the user didnt reply fast enough, he loses##
                        tem = fdefn['inv']
                        tem.gold += 10
                        fdefn['inv'] = tem

                        lose(fattk, fdefn)
                        battle_file.close()
                        if os.path.exists(f"battle_files\\{int(msg_auth.id) + int(fdefn['inv'].name)}"):
                            shutil.rmtree(f"battle_files\\{int(msg_auth.id) + int(fdefn['inv'].name)}")
                        await ctx.send(embed=discord.Embed(
                            title=f'{fattk["name"]} has been idled for too long and loses the game.',
                            colour=discord.Color.greyple()))

                ##Letting the other player plays##
                tem1 = fattk["inv"]
                tem1.on_turn = False
                fattk["inv"] = tem1

                tem2 = fdefn["inv"]
                tem2.on_turn = True
                fdefn["inv"] = tem2


            fdefn.close()
        fattk.close()


@client.command()
async def surrender(ctx):
    msg_auth = ctx.message.author
    if not started(msg_auth):
        await ctx.send(embed = discord.Embed(
            title=pls_register_first,
            colour=discord.Color.red()))

    else:
        with shelve.open(f"Player databases\\{msg_auth.id}\\playerinv") as fself:
            if fself['inv'].in_battle == False:
                await ctx.send(embed=discord.Embed(
                    title=not_in_battle,
                    colour=discord.Color.red()))

            elif fself['inv'].on_turn == False:
                await ctx.send(embed=discord.Embed(
                    title=not_on_turn,
                    colour=discord.Color.red()))
            else:
                fother = shelve.open(f"Player databases\\{fself['inv'].battle_with['key'].name}\\playerinv")
                tem = fother['inv']
                tem.gold += 10
                fother['inv'] = tem

                lose(fself,fother)

                shutil.rmtree(f"battle_files\\{int(msg_auth.id) + int(fother['inv'].name)}")

                fother.close()


                await ctx.send(embed = discord.Embed(
                    title=f"{msg_auth.name} surrendered.",
                    color= discord.Color.red()))

client.run(Token)




