# -*- coding: utf-8 -*-
import random
from collections import defaultdict, Counter

class Card():
    def __init__(self, value, suit):
        """
        花色用英文「'h', 's', 'd', 'c'」("Hearts", "Spades", "Diamonds", "Clubs")來表示;
        點數的範圍是1~13
        """
        self.value=value
        self.suit=suit

    def __repr__(self):
        suits = {"h":"♡", "s":"♠", "d":"♢", "c":"♣"}
        values = {**{i:str(i) for i in range(2,10)}, **{10:'T', 11:'J',12:'Q', 13:'K', 1:'A'}}
        return values[self.value] + suits[self.suit]

    
class StardardDeck():
    def __init__(self):
        self.cards = [Card(value, suit) for value in range(1,14) for suit in 'hsdc']
        
    def __len__(self):
        return len(self.cards)
        
    def __getitem__(self, i):
        return self.cards[i]
    
    def __setitem__(self, i, val):
        self.cards[i] = val
                
    def __repr__(self):
        return ' '.join([card.__repr__() for card in self.cards])
        
    def draw(self, k=1):
        # 抽k張牌
        return [self.cards.pop() for _ in range(k)] 
        
class HandChecker():
    @staticmethod
    def groupby_suit(cards):
        """
        Group by 花色.
        Sample: [J♢, 8♣, 2♣, 4♠, 4♢]
        {'d': [4, 11], 'c': [2, 8], 's': [4]}
        """
        group = defaultdict(list)
        for card in cards:
            group[card.suit].append(card.value)
        return {k: sorted(v) for k, v in group.items()}
        
    @staticmethod
    def straight(rank):
        """
        判斷順子。
        Sample: rank = [2,3,4,5,5,6,12]
        return 6
        """
        rank = sorted(set(rank), reverse=True)
        for i in range(len(rank)-4):
            if rank[i]-rank[i+4]==4:
                return rank[i]
        return -1
    
    @staticmethod
    def judge_rank(cards):
        """
        給定list of cards, 判斷牌型
        回傳元組以方便比大小，認開頭判斷牌型
        (9, 順子最大數): 同花順
        (8, 四條數字,散牌): 四條
        (7, 三條數字, 二條數字): 葫蘆
        (6, 散牌5張): 同花
        (5, 順子最大數): 順子
        (4, 三條數字,散牌2張): 三條
        (3, 二條數字1, 二條數字2, 散牌): 兩對
        (2, 二條數字, 散牌3張): 一對
        (1, 散牌5張): 散牌
        """
        suit_gp = HandChecker.groupby_suit(cards)
        
        """
        Note: 這個地方容易出錯，rank是取出牌面點數，不看花色，
        用來判斷是不是順子，但是判斷順子時，A可以視為14或1，
        因為A2345 及 TJQKA 都是合法的順子，故牌面值有A時，14跟1都應該記錄
        """
        rank =  [card.value for card in cards]
        rank = rank+[14]*rank.count(1)
        
        flush = [k for k,v in suit_gp.items() if len(v)>=5] # 取出滿足同花的花色
        flit = lambda L, d: [e for e in L if e!=d]
        sr = flit([HandChecker.straight(suit_gp[f]) for f in flush], -1)
        if sr:
            return (9, max(sr)) # 同花順
            
        cnt_rank = Counter(flit(rank,1)) #注意比大小時，A應視為14而非1
        kinds = {i:sorted([k for k,v in cnt_rank.items() if v==i]) for i in range(1,5)}
        if kinds[4]:
            return (8, kinds[4][-1], max([r for r in cnt_rank if r!=kinds[4][-1]]))
        if len(kinds[3])>=2 or kinds[3] and kinds[2]:
            return (7, kinds[3][-1], max(e for e in kinds[3]+kinds[2] if e!=kinds[3][-1]))
        if flush:
            """
            同花比大小也要將A應視為14而非1
            """
            return (6, *max([sorted((14 if num==1 else num) for num in suit_gp[f])[-5:][::-1] for f in flush]))
        st = HandChecker.straight(rank)
        if st!=-1:
            return (5,st)
        if kinds[3]:
            return (4, kinds[3][-1], *kinds[1][-2:][::-1])
        if len(kinds[2])>=2:
            return (3, kinds[2][-1], kinds[2][-2], kinds[1][-1])
        if kinds[2]:
            return (2, kinds[2][-1], *kinds[1][-3:][::-1])
        return (1,*kinds[1][-5:][::-1])
            
    
if __name__=='__main__':
    deck = StardardDeck()
    print("標準撲克牌:", deck)
    random.shuffle(deck)
    print("把牌堆洗亂: ", deck)
    randomCard = deck.draw()
    print("抽出最上方的牌:", randomCard)
    print("剩下的牌為:" ,deck)
    cards = deck.draw(7)
    print(cards)
    print(HandChecker.groupby_suit(cards))
    print(HandChecker.judge_rank(cards))
