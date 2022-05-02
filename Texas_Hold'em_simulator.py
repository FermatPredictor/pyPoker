# -*- coding: utf-8 -*-
import random
import time
from collections import Counter
from poker import Card, StardardDeck, HandChecker

def percent_dict(d):
    """
    input一個dict, 回傳每個key值所占百分比
    """
    total = sum(d.values())
    return {k:v*100/total for k,v in d.items()}

def input_card(s):
    """
    用浮點數字串表示一張牌，方便輸入，
    如3.12，表示紅心Q，
    第一個數字表示花色、第二個數字表示數字
    """
    suit, value = s.split('.')
    d = {'1':'c', '2':'d', '3':'h', '4':'s'}
    return Card(int(value), d[suit])
    
    
def simulate_game(myCard, n, field):
    """
    給定我們的手牌(2張)，參與對手數量n，場上牌，
    模擬一場遊戲並回傳我們手牌的名次
    """
    deck = StardardDeck()
    deck = [card for card in deck if card not in myCard+field]
    random.shuffle(deck)
    others = [[deck.pop() for _ in range(2)] for _ in range(n)]
    simulate_field = field+[deck.pop() for _ in range(5-len(field))] 
    my_types = HandChecker.judge_rank(myCard+simulate_field)
    hand_types = sorted(set([HandChecker.judge_rank(hand+simulate_field) for hand in others]+[my_types]), reverse=True)
    ranking = hand_types.index(my_types)+1
    
#    print(f"隨機模擬其它人的手牌: {others}")
#    print(f"隨機模擬公共牌: {simulate_field}")
#    print(f"隨機模擬我方牌型: {myCard+simulate_field}, {my_types}")
#    for hand in others:
#        print(f"隨機模擬他方牌型: {hand+simulate_field}, {HandChecker.judge_rank(hand+simulate_field)}")
#    print(hand_types)
#    print(f"本次模擬中，我方名次: {ranking}")
    
    return ranking

def batch_simulate_game(myCard, n, field, game_num=1000):
    start = time.time()
    p_cnt = percent_dict(Counter([simulate_game(myCard, n, field) for i in range(game_num)]))
    ev = sum(i*p_cnt.get(i, 0) for i in range(1, n+2))/100
    end = time.time() - start
    
    print(f"我的手牌為: {myCard}, 公共牌為: {field}")
    for i in range(1, n+2):
        print(f"模擬牌型獲得第{i}名的概率為: {p_cnt.get(i, 0)}%")
    print(f"期望值= {ev}名(分析時間: {round(end,2)}秒)")


def main():
    while True:
        i_str = input("請輸入你的手牌及其它參與牌局人數(格式範例: 1.5 2.7 5)")
        *myCard, n = i_str.strip().split()
        myCard = [input_card(s) for s in myCard]
        n = int(n)
        batch_simulate_game(myCard, n, [])
        
        try:
            i_str = input("請輸入前三張公共牌: ")
            field = [input_card(s) for s in i_str.strip().split()]
            batch_simulate_game(myCard, n, field)
        except:
            continue
        
        try:
            i_str = input("請輸入第四張公共牌: ")
            field.append(input_card(i_str.strip()))
            batch_simulate_game(myCard, n, field)
        except:
            continue
        
        try:
            i_str = input("請輸入第五張公共牌: ")
            field.append(input_card(i_str.strip()))
            batch_simulate_game(myCard, n, field)
        except:
            continue
     

if __name__=='__main__':
    main()
