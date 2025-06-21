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
        self.secH = None
        self.secB = None
        self.splitcnt = 0
    
    def give_hand(self,deck):
        self.hand = [deck.deal_card(),deck.deal_card()]
      
    def addMoney(self, add=0, second = False):
        if second:
            self.pocket += self.secB * add
        else:
            self.pocket += self.bet * add
        
    def choose_bet(self, second = False):
        if second:
            self.secB = self.bet   ####### might be wrong ###########
        while not second:
            ans = get_answer('bet')
            amt = 100 if ans == '1' else amt = 250 if ans == '2' \
                else amt = 500 if ans == '3' else amt = 100 if ans == '4' \
                    else amt = int(ans)
            if amt < 50:
                type_text("Minimum bet is $50.")
            elif amt > self.pocket:
                type_text("You don't have enough money for that bet.")
            else:
                self.bet = amt
                break       
    
    def add_card(self, deck, second = False):
        if second:
            self.secH.append(deck.deal_card())
        else:
            self.hand.append(deck.deal_card())

    def value(self, second = False):
        if second:
            val = sum(values[card[0]] for card in self.secH)
            aces = sum(1 for card in self.secH if card[0] == 'A')
        else:
            val = sum(values[card[0]] for card in self.hand)
            aces = sum(1 for card in self.hand if card[0] == 'A')
        while val > 21 and aces:
            val -= 10
            aces -= 1
        return val
        

    def toString(self, hm, second = False):
        res = ''
        if hm == 'hand':
            if second:
                for card in self.secH:
                    res += f'{call[card[0]]} of {card[1]}'
                    if card != self.secH[-1]:
                        res += ', '
            else:
                for card in self.hand:
                    res += f'{call[card[0]]} of {card[1]}'
                    if card != self.hand[-1]:
                        res += ', '
        elif hm == 'money':
            res += f'${self.pocket}'
        return res

    def show_hand(self, reveal_all=True, hnd = 0):
        label = "Your" if self.name == "Player" else f"{self.name}'s"
        if not reveal_all:
            return f"{label} hand: {call[self.hand[0][0]]} of {self.hand[0][1]}, ()?()"
        if hnd == 1:
            return f"{label} first hand: {self.toString('hand')} (value: {self.value()})"
        elif hnd == 2:
            return f"{label} second hand: {self.toString('hand', second= True)} (value: {self.value(second = True)})"

        return f"{label} hand: {self.toString('hand')} (value: {self.value()})"

    def has_blackjack(self, ):
        return self.value() == 21 and len(self.hand) == 2

    def is_busted(self, second = False):
        if second:
            return self.value(True) > 21
        else:
            return self.value() > 21
    
    def can_split(self):
        res = self.can_double() and self.hand[0][0] == self.hand[1][0] and not self.splitcnt
        self.splitcnt +=1
        return  res
    
    def can_double(self, second = False):
        if second:
            return len(self.secH) == 2 and self.pocket >= self.secB
        else:
            return len(self.hand) == 2 and self.pocket >= self.bet
        
    def play_double(self, deck, second = False):
        if second:
            self.addMoney(-1, True)
            self.secB *= 2
            self.add_card(deck, True)
            type_text(self.show_hand(hnd=2))
        else:
            self.addMoney(-1)
            self.bet *= 2
            self.add_card(deck)
            if self.splitcnt: 
                type_text(self.show_hand())


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
        type_text("1.Hit    2.Stand ", newline = False)
        return input().strip()
    
    if forw == 'hsd':
        type_text('Which one do you choose?')
        type_text("1.Hit    2.Stand    3.Double ", newline = False)
        return input().strip()
    
    if forw == 'hsds':
        type_text('Which one do you choose?')
        type_text("1.Hit    2.Stand    3.Double    4.Split ", newline = False)
        return input().strip()
    
    if forw == 'continue':
        type_text("Wanna play more? 1.yes  or  2.no : ", newline=False)
        return True if input().strip() == '1' else False
    
    if forw == 'bet':
        type_text("How much do you want to bet?")
        # maybe not type text
        if player.pocket >= 1000:
            type_text("1.$100    2.$250    3.$500    4.$1000    5.custom (min $50)    : ", newline=False)
        elif player.pocket >= 500:
            type_text("1.$100    2.$250    3.$500    4.custom (min $50)    : ", newline=False)
        elif player.pocket >= 250:
            type_text("1.$100    2.$250    3.custom (min $50)    : ", newline=False)
        elif player.pocket >= 100:
            type_text("1.$100    2.custom (min $50)    : ", newline=False)
        else:
            type_text("custom (min $50)    : ", newline=False)
        return input().strip()
    
    if forw == 'restart':
        type_text('Do you want to restart the game? 1.yes or 2.no : ', newline=False)
        return input().strip()
        


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


def play_hand(player, deck):
    # first_turn = True
    # double = player.can_double()
    # split = player.can_split()
    
    while player.value() < 21:
        double = player.can_double()
        split = player.can_split()

        if split:
            move = get_answer('hsds')
        elif double:
            move = get_answer('hsd')
        else:
            move = get_answer('hs')
        
        if move == '1':
            player.add_card(deck)
            type_text(player.show_hand())
        elif move == '2':
            break
        elif move == '3' and double:
            player.addMoney(-1)
            player.bet *= 2
            
        
    

deck = Deck()
player = Player("Player",deck)
dealer = Player('Dealer',deck)


def play_blackjack():
    player.give_hand(deck)
    dealer.give_hand(deck)
    
    type_text(f'Your current balance is {player.toString('money')}')
    player.choose_bet()
    player.addMoney(add=-1)
    
    if reveal(player,dealer):
        return True

    type_text(player.show_hand())
    type_text(dealer.show_hand(reveal_all=False))
    
    # play_hand(player, deck)
    
    first_turn = True
    while player.value() < 21:
        double = first_turn and player.pocket >= player.bet
        move = get_answer('hsd') if double else get_answer('hs')
        
        
        if move == '1':
            player.add_card(deck)
            type_text(player.show_hand())
        elif move == '2': break
        elif move == '3' and double:
            player.addMoney(-1)
            player.bet *= 2
            player.add_card(deck)
            type_text(player.show_hand())
            break
        else:
            type_text('This is not an option rn.')
            continue
        first_turn = False

    if player.value() > 21:
        type_text("Bust! You lose.")
        if player.pocket < 50:
            type_text("You're out of money. Game over!")
            return False
        return True

    type_text(dealer.show_hand())
    while dealer.value() < 17:
        dealer.add_card(deck)
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
        return False
    return True


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
        if not play_blackjack():
            if get_answer('restart') == '1':
                player.pocket = 1000
                cont = True
                type_text('--------- Restarted with $1000 ---------')
                continue
            else:
                break
             
        cont = get_answer("continue")
        if cont:
            type_text('----------------Sure!-----------------')   
        
    print_msg('bye')
    
try:
    main()
except KeyboardInterrupt as err:
    type_text('Program stopped by user. Thanks for playing!')
    exit()