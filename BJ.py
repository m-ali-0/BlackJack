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
    def __init__(self, num_decks=6):
        self.cards = []
        self.num_decks = num_decks
        self._reset_deck()
        
    def _reset_deck(self):
        self.cards = [(rank, suit) for _ in range(self.num_decks) for suit in suits for rank in ranks]
        self.shuffle()
    
    def shuffle(self):
        for i in range(len(self.cards) - 1, 0, -1):
            j = secrets.randbelow(i + 1)
            self.cards[i], self.cards[j] = self.cards[j], self.cards[i]
            
    def deal_card(self):
        if len(self.cards) < self.num_decks * 52 * 0.25: 
            type_text("Shuffling cards...", delay=0.02)
            self._reset_deck()
        return self.cards.pop()
    
class Player:
    def __init__(self, name, deck, pocket = 1000, bet = 0):
        self.name = name
        self.hand = [deck.deal_card(), deck.deal_card()]
        self.pocket = pocket
        self.bet = bet
        
    def addMoney(self, add=0):
        self.pocket += self.bet * add
        
    def choose_bet(self):
        while True:
            ans = get_answer('bet')
            if ans == '1':
                amt = 100
            elif ans == '2':
                amt = 250
            elif ans == '3':
                amt = 500
            elif ans == '4':
                amt = 1000
            else:
                amt = int(ans)
            if amt < 50:
                type_text("Minimum bet is $50.")
            elif amt > self.pocket:
                type_text("You don't have enough money for that bet.")
            else:
                self.bet = amt
                break

            
    
    def add_card(self, card):
        self.hand.append(card)

    def value(self):
        val = sum(values[card[0]] for card in self.hand)
        aces = sum(1 for card in self.hand if card[0] == 'A')
        while val > 21 and aces:
            val -= 10
            aces -= 1
        return val
        

    def toString(self, hm):
        res = ''
        if hm == 'hand':
            for card in self.hand:
                res += f'{call[card[0]]} of {card[1]}'
                if card != self.hand[-1]:
                    res += ', '
        elif hm == 'money':
            res += f'${self.pocket}'
        return res

    def show_hand(self, reveal_all=True):
        label = "Your" if self.name.lower() == "player" else f"{self.name}'s"
        if not reveal_all:
            return f"{label} hand: {call[self.hand[0][0]]} of {self.hand[0][1]}, ()?()"
        return f"{label} hand: {self.toString('hand')} (value: {self.value()})"

    def has_blackjack(self):
        return self.value() == 21 and len(self.hand) == 2

    def is_busted(self):
        return self.value() > 21


def type_text(text, delay=0.03, newline = True, width = 100):
    if width:
        pad = (width - len(text)) // 2
        print(' ' * pad, end='') 
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    if newline:
        print()

def sl(n):
    time.sleep(n)

 
def get_answer(forw):
    if forw == 'hs':
        type_text('Which one do you choose?')
        type_text("1.Hit    2.Stand    3.Double ", newline = False)
        return input().lower()
    if forw == 'continue':
        type_text("Wanna play more? 1.yes  or  2.no : ", newline=False)
        return True if input() == '1' else False
    if forw == 'bet':
        type_text("How much do you want to bet?")
        # maybe not type text
        type_text("1.$100    2.$250    3.$500    4.$1000    5.custom (min $50)    : ", newline=False)
        return input()

        


def reveal(player, dealer):
    if player.has_blackjack() and dealer.has_blackjack():
        type_text(player.show_hand())
        type_text(dealer.show_hand())
        type_text("Both have Blackjack. It's a tie!")
        player.addMoney(add = 1)
        return True
    elif player.has_blackjack():
        type_text(player.show_hand())
        type_text(dealer.show_hand())
        type_text("Blackjack! You win!")
        player.addMoney(add = 2.5)
        return True
    elif dealer.has_blackjack():
        type_text(player.show_hand())
        type_text(dealer.show_hand())
        type_text("Dealer has Blackjack. You lose.")
        return True
    return False


deck = Deck()
player = Player("Player",deck)
dealer = Player('Dealer',deck)


def play_blackjack():
    player.hand = [deck.deal_card(), deck.deal_card()]
    dealer.hand = [deck.deal_card(), deck.deal_card()]

    
    type_text(f'Your current balance is {player.toString('money')}')
    player.choose_bet()
    player.addMoney(add=-1)
    
    if reveal(player,dealer):
        return      

    type_text(player.show_hand())
    type_text(dealer.show_hand(reveal_all=False))
    
    
    while player.value() < 21:
        move = get_answer('hs')
        if move == '1':
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
        player.addMoney(add=2)
    elif pv < dv:
        type_text("Dealer wins.")
    else:
        type_text("It's a tie!")
        player.addMoney(add=1)
    
    if player.pocket < 50:
        type_text("You're out of money. Game over!")
        return



def print_msg(txt):
    if txt == 'hi':
        # sl(delay)
        type_text('-------------------------------------')
        type_text('Hello! Wanna lose some money ha? xaxa')
        # sl(delay)
        type_text('Why not? Go ahead!')
        # sl(delay)
        type_text('And don\'t forget to enjoy!')
        # sl(delay)
        type_text('-------------------------------------')
        # sl(delay)
        print('\n')
    else:
        print('\n'*1)
        type_text('-------------------------------------')
        # sl(delay)
        type_text('Thanks for playing! Hope you enjoyed!')
        # sl(delay)
        type_text('And see you later, alligator!')
        # sl(delay)
        type_text('-------------------------------------')
        # sl(delay)


def main():
    cont = True
    print_msg('hi')
    while cont:
        play_blackjack()
        cont = get_answer("continue")
        if cont:
            type_text('----------------Sure!-----------------')   
        
    print_msg('bye')
    
try:
    main()
except KeyboardInterrupt as err:
    type_text('Program stopped by user. Thanks for playing!')
    exit()