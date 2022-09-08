import random

# 卡牌的基础设定

class card():
    def __init__(self, colour, number):
        self.colour = colour
        self.number = number
    
    def ReadCard(self):
        if self.colour == "Joker":
            return "Joker"
        if self.colour == "spades":
            c = "黑桃"
        elif self.colour == "hearts":
            c = "红桃"
        elif self.colour == "clubs":
            c = "梅花"
        elif self.colour == "diamonds":
            c = "方块"
        else:
            if self.number == 11:
                return "J，花色被消除"
            if self.number == 12:
                return "Q，花色被消除"
            return "K，花色被消除"
        if self.number <= 10:
            return c + str(self.number)
        elif self.number == 11:
            return c + "J"
        elif self.number == 12:
            return c + "Q"
        else:
            return c + "K"

class BossCard(card):
    def __init__(self, colour, number):
        self.colour = colour
        self.number = number
        self.tempt_discard_pile = []
        if number == 11:
            self.attack = 10
            self.health = 20
        elif number == 12:
            self.attack = 15
            self.health = 30
        else:
            self.attack = 20
            self.health = 40

def Read_Colour(c):
    if c =="spades":
        return "黑桃"
    if c == "hearts":
        return "红桃"
    if c == "clubs":
        return "梅花"
    if c == "diamonds":
        return "方块"

def Initialize_Library(): # 创建随机牌库
    library = []
    for i in range(10):
        tempt = card("spades", i + 1) # 黑桃
        library.append(tempt)
        tempt = card("hearts", i + 1) # 红桃
        library.append(tempt)
        tempt = card("clubs", i + 1) # 梅花
        library.append(tempt)
        tempt = card("diamonds", i + 1) # 方块
        library.append(tempt)
    random.shuffle(library) # 洗牌库
    # for i in library:
    #     print(i.colour + str(i.number))
    # print(len(library))
    return library

def Initialize_Boss(): # 创建随机Boss库
    boss = []
    for i in range(11, 14):
        tempt = []
        temptcard = BossCard("spades", i) # 黑桃
        tempt.append(temptcard)
        temptcard = BossCard("hearts", i) # 红桃
        tempt.append(temptcard)
        temptcard = BossCard("clubs", i) # 梅花
        tempt.append(temptcard)
        temptcard = BossCard("diamonds", i) # 方块
        tempt.append(temptcard)
        random.shuffle(tempt)
        for x in tempt:
            boss.append(x)
    return boss

def Initialize_Game():
    return Initialize_Library(), Initialize_Boss(), [] # 牌堆、Boss堆、弃牌堆


"""x, y, z= Initialize_Game()
print(len(x))
for i in x:
    print(i.ReadCard())
for j in y:
    print(j.ReadCard())"""