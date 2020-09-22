import discord
class Character:   #Setup the character construction class

    dict_of_cha = {}
    def __init__(self,name , id, hp, attk, defn, first_attr, second_attr, first_des, second_des,
                 image_file, gender, cost, status = None):
        self.name = name
        self.id = id
        self.hp = hp
        self. attk = attk
        self.defn = defn
        self.first_attr = first_attr
        self.second_attr = second_attr
        self.first_des = first_des
        self.second_des = second_des
        self.image_file = image_file
        self.gender = gender
        self.cost = cost
        self.dict_of_cha[self.id] = self

        if status is None:
            self.status = "alive"  ##There are multiple status: alive, dead, stunned
        else:
            self.status = status






    def __str__(self):
        return(f"{self.name}")

    def description(self):
        return(f"Gender = {self.gender}\nCost = {self.cost}\n\n"
               f"Hp = {self.hp}\nAttack = {self.attk}\nDefense = {self.defn}\n"
               f"Personality = {self.first_attr}: {self.first_des}\n\nAppearance = {self.second_attr}: {self.second_des}")



class Player:   ##Setup the character construction class

    def __init__(self,name,cha_dict = None, selected_cha = None, gold = None,
                 in_battle = None, challenger = None, on_turn = None, battle_with = None,
                 p = None, first_turn = None):
        self.name = name
        if cha_dict is None:
            self.cha_dict = {}
        else:
            self.cha_dict = cha_dict

        if selected_cha is None:
            self.selected_cha = {"1":None,"2":None,"3":None}
        else:
            self.selected_cha = selected_cha

        if gold is None:
            self.gold = 40
        else:
            self.gold = gold

        if in_battle is None:
            self.in_battle = False
        else:
            self.in_battle = in_battle

        if challenger is None:
            self.challenger = {"key":None}
        else:
            self.challenger = challenger


        if on_turn is None:
            self.on_turn = False
        else:
            self.on_turn = on_turn

        if battle_with is None:
            self.battle_with = {"key": None}
        else:
            self.battle_with = battle_with

        if p is None:
            self.p = None
        else:
            self.p = p

        if first_turn is None:
            self.first_turn = False
        else:
            self.first_turn = first_turn




    def cha_num(self):
        return (f"You have a total of {len(self.cha_dict)} characters in your inventory")

    def add_gold(self, value):
        self.gold += value
        return self.gold


    def fight(self, defner):
        pass










##Personality and appearance descrpition strings##

p_friendly = "When you have [ 2 , 3 ] friendly characters, each member of the ally team gains hp."
p_nice = "When you have [ 2 , 3 ] nice characters, each member of the ally team gains attack."
p_antisocial = "When you have [ 2 , 3 ] antisocial characters, each member of the ally team gains defense."

p_annoying = "When you have [ 2 , 3 ] annoying characters, each member of the enemy team loses hp."
p_funny = "When you have [ 2 , 3 ] funny characters, each member of the enemy team loses attack."
p_intelligent = "When you have [ 2 , 3 ] intelligent characters, each member of the enemy team loses defense."


a_thin = "When you have [ 2, 3 ] thin characters, every thin character in the ally teams gains hp."
a_without_glasses = "When you have [ 2, 3 ] characters without glasses , every character without glasses in the ally team gains attack."
a_short = "When you have [ 2, 3 ] short characters, every short character in the ally team gains defense."

a_fat = "When you have [ 2, 3 ] fat characters, every fat character in the enemy team loses hp."
a_with_glasses = "When you have [ 2, 3 ] characters with glasses, every character with glasses in the enemy team loses attack."
a_tall =  "When you have [ 2, 3 ] tall characters, every tall character in the enemy team loses defense."



##Character construction##
#Defining characters, their passives and their abilities##


cha001 = Character("Tin Win Naing", "001", 15, 7, 2, "Annoying", "Thin",
                   p_annoying, a_thin,
                   "001pic.jpg","male", 10)

cha002 = Character("Ye Yint Nyi Nyi", "002", 18, 6, 2, "Antisocial", "Tall",
                   p_antisocial, a_tall,
                   "002pic.jpg","male", 10)

cha003 = Character("Khant Nyar Lu", "003", 18, 6, 3, "Intelligent", "With glasses",
                   p_intelligent, a_with_glasses,
                   "003pic.jpg","male", 10)

cha004 = Character("Hphone Myat Mon", "004", 18, 5, 4, "Antisocial", "Without glasses",
                    p_antisocial, a_without_glasses,
                   "004pic.jpg","male", 10)

cha005 = Character("Thila", "005", 25, 6, 3, "Friendly", "Thin",
                   p_friendly, a_thin,
                   "005pic.jpg","male", 10)

cha006 = Character("Moses", "006", 23, 6, 2, "Nice", "Tall",
                   p_nice, a_tall,
                   "006pic.jpg","male", 10)

cha007 = Character("Thiri Shin That", "007", 25, 5, 3, "Annoying", "Fat",
                   p_annoying, a_fat,
                   "007pic.jpg","female", 10)

cha008 = Character("Ei Ei Min", "008", 15, 5, 4, "Nice", "Short",
                   p_nice, a_short,
                   "008pic.jpg","female", 10)

cha009 = Character("Lamin No No", "009", 15, 5, 3, "Annoying", "Without_glasses",
                    p_annoying, a_without_glasses,
                   "009pic.jpg", "female", 10)

cha010 = Character("Thiha Swan Htet", "010", 23, 5,1, "Intelligent", "With_glasses",
                    p_intelligent, a_with_glasses,
                   "010pic.jpg", "male", 10)

cha011 = Character("Aung Kyaw Myint", "011", 20, 5, 2, "Nice", "Fat",
                   p_nice, a_fat,
                   "011pic.jpg", "female", 10)

cha012 = Character("Kay Khine Maw", "012", 20, 5, 2, "Friendly", "Short",
                   p_friendly, a_short,
                   "012pic.jpg","female", 10)

cha013 = Character("Zin Min Htet", "013", 18, 4, 2, "Friendly", "Short",
                   p_friendly, a_short,
                   "013pic.jpg", "male", 10)

cha014 = Character("Kyal Sin Linn", "014", 25, 3, 2, "Friendly", "With_glasses",
                   p_friendly, a_with_glasses,
                   "014pic.jpg", "female", 10)

cha015 = Character("Yun Yee Ywal Nay Myo", "015", 23, 3, 1, "Friendly", "Thin",
                   p_friendly, a_thin,
                   "015pic.jpg","female", 10)

##Fuctions for manipulating attributes based on the synergy##
def statement(synergy,number, name, attribute, initial, final, in_or_de):
    return (f"Because {number} of the same '{synergy}' synergy were present,\n" 
               f"{name}'s {attribute} has been {in_or_de} from {initial} to {final}.")



def value_increase(ally_list,attribute, value_type, base_value, bonus_value,in_or_de, conditional = False, enemy_list = None):


    same_synergy_num = [x for x in ally_list if x.first_attr == attribute]
    embed = discord.Embed(color=discord.Color.green())
    if enemy_list is None:
        if len(same_synergy_num) < 2:
            return
        elif conditional == False and len(same_synergy_num) >= 2:
            if len(same_synergy_num) >= 3:
                for i in ally_list:
                    i.__dict__[value_type] += base_value + bonus_value
                    embed.add_field(name=statement(attribute, len(same_synergy_num), i.name, value_type,
                                                   i.__dict__[value_type] - (base_value + bonus_value),
                                                   i.__dict__[value_type], in_or_de), value="##########", inline=False)

                return embed


            elif len(same_synergy_num) >= 2:
                for i in ally_list:
                    i.__dict__[value_type] += base_value
                    embed.add_field(name=statement(attribute, len(same_synergy_num), i.name, value_type,
                                                   i.__dict__[value_type] - base_value,
                                                   i.__dict__[value_type], in_or_de), value="##########", inline=False)
                return embed

        elif conditional == True and len(same_synergy_num) > 2:
            if len(same_synergy_num) >= 3:
                for i in ally_list:
                    if i.first_attr == attribute:
                        i.__dict__[value_type] += base_value + bonus_value
                        embed.add_field(name=statement(attribute, len(same_synergy_num), i.name, value_type,
                                                       i.__dict__[value_type] - (base_value + bonus_value),
                                                       i.__dict__[value_type], in_or_de), value="##########",
                                        inline=False)
                return embed

            elif len(same_synergy_num) >= 2:
                for i in ally_list:
                    if i.first_attr == attribute:
                        i.__dict__[value_type] += base_value
                        embed.add_field(name=statement(attribute, len(same_synergy_num), i.name, value_type,
                                                       i.__dict__[value_type] - base_value,
                                                       i.__dict__[value_type], in_or_de), value="##########",
                                        inline=False)
                return embed

    else:
        if len(same_synergy_num) < 2:
            return discord.Embed(title="Not enough synergies.", colour=discord.Color.greyple())
        elif conditional == False and len(same_synergy_num) >= 2:
            if len(same_synergy_num) >= 3:
                for i in enemy_list:
                    i.__dict__[value_type] += -(base_value + bonus_value)
                    embed.add_field(name=statement(attribute, len(same_synergy_num), i.name, value_type,
                                                   i.__dict__[value_type] - (base_value + bonus_value),
                                                   i.__dict__[value_type], in_or_de), value="##########", inline=False)

                return embed


            elif len(same_synergy_num) >= 2:
                for i in enemy_list:
                    i.__dict__[value_type] += -(base_value)
                    embed.add_field(name=statement(attribute, len(same_synergy_num), i.name, value_type,
                                                   i.__dict__[value_type] - base_value,
                                                   i.__dict__[value_type], in_or_de), value="##########", inline=False)
                return embed

        elif conditional == True and len(same_synergy_num) > 2:
            if len(same_synergy_num) >= 3:
                for i in enemy_list:
                    if i.first_attr == attribute:
                        i.__dict__[value_type] += -(base_value + bonus_value)
                        embed.add_field(name=statement(attribute, len(same_synergy_num), i.name, value_type,
                                                       i.__dict__[value_type] - (base_value + bonus_value),
                                                       i.__dict__[value_type], in_or_de), value="##########",
                                        inline=False)
                return embed

            elif len(same_synergy_num) >= 2:
                for i in enemy_list:
                    if i.first_attr == attribute:
                        i.__dict__[value_type] += -(base_value)
                        embed.add_field(name=statement(attribute, len(same_synergy_num), i.name, value_type,
                                                       i.__dict__[value_type] - base_value,
                                                       i.__dict__[value_type], in_or_de), value="##########",
                                        inline=False)
                return embed















