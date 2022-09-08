import Card
import random

# 对手牌、牌堆、弃牌堆的操作

def Compare_Cards(c1, c2): # 卡牌的比较
    order = ["spades", "hearts", "clubs", "diamonds"]
    if order.index(c1.colour) < order.index(c2.colour):
        return 1 # c1比c2小
    elif order.index(c1.colour) > order.index(c2.colour):
        return -1 # c1比c2大
    else:
        if c1.number < c2.number:
            return 1 # c1比c2小
        else:
            return -1 # c1比c2大

def Arrange_Hand(Player): # 整理手牌
    # 数量不多，就冒泡排了
    for i in range(len(Player) - 1):
        change = False
        for j in range(len(Player) - 1 - i):
            if Compare_Cards(Player[j], Player[j + 1]) == -1:
                Player[j], Player[j + 1] = Player[j + 1], Player[j]
                change = True
        if not change:
            break
    return

def Set_Cards(Players, library): # 发牌
    # 玩家、牌堆
    draw_num = len(Players) * (9 - len(Players))
    Player_order = 1
    Player_number = len(Players)
    o = Player_order - 1 # 当前需要抽卡的玩家
    while(draw_num > 0):
        Players[o].append(library[0])
        Arrange_Hand(Players[o])
        library.pop(0)
        draw_num -= 1
        o += 1
        o = o % Player_number
    print("牌堆设置完成，游戏正式开始")
    return

def Draw_Card(draw_num, Players, Player_order, library, limit): # 抽牌
    # 抽的张数、玩家、第一个抽卡的玩家的序号、牌堆
    if len(library) == 0:
        print("方片效果发动，但牌库已经没有牌了，抽牌失败")
        return
    Player_number = len(Players)
    o = Player_order - 1 # 当前需要抽卡的玩家
    limited = False # 是否存在已经确认的手牌达到上限的玩家
    oringinal_num = draw_num
    while(draw_num > 0):
        if len(library) == 0:
            print("方片效果发动，成功抽取"+ str(oringinal_num - draw_num) + "张牌，牌堆已被抽空，抽牌提前终止")
            return
        if limited:
            if o == last: # last是手牌达到上限时定义的，直到出现手牌未达到上限的玩家之前都不会更改，o == last代表所有玩家手牌均达到上限
                print("方片效果发动，成功抽取"+ str(oringinal_num - draw_num) + "张牌，所有玩家手牌均达到上限，抽牌提前终止")
                return
            if len(Players[o]) == limit: # 当前角色手牌数已经到达上限
                o += 1
                o = o % Player_number # 跳转至下一个角色，limited不变
                continue
            # 没有进上面两种情况，说明当前角色手牌数未到上限
            Players[o].append(library.pop(0))
            Arrange_Hand(Players[o])
            limited = False
            draw_num -= 1
        else:
            # limited为False，代表上一个角色抽了牌
            if len(Players[o]) == limit:
                last = o
                o += 1
                o = o % Player_number
                limited = True
            else:
                Players[o].append(library.pop(0))
                Arrange_Hand(Players[o])
                o += 1
                o = o % Player_number
                limited = False
                draw_num -= 1
    print("方片效果发动，成功抽取"+ str(oringinal_num) + "张牌")
    return

def Recover(Recover_num, library, discard_pile): # 从弃牌堆回收牌至牌库
    # 放回的张数、牌堆、弃牌堆
    if len(discard_pile) == 0:
        print("红桃效果发动，但弃牌堆中没有牌，回收失败")
        return
    random.shuffle(discard_pile) # 洗弃牌堆
    for i in range(Recover_num):
        library.append(discard_pile.pop())
        if len(discard_pile) == 0 and i < Recover_num - 1:
            random.shuffle(library) # 洗牌堆
            print("红桃效果发动，成功从弃牌堆回收" + str(i) + "张牌，弃牌堆卡牌数量为0，回收提前终止")
            return
    random.shuffle(library) # 洗牌堆
    print("红桃效果发动，成功从弃牌堆回收" + str(Recover_num) + "张牌")
    return
    
def Show_Hand(Player): # 展示手牌
    # 持手牌的玩家
    if len(Player) == 0:
        print("你目前没有手牌，跳过操作")
        return False # 直接跳过接下来的操作
    print("你的手牌有：")
    for i in range(len(Player)):
        print(str(i + 1) + ". " + Player[i].ReadCard())
    return True

def Play_Cards(numbers, Player, tempt_discard_pile): # 打出手牌，仅检查是否可以打出以及将打出的牌置入临时弃牌堆
    # 打出的牌的编号，持牌玩家，临时弃牌堆
        # numbers应为一个字符串
    c = []
    check = []
    for i in numbers:
        if not i.isdigit():
            print("非法输入，请重新输入")
            return False
        if int(i) < 1 or int(i) > len(Player):
            print("输入数字超出范围，请重新输入")
            return False
        if i in check:
            print("请勿输入重复的数字")
            return False
        check.append(i)
        c.append(Player[int(i) - 1])
    # c为所有的要打出的卡牌了
    if len(c) == 1: # 一张牌，一定可行
        for i in c:
            Player.remove(i)
            tempt_discard_pile.append(i)
        return c # 从手牌移至临时弃牌堆，返回打出的牌的列表
    if len(c) == 2 and (c[0].number == 1 or c[1].number == 1): # 有宠物牌
        for i in c:
            Player.remove(i)
            tempt_discard_pile.append(i)
        return c # 从手牌移至临时弃牌堆，返回打出的牌的列表
    for i in c:
        if i.number == 1:
            print("宠物仅能与一张任意其它牌一同打出，不能参与多张牌的连招，请重新输入")
            return False # 有宠物牌且大于等于3张一起打出
    for i in c:
        if i.number != c[0].number:
            print("仅有使用若干张点数相同的牌作为连招打出或是一张任意牌携带宠物(点数为1的牌)打出的情况下才可以打出多张牌，请重新输入")
            return False # 使用的牌点数不同，不能作为连招打出
    if c[0].number * len(numbers) > 10:
        print("连招需要点数和不大于10才可打出，请重新输入")
        return False # 使用的牌和大于10，不能作为连招打出
    for i in c:
        Player.remove(i)
        tempt_discard_pile.append(i) # 只剩正确连招的情况了
    return c # 从手牌移至临时弃牌堆，再返回打出的牌的列表

def Discard(numbers, Player, attack, discard_pile): # 受到boss攻击，弃置手牌
    # 选定弃置的手牌序号，持牌玩家，受到的伤害值，弃牌堆
        # numbers应为一个字符串
    c = []
    check = []
    for i in numbers:
        if not i.isdigit():
            print("非法输入，请重新输入")
            return False
        if int(i) < 1 or int(i) > len(Player):
            print("输入数字超出范围，请重新输入")
            return False
        if i in check:
            print("请勿输入重复的数字")
            return False
        check.append(i)
        c.append(Player[int(i) - 1])
    # c为要弃置的牌
    sum = 0
    for i in c:
        sum += i.number
    if sum < attack:
        print("弃置的牌之和小于受到的伤害，请重新输入")
        return False
    for i in c:
        Player.remove(i)
        discard_pile.append(i)
    print("已将" + str(len(numbers)) + "张牌置入弃牌堆")
    return True # 从手牌移至弃牌堆，返回True代表成功

def Set_Cards_1(player, library):
    for i in range(8):
        player.append(library.pop(0))
    Arrange_Hand(player)
    return

def Draw_Card_1(draw_num, Player, library):
    # 抽的张数、玩家、牌堆
    if len(library) == 0:
        print("方片效果发动，但牌库已经没有牌了，抽牌失败")
        return
    oringinal_num = draw_num
    while(draw_num > 0):
        if len(library) == 0:
            print("方片效果发动，成功抽取"+ str(oringinal_num - draw_num) + "张牌，牌堆已被抽空，抽牌提前终止")
            return
        if len(Player) == 8:
            print("方片效果发动，成功抽取"+ str(oringinal_num - draw_num) + "张牌，手牌已到上限，抽牌提前终止")
            return
        Player.append(library.pop(0))
        Arrange_Hand(Player)
        draw_num -= 1
    print("方片效果发动，成功抽取"+ str(oringinal_num) + "张牌")
    return

def Show_Hand_1(Player): # 展示手牌
    # 持手牌的玩家
    if len(Player) == 0:
        print("你没有手牌可打了，游戏失败！")
        return False # 直接跳过接下来的操作
    print("你的手牌有：")
    for i in range(len(Player)):
        print(str(i + 1) + ". " + Player[i].ReadCard())
    return True