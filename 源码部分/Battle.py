import Card
import CardMoves
import random
# 与boss战斗的四个阶段
# 打牌、触发效果、造成伤害、受到伤害

# 多人：
def Play_Cards(Players, Player_order, boss_card, discard_pile, library): # 打出手牌
    # 行动玩家，行动玩家序号，当前boss，弃牌堆，牌库
    Player = Players[Player_order - 1]
    print("---" + str(Player_order) + "号玩家出牌阶段---")
    if not CardMoves.Show_Hand(Player):
        return False
    print("目前boss：" + boss_card.ReadCard() + " 攻击力: " + str(boss_card.attack) + ", 生命值: " + str(boss_card.health))
    print("目前弃牌堆的牌数：" + str(len(discard_pile)) + "；目前牌堆的牌数：" + str(len(library)))
    tempt = "各玩家手牌数："
    for i in range(len(Players)):
        tempt += str(i + 1) + "号玩家：" + str(len(Players[i])) + "张；"
    print(tempt)
    print("请输入你想要打出的手牌序号，或输入0以跳过，输入00以认输，注意如果所有玩家均主动或被动地连续跳过，则默认判负：")
    numbers = input()
    if numbers == "0":
        return False
    if numbers == "00":
        return "yield"
    check = CardMoves.Play_Cards(numbers, Player, boss_card.tempt_discard_pile)
    while(not check):
        numbers = input()
        if numbers == "0":
            return False
        if numbers == "00":
            return "yield"
        check = CardMoves.Play_Cards(numbers, Player, boss_card.tempt_discard_pile)
    return check # 成功打出时，返回打出的牌组成的列表，打出的牌进入boss牌的临时弃牌堆

def Discard(Players, Player_order, attack, discard_pile):
    Player = Players[Player_order - 1]
    if attack == 0:
        print("boss的攻击为0，无需弃牌")
        return False
    print("boss的攻击为" + str(attack) + "，需要弃置点数之和不小于" + str(attack) + "的手牌")
    sum = 0
    for x in Player:
        sum += x.number
    if sum < attack:
        print("手牌点数不足，你被击败了！")
        Players.pop(Player_order - 1)
        if len(Players) == 0:
            print("队伍已被全部击败，游戏失败！")
            return True
        print("你的队友将会继续战斗，序号大于" + str(Player_order) + "的成员的序号将会依次减一，游戏继续")
        return True
    CardMoves.Show_Hand(Player)
    print("请输入你想要弃置的手牌序号：")
    numbers = input()
    check = CardMoves.Discard(numbers, Player, attack, discard_pile)
    while(not check):
        numbers = input()
        check = CardMoves.Discard(numbers, Player, attack, discard_pile)
    return False

def Trigger_Effect_and_Create_Damage(Cards, boss_card, Players, Player_order, library, discard_pile, limit): # 触发效果并造成伤害
    # 打出的牌，当前boss，全部玩家，行动玩家序号，牌库，弃牌堆
    if len(Cards) == 1 and Cards[0].colour == "Joker":
        boss_card.colour = boss_card.colour.upper()
        return "joker"
    colour = []
    for x in Cards:
        if not x.colour in colour:
            colour.append(x.colour)
    invalid = False
    if boss_card.colour in colour:
        invalid = True
        colour.remove(boss_card.colour)
    effect = ""
    for x in colour:
        effect += Card.Read_Colour(x)
        effect += "、"
    effect = effect[:-1]
    sum = 0
    for x in Cards:
        if x.number == 11:
            s = 10
        elif x.number == 12:
            s = 15
        elif x.number == 13:
            s = 20
        else:
            s = x.number
        sum += s
    if invalid and len(colour) > 0:
        print(Card.Read_Colour(boss_card.colour) + "对boss无效，生效花色为：" + effect + "，数值为" + str(sum))
    elif invalid:
        print(Card.Read_Colour(boss_card.colour) + "对boss无效，打出的牌数值为" + str(sum))
    else:
        print("生效花色为：" + effect + "，数值为" + str(sum))
    if "spades" in colour:
        boss_card.attack = max(0, boss_card.attack - sum)
        print("黑桃效果发动，boss的攻击力被降至" + str(boss_card.attack))
    if "hearts" in colour:
        CardMoves.Recover(sum, library, discard_pile)
    if "diamonds" in colour:
        CardMoves.Draw_Card(sum, Players, Player_order, library, limit)
    if "clubs" in colour:
        boss_card.health -= sum * 2
        print("梅花效果发动，对boss造成了" + str(sum * 2) + "点伤害")
    else:
        boss_card.health -= sum
        print("对boss造成了" + str(sum) + "点伤害")
    return

def Check_Boss_Card(boss_card, boss_library, library, discard_pile): # 检查boss状况，返回是否击败及将要面对的boss（不论是否变动）
    # 当前boss，boss库，牌库，弃牌堆
    if boss_card.health > 0:
        print("boss剩余血量：" + str(boss_card.health) + "，由于未能击杀，将受到boss的反击")
        return False, boss_card
    elif len(boss_library) > 0:
        discard_pile += boss_card.tempt_discard_pile
        random.shuffle(discard_pile) # 将临时弃牌堆的牌洗入弃牌堆，然后洗牌
        if boss_card.health < 0:
            print("成功击杀boss，下一个boss为" + boss_library[0].ReadCard())
            return True, boss_library.pop(0)
        print("成功感化boss，下一个boss为" + boss_library[0].ReadCard())
        boss_card.colour = boss_card.colour.lower()
        library.insert(0, boss_card)
        return True, boss_library.pop(0)
    else:
        print("恭喜，成功过关！")
        return True, None
    
def Complete_Process(boss_card, Players, Player_order, library, discard_pile, boss_library, limit): # 完整流程
    Cards = Play_Cards(Players, Player_order, boss_card, discard_pile, library)
    last = Player_order
    while (not Cards):
        Player_order += 1
        if Player_order == len(Players) + 1:
            Player_order = 1
        if Player_order == last:
            print("所有玩家均选择跳过，游戏失败!")
            return False, False
        Cards = Play_Cards(Players, Player_order, boss_card, discard_pile, library)
    if Cards == "yield":
        print("已投降")
        return False, False
    result = Trigger_Effect_and_Create_Damage(Cards, boss_card, Players, Player_order, library, discard_pile, limit)
    if result == "joker":
        print("joker牌效果已发动，请输入角色序号指定下一个行动的玩家：")
        check = False
        while(not check):
            check = True
            x = input()
            for i in x:
                if not i.isdigit():
                    print("非法输入，请重新输入")
                    check = False
                    continue
            new_order = int(x)
            if new_order > len(Players) or new_order <= 0:
                print("输入数字超出范围，请重新输入")
                check = False
                continue
        return new_order, boss_card # 返回下一个行动的序号及当前boss
    # 未进入上面的条件分支，则是正常结算完成了
    kill, next = Check_Boss_Card(boss_card, boss_library, library, discard_pile)
    if kill == True:
        if next == None:
            return False, True # 第一个False判断游戏是否还要继续，第二个True代表获胜
        return Player_order, next
    # 未进入上面的条件分支，则是未击杀boss，需要受到boss的反击，即弃牌
    defeated = Discard(Players, Player_order, boss_card.attack, discard_pile)
    if defeated:
        if len(Players) == 0:
            return False, False
        return Player_order, next
    new_order = Player_order + 1
    if new_order == len(Players) + 1:
        new_order = 1
    return new_order, next

# 单人
def Play_Cards_1(Player, boss_card, discard_pile, library): # 打出手牌
    # 玩家，当前boss，弃牌堆，牌库
    print("---出牌阶段---")
    if not CardMoves.Show_Hand_1(Player):
        return False
    print("目前boss：" + boss_card.ReadCard() + " 攻击力: " + str(boss_card.attack) + ", 生命值: " + str(boss_card.health))
    print("目前弃牌堆的牌数：" + str(len(discard_pile)) + "；目前牌堆的牌数：" + str(len(library)))
    print("请输入你想要打出的手牌序号，或输入0以使用joker，输入00以认输：")
    numbers = input()
    if numbers == "0":
        return "joker"
    if numbers == "00":
        return "yield"
    check = CardMoves.Play_Cards(numbers, Player, boss_card.tempt_discard_pile)
    while(not check):
        numbers = input()
        if numbers == "0":
            return "joker"
        if numbers == "00":
            return "yield"
        check = CardMoves.Play_Cards(numbers, Player, boss_card.tempt_discard_pile)
    return check # 成功打出时，返回打出的牌组成的列表，打出的牌进入boss牌的临时弃牌堆

def Discard_1(Player, attack, library, discard_pile, joker):
    if attack == 0:
        print("boss的攻击为0，无需弃牌")
        return False, joker
    print("boss的攻击为" + str(attack) + "，需要弃置点数之和不小于" + str(attack) + "的手牌")
    CardMoves.Show_Hand(Player)
    x = "1"
    while (joker > 0 and x == "1"):
        print("如果想要使用joker牌，请输入1，否则请输入任意其它内容")
        x = input()
        if x == "1":
            print("joker效果发动，弃置全部手牌并重抽8张")
            for i in range(len(Player)):
                discard_pile.append(Player.pop(0))
            if len(library) == 0:
                print("牌库已经空了，抽牌失败，游戏失败")
                return True
            if len(library) < 8:
                print("成功抽取" + str(len(library)) + "张手牌，牌库已经抽空，抽牌提前终止")
                for i in range(len(library)):
                    Player.append(library.pop(0))
                CardMoves.Arrange_Hand(Player)
            else:
                print("成功抽取8张牌")
                for i in range(8):
                    Player.append(library.pop(0))
            joker -= 1
            print("joker牌效果本局游戏中还可以发动" + str(joker) + "次，游戏继续")
            CardMoves.Show_Hand(Player)
    sum = 0
    for x in Player:
        sum += x.number
    if sum < attack:
        print("手牌点数不足，你被击败了！")
        return True, joker
    print("请输入你想要弃置的手牌序号：")
    numbers = input()
    check = CardMoves.Discard(numbers, Player, attack, discard_pile)
    while(not check):
        numbers = input()
        check = CardMoves.Discard(numbers, Player, attack, discard_pile)
    return False, joker

def Trigger_Effect_and_Create_Damage_1(Cards, boss_card, Player, library, discard_pile, joker): # 触发效果并造成伤害
    # 打出的牌，当前boss，全部玩家，行动玩家序号，牌库，弃牌堆
    if Cards == "joker":
        if joker == 0:
            print("本局游戏joker牌使用次数已用完，无法再使用！")
            return "JOKER"
        else:
            print("joker效果发动，弃置全部手牌并重抽8张")
            discard_pile += Player
            if len(library) < 8:
                print("成功抽取" + str(len(library)) + "张手牌，牌库已经抽空，抽牌提前终止")
                Player = library
                library = []
            else:
                print("成功抽取8张牌")
                Player = library[0:8]
                library = library[9:]
            return "joker"
    colour = []
    for x in Cards:
        if not x.colour in colour:
            colour.append(x.colour)
    invalid = False
    if boss_card.colour in colour:
        invalid = True
        colour.remove(boss_card.colour)
    effect = ""
    for x in colour:
        effect += Card.Read_Colour(x)
        effect += "、"
    effect = effect[:-1]
    sum = 0
    for x in Cards:
        if x.number == 11:
            s = 10
        elif x.number == 12:
            s = 15
        elif x.number == 13:
            s = 20
        else:
            s = x.number
        sum += s
    if invalid and len(colour) > 0:
        print(Card.Read_Colour(boss_card.colour) + "对boss无效，生效花色为：" + effect + "，数值为" + str(sum))
    elif invalid:
        print(Card.Read_Colour(boss_card.colour) + "对boss无效，打出的牌数值为" + str(sum))
    else:
        print("生效花色为：" + effect + "，数值为" + str(sum))
    if "spades" in colour:
        boss_card.attack = max(0, boss_card.attack - sum)
        print("黑桃效果发动，boss的攻击力被降至" + str(boss_card.attack))
    if "hearts" in colour:
        CardMoves.Recover(sum, library, discard_pile)
    if "diamonds" in colour:
        CardMoves.Draw_Card_1(sum, Player, library)
    if "clubs" in colour:
        boss_card.health -= sum * 2
        print("梅花效果发动，对boss造成了" + str(sum * 2) + "点伤害")
    else:
        boss_card.health -= sum
        print("对boss造成了" + str(sum) + "点伤害")
    return

def Complete_Process_1(boss_card, Player, library, discard_pile, boss_library, joker): # 完整流程
    Cards = Play_Cards_1(Player, boss_card, discard_pile, library)
    if not Cards:
        return False, False, 0
    if Cards == "yield":
        print("已投降")
        return False, False, 0
    result = Trigger_Effect_and_Create_Damage_1(Cards, boss_card, Player, library, discard_pile, joker)
    if result == "joker":
        joker -= 1
        print("joker牌效果本局游戏中还可以发动" + str(joker) + "次，游戏继续")
        return True, boss_card, joker # 返回是否继续及当前boss以及joker牌剩余使用次数
    while (result == "JOKER"):
        Cards = Play_Cards_1(Player, boss_card, discard_pile, library)
        if not Cards:
            return False, False, joker
        if Cards == "yield":
            print("已投降")
            return False, False, joker
        result = Trigger_Effect_and_Create_Damage_1(Cards, boss_card, Player, library, discard_pile, joker)
    # 未进入上面的条件分支，则是正常结算完成了
    kill, next = Check_Boss_Card(boss_card, boss_library, library, discard_pile)
    if kill == True:
        if next == None:
            return False, True, joker # 第一个False判断游戏是否还要继续，第二个True代表获胜，joker代表剩余joker使用次数
        return True, next, joker
    # 未进入上面的条件分支，则是未击杀boss，需要受到boss的反击，即弃牌
    defeated, joker = Discard_1(Player, boss_card.attack, library, discard_pile, joker)
    if defeated:
        return False, False, joker
    return True, next, joker