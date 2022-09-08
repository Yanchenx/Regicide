import Card
import CardMoves
import Battle
import random

def Get_Player_Number():
    print("请输入游玩人数(1-4人)")
    i = input()
    if i == "2":
        return [[], []], 7
    if i == "3":
        return [[], [], []], 6
    if i == "4":
        return [[], [], [], []], 5
    if i == "1":
        return [], 8
    else:
        print("非法输入，请重新输入")
        return False, False

library, Bosses, discard_pile = Card.Initialize_Game()
Players, limit = Get_Player_Number()
while(not limit):
    Players, limit = Get_Player_Number()
Joker = Card.card("Joker", 0)
if limit < 8:
    for i in range(7 - limit):
        library.append(Joker)
    random.shuffle(library)
    CardMoves.Set_Cards(Players, library)
    boss = Bosses.pop(0)
    check = True
    order = 1
    while(check):
        order, boss = Battle.Complete_Process(boss, Players, order, library, discard_pile, Bosses, limit)
        if not order: # 注意order不会是0，所以不会出问题
            if boss:
                print("游戏结束，玩家胜利")
            else:
                print("游戏结束，玩家失败")
            check = False
else: # 单人游戏
    joker = 2
    Player = []
    CardMoves.Set_Cards_1(Player, library)
    boss = Bosses.pop(0)
    check = True
    while(check):
        check, boss, joker = Battle.Complete_Process_1(boss, Player, library, discard_pile, Bosses, joker)
    if not boss:
        print("游戏结束，玩家失败")
    else:
        if joker == 2:
            print("游戏结束，玩家胜利，本局游戏中没有使用joker，获得金牌！")
        elif joker == 1:
            print("游戏结束，玩家胜利，本局游戏中使用了1次joker，获得银牌！")
        else:
            print("游戏结束，玩家胜利，本局游戏中使用了2次joker，获得铜牌！")
print("输入1以再次开始游戏，输入其它以结束游戏")
again = input()
while (again == "1"):
    library, Bosses, discard_pile = Card.Initialize_Game()
    Players, limit = Get_Player_Number()
    while(not limit):
        Players, limit = Get_Player_Number()
    Joker = Card.card("Joker", 0)
    if limit < 8:
        for i in range(7 - limit):
            library.append(Joker)
        random.shuffle(library)
        CardMoves.Set_Cards(Players, library)
        boss = Bosses.pop(0)
        check = True
        order = 1
        while(check):
            order, boss = Battle.Complete_Process(boss, Players, order, library, discard_pile, Bosses, limit)
            if not order: # 注意order不会是0，所以不会出问题
                if boss:
                    print("游戏结束，玩家胜利")
                else:
                    print("游戏结束，玩家失败")
                check = False
    else: # 单人游戏
        joker = 2
        Player = []
        CardMoves.Set_Cards_1(Player, library)
        boss = Bosses.pop(0)
        check = True
        while(check):
            check, boss, joker = Battle.Complete_Process_1(boss, Player, library, discard_pile, Bosses, joker)
        if not boss:
            print("游戏结束，玩家失败")
        else:
            if joker == 2:
                print("游戏结束，玩家胜利，本局游戏中没有使用joker，获得金牌！")
            elif joker == 1:
                print("游戏结束，玩家胜利，本局游戏中使用了1次joker，获得银牌！")
            else:
                print("游戏结束，玩家胜利，本局游戏中使用了2次joker，获得铜牌！")
    print("输入1以再次开始游戏，输入其它以结束游戏")
    again = input()