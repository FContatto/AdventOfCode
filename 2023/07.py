def get_hand_type(hand):
    hand_dict = dict()
    n_j = 0
    for c in hand:
        n_j += (c=='J')
        hand_dict[c] = hand_dict.get(c, 0)
        hand_dict[c] +=1
    hand_ls = []
    for k,v in hand_dict.items():
        hand_ls.append((v,k))
    hand_ls = sorted(hand_ls)
    if len(hand_ls)==1:
        return 7 #five of a kind
    if len(hand_ls)==2:
        if n_j>0:
            return 7
        if hand_ls[0][0]==1:
            return 6 # four of a kind
        return 5 #full house
    if len(hand_ls)==5:
        if n_j>0:
            return 2
        return 1 #high card
    if len(hand_ls)==4:
        if n_j>0:
            return 4
        return 2 #one pair
    if hand_ls[2][0]==3:
        if n_j>0:
            return 6
        return 4 #three of a kind
    if n_j==1:
        return 5
    if n_j==2:
        return 6
    return 3 #two pair

card_to_num_dict = {'A':14, 'K':13, 'Q':12, 'J':1, 'T':10}

def cards_lt(h1, h2):
    for i in range(len(h1)):
        if h1[i] in card_to_num_dict:
            card_1 = card_to_num_dict[h1[i]]
        else:
            card_1 = int(h1[i])
        if h2[i] in card_to_num_dict:
            card_2 = card_to_num_dict[h2[i]]
        else:
            card_2 = int(h2[i])
        if card_1<card_2:
            return True
        if card_2<card_1:
            return False
    raise Exception('Cards are equal!')

class Hand:
    def __init__(self, h):
        self.h=h
    def __lt__(self, other):
        h_type_self = get_hand_type(self.h)
        h_type_other = get_hand_type(other.h)
        if h_type_self!=h_type_other:
            return h_type_self<h_type_other
        return cards_lt(self.h, other.h)

def sort_bets(words):
    hand_and_bets = []
    for w in words:
        h,b = w.split()
        hand_and_bets.append((Hand(h),int(b)))
    return sorted(hand_and_bets)

def calc_winnings(words):
    sorted_bets = sort_bets(words)
    total_win = 0
    for i,h_b in enumerate(sorted_bets):
        total_win += (i+1)*h_b[1]
    return total_win
 
print(calc_winnings(words))    