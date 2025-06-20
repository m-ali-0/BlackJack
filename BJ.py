import secrets, time
delay = .4

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
class Player:
    def __init__(self, name, deck):
        self.name = name
        self.hand = [deck.deal_card(), deck.deal_card()]
        
    def add_card(self, card):
        self.hand.append(card)

    def value(self):
        return hand_value(self.hand)

    def ToString(self):
        res = ''
        for card in self.hand:
            res += f'{call[card[0]]} of {card[1]}'
            if card != self.hand[-1]:
                res += ', '
        return res

    def show_hand(self, reveal_all=True):
        label = "Your" if self.name.lower() == "player" else f"{self.name}'s"
        if not reveal_all:
            return f"{label} hand: {call[self.hand[0][0]]} of {self.hand[0][1]}, ()?()"
        return f"{label} hand: {self.ToString()} (value: {self.value()})"

    def has_blackjack(self):
        return self.value() == 21 and len(self.hand) == 2

    def is_busted(self):
        return self.value() > 21


def type_text(text, delay=0.05,newline = True):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    if newline:
        print()

def sl(n):
    time.sleep(n)
       
def hand_value(hand):
    value = sum(values[card[0]] for card in hand)
    aces = sum(1 for card in hand if card[0] == 'A')
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value

 
def get_answer(forw):
    if forw == 'hs':
        type_text("Hit or Stand? ", newline = False)
        return input().lower()
    if forw == 'continue':
        type_text("Wanna play more?(yes or no): ", newline=False)
        return True if input() in {'yes','sure','why not','yes please','yepp'} else False 

def reveal(player, dealer):
    if player.has_blackjack() and dealer.has_blackjack():
        type_text(player.show_hand())
        type_text(dealer.show_hand())
        type_text("Both have Blackjack. It's a tie!")
        return True
    elif player.has_blackjack():
        type_text(player.show_hand())
        type_text(dealer.show_hand())
        type_text("Blackjack! You win!")
        return True
    elif dealer.has_blackjack():
        type_text(player.show_hand())
        type_text(dealer.show_hand())
        type_text("Dealer has Blackjack. You lose.")
        return True
    return False


def play_blackjack():
    deck = Deck()
    # player = [deck.deal_card(), deck.deal_card()]
    # dealer = [deck.deal_card(), deck.deal_card()]
    
    player = Player("Player",deck)
    dealer = Player('Dealer',deck)
    
    if reveal(player,dealer):
        return      

    type_text(player.show_hand())
    type_text(dealer.show_hand(reveal_all=False))
    
    # type_text(handToStr(player, "P")) #######
    # type_text(f"Dealer's hand: {call[dealer[0][0]]} of {dealer[0][1]}, ()?()")
    
    while player.value() < 21:
        move = get_answer('hs')
        if move in {'hit', 'h','yes','sure','yepp'}:
            player.add_card(deck.deal_card())
            type_text(player.show_hand())
        else:
            break

    if player.value() > 21:
        type_text("Bust! You lose.")
        return

    type_text(dealer.show_hand())
    while dealer.value() < 17:
        dealer.add_card(deck.deal_card())
        type_text(dealer.show_hand())

    pv = player.value()
    dv = dealer.value()

    if dv > 21 or pv > dv:
        type_text("You win!")
    elif pv < dv:
        type_text("Dealer wins.")
    else:
        type_text("It's a tie!")



def printer(txt):
    if txt == 'hi':
        sl(delay)
        type_text('-------------------------------------')
        type_text('Hello! Wanna lose some money ha? xaxa')
        sl(delay)
        type_text('Why not? Go ahead!')
        sl(delay)
        type_text('And don\'t forget to enjoy!')
        sl(delay)
        type_text('-------------------------------------')
        sl(delay)
        print('\n')
    else:
        print('\n'*1)
        type_text('-------------------------------------')
        sl(delay)
        type_text('Thanks for playing! Hope you enjoyed!')
        sl(delay)
        type_text('And see you later, alligator!')
        sl(delay)
        type_text('-------------------------------------')
        sl(delay)


def main():
    cont = True
    printer('hi')
    while cont:
        play_blackjack()
        cont = get_answer("continue")
        sl(delay)
    printer('bye')
    
try:
    main()
except KeyboardInterrupt as err:
    type_text('Program stopped by user. Thanks for playing!')
    exit()