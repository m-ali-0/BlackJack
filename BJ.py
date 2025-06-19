import secrets

suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
values = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
    '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11
}
call = {
    'J' : 'Jack', 'Q' : 'Queen', 'K': 'King', 'A': 'Ace', '2': '2', '3': '3', 
    '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9', '10': '10'
}

class Deck:
    def __init__(self):
        self.cards = [(rank, suit) for suit in suits for rank in ranks]
        self.shuffle()
        
    def shuffle(self):
        for i in range(len(self.cards) - 1, 0, -1):
            j = secrets.randbelow(i + 1)
            self.cards[i], self.cards[j] = self.cards[j], self.cards[i]
            
    def deal_card(self):
        return self.cards.pop()
    
def hand_value(hand):
    value = sum(values[card[0]] for card in hand)
    aces = sum(1 for card in hand if card[0] == 'A')
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value

def handToString(hand):
    res = ''
    for card in hand:
        res += f'{call[card[0]]} of {card[1]}'
        if card != hand[-1]:
            res += ', '
    return res
    

def print_hand(hand, who = 'Dealer'):
    if who == 'P':
        print(f"Your hand: {handToString(hand)} (value: {hand_value(hand)})")
    else:
        print(f"Dealer's hand: {handToString(hand)} (value: {hand_value(hand)})")
    
def get_answer(forw):
    if forw == 'hs':
        return input("Hit or Stand? ").lower()
    if forw == 'continue':
        return True if input("Wanna play more?(yes or no): ")=='yes' else False 


def play_blackjack():
    deck = Deck()
    player = [deck.deal_card(), deck.deal_card()]
    dealer = [deck.deal_card(), deck.deal_card()]

    print_hand(player, "P") #######
    print(f"Dealer's hand: {call[dealer[0][0]]} of {dealer[0][1]}, ()?()")

    while hand_value(player) < 21:
        move = get_answer('hs')
        if move == 'hit':
            player.append(deck.deal_card())
            print_hand(player, "P")
        else:
            break

    if hand_value(player) > 21:
        print("Bust! You lose.")
        return

    print_hand(dealer)
    while hand_value(dealer) < 17:
        dealer.append(deck.deal_card())
        print_hand(dealer)

    pv = hand_value(player)
    dv = hand_value(dealer)

    if dv > 21 or pv > dv:
        print("You win!")
    elif pv < dv:
        print("Dealer wins.")
    else:
        print("It's a tie!")

cont = True
print('-------------------------------------')
print('Hello! Wanna lose some money ha? xaxa\nWhy not? Go ahead!\nAnd don\'t forget to enjoy!')
print('-------------------------------------')
print('\n'*1)

while cont:
    play_blackjack()
    cont = get_answer("continue")

print('\n'*1)
print('-------------------------------------')
print('Thanks for playing! Hope you enjoyed!\nAnd see you later, alligator!')
print('-------------------------------------')
