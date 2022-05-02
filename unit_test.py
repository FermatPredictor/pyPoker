# -*- coding: utf-8 -*-
import random
from collections import Counter
import unittest
from poker import Card, StardardDeck, HandChecker

def percent_dict(d):
    """
    input一個dict, 回傳每個key值所占百分比
    """
    total = sum(d.values())
    return {k:v*100/total for k,v in d.items()}


class Test(unittest.TestCase):

    def test_basic(self):
        """
        基礎牌型測試
        """
        test_case = [
        [[Card(2,'c'), Card(3,'c'), Card(3,'d'),  Card(4,'d'), Card(4,'c'), Card(5,'c'), Card(1,'c')], (9,5)],
        [[Card(10,'c'), Card(10,'d'), Card(10,'h'),  Card(10,'s'), Card(7,'c'), Card(7,'d'), Card(2,'c')], (8,10,7)],
        [[Card(10,'c'), Card(10,'d'), Card(10,'h'),  Card(7,'s'), Card(7,'c'), Card(7,'d'), Card(1,'c')], (7,10,7)],
        [[Card(2,'d'), Card(5,'d'), Card(7,'d'),  Card(9,'d'), Card(9,'s'), Card(1,'d')], (6,14,9,7,5,2)],
        [[Card(1,'c'), Card(2,'s'), Card(3,'d'),  Card(4,'s'), Card(5,'d'), Card(8,'c'), Card(1,'c')], (5,5)],
        [[Card(10,'c'), Card(11,'s'), Card(12,'d'),  Card(13,'s'), Card(1,'d'), Card(8,'c'), Card(1,'c')], (5,14)],
        [[Card(2,'d'), Card(3,'h'), Card(4,'h'),  Card(6,'s'), Card(7,'d'), Card(1,'d'), Card(13,'c')], (1,14,13,7,6,4)]
        ]
        for hand, ans in test_case:
            self.assertEqual(HandChecker.judge_rank(hand), ans) 
        
    def test_prob_5(self):
        """
        用程試測試隨機五張牌的牌型概率，與數學算出來的理論值比較
        各牌型的出現概率如下:
        
        straight flush    0.0014%
        four of a kind    0.0240%
        full house        0.1441%
        flush             0.1965%
        straight          0.3925%
        three of a kind   2.1128%
        two pair          4.7539%
        one pair          42.2569%
        high card         50.1177%
        
        五~七張牌的機率: https://home.gamer.com.tw/creationDetail.php?sn=3828045
        """
        print()
        print("test prob of five card...")
        deck = StardardDeck()
        cnt = Counter()
        for _ in range(100000):
            random.shuffle(deck)
            hand = HandChecker.judge_rank(deck[:5])
            cnt[hand[0]] += 1
        
        p_cnt = percent_dict(cnt)
        for i in range(9,0,-1):
            print(i, p_cnt.get(i,0))
        print("End test prob of five card...")
        
    def test_prob_7(self):
        """
        用程試測試隨機七張牌的牌型概率，與數學算出來的理論值比較
        各牌型的出現概率如下:
        
        straight flush    0.0311%
        four of a kind    0.1681%
        full house        2.5961%
        flush             3.0255%
        straight          4.6194%
        three of a kind   4.8299%
        two pair          23.4955%
        one pair          43.8225%
        high card         17.4119%
        
        五~七張牌的機率: https://home.gamer.com.tw/creationDetail.php?sn=3828045
        """
        print()
        print("test prob of 7 card...")
        deck = StardardDeck()
        cnt = Counter()
        for _ in range(100000):
            random.shuffle(deck)
            hand = HandChecker.judge_rank(deck[:7])
            cnt[hand[0]] += 1
        
        p_cnt = percent_dict(cnt)
        for i in range(9,0,-1):
            print(i, p_cnt.get(i,0))
        print("End test prob of 7 card...")


if __name__ == '__main__':
    unittest.main()