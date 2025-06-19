import secrets

suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
values = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
    '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11
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

def print_hand(hand, who):
    print(f"{who}'s hand: {hand} (value: {hand_value(hand)})")


def play_blackjack():
    deck = Deck()
    player = [deck.deal_card(), deck.deal_card()]
    dealer = [deck.deal_card(), deck.deal_card()]

    print_hand(player, "Player")
    print(f"Dealer's hand: [{dealer[0]}, ('?', '?')]")

    while hand_value(player) < 21:
        move = input("Hit or Stand? ").lower()
        if move == 'hit':
            player.append(deck.deal_card())
            print_hand(player, "Player")
        else:
            break

    if hand_value(player) > 21:
        print("Bust! You lose.")
        return

    print_hand(dealer, "Dealer")
    while hand_value(dealer) < 17:
        dealer.append(deck.deal_card())
        print_hand(dealer, "Dealer")

    pv = hand_value(player)
    dv = hand_value(dealer)

    if dv > 21 or pv > dv:
        print("You win!")
    elif pv < dv:
        print("Dealer wins.")
    else:
        print("It's a tie!")

play_blackjack()