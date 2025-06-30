import secrets, time, Utils, Player
delay = .4


class Deck:
    def __init__(self, num_decks=6):
        self.cards = []
        self.num_decks = num_decks
        self._reset_deck()
        
    def _reset_deck(self):
        self.cards = [(rank, suit) for _ in range(self.num_decks) for suit in Utils.suits for rank in Utils.ranks]
        self.shuffle()
    
    def shuffle(self):
        for i in range(len(self.cards) - 1, 0, -1):
            j = secrets.randbelow(i + 1)
            self.cards[i], self.cards[j] = self.cards[j], self.cards[i]
            
    def deal_card(self):
        if len(self.cards) < self.num_decks * 52 * 0.25: 
            Utils.type_text("Shuffling cards...", delay=0.02)
            self._reset_deck()
        return self.cards.pop()
    
 

def reveal(player, dealer):
    if player.has_blackjack() and dealer.has_blackjack():
        Utils.type_text(player.show_hand())
        Utils.type_text(dealer.show_hand())
        Utils.type_text("Both have Blackjack. It's a tie!")
        player.addMoney(add = 1)
        return True
    elif player.has_blackjack():
        Utils.type_text(player.show_hand())
        Utils.type_text(dealer.show_hand())
        Utils.type_text("Blackjack! You win!")
        player.addMoney(add = 2.5)
        return True
    elif dealer.has_blackjack():
        Utils.type_text(player.show_hand())
        Utils.type_text(dealer.show_hand())
        Utils.type_text("Dealer has Blackjack. You lose.")
        return True
    return False


    

deck = Deck()
player = Player.Player("Player",deck)
dealer = Player.Player('Dealer',deck)


def play_blackjack():
    player.give_hand(deck)
    dealer.give_hand(deck)
    
    player.secH = []
    player.splitcheck = 0
    player.splitted = False
    
    Utils.type_text(f'Your current balance is {player.toString('money')}')
    player.choose_bet()
    player.addMoney(add=-1)
    
    if reveal(player,dealer):
        return True

    Utils.type_text(player.show_hand())
    Utils.type_text(dealer.show_hand(reveal_all=False))
    
    player.play_hand(deck)
    

    if player.value() > 21:
        Utils.type_text("Bust! You lose.")
        if player.pocket < 50:
            Utils.type_text("You're out of money. Game over!")
            return False
        return True

    Utils.type_text(dealer.show_hand())
    while dealer.value() < 17:
        dealer.add_card(deck)
        Utils.type_text(dealer.show_hand())

    pv = player.value()
    dv = dealer.value()
    
    if player.splitted:
        for i, second in enumerate([False, True], 1):
            pv = player.value(second)
            result_text = f"First" if i == 1 else "Second"
            if pv > 21:
                Utils.type_text(f"{result_text} hand busts! You lose.")
            elif dv > 21 or pv > dv:
                Utils.type_text(f"{result_text} hand wins!")
                player.addMoney(add=2, second=second)
            elif pv < dv:
                Utils.type_text(f"{result_text} hand loses.")
            else:
                Utils.type_text(f"{result_text} hand ties.")
                player.addMoney(add=1, second=second)
    else:
        
        if dv > 21 or pv > dv:
            Utils.type_text("You win!")
            player.addMoney(add=2)
        elif pv < dv:
            Utils.type_text("Dealer wins.")
        else:
            Utils.type_text("It's a tie!")
            player.addMoney(add=1)
    
    if player.pocket < 50:
        Utils.type_text("You're out of money. Game over!")
        return False
    return True


def print_msg(txt):
    if txt == 'hi':
        Utils.type_text('-------------------------------------')
        Utils.type_text('Hello! Wanna lose some money ha? xaxa')
        Utils.type_text('Why not? Go ahead!')
        Utils.type_text('And don\'t forget to enjoy!')
        Utils,Utils.type_text('-------------------------------------')
        print('\n')
    else:
        print('\n'*1)
        Utils.type_text('-------------------------------------')
        Utils.type_text('Thanks for playing! Hope you enjoyed!')
        Utils.type_text('And see you later, alligator!')
        Utils.type_text('-------------------------------------')


def main():
    cont = True
    print_msg('hi')
    while cont:
        if not play_blackjack():
            if Utils.get_answer('restart') == '1':
                player.pocket = 1000
                cont = True
                Utils.type_text('--------- Restarted with $1000 ---------')
                continue
            else:
                break
             
        cont = Utils.get_answer("continue")
        if cont:
            Utils.type_text('----------------Sure!-----------------')   
        
    print_msg('bye')
    
try:
    main()
except KeyboardInterrupt as err:
    Utils.type_text('Program stopped by user. Thanks for playing!')
    exit()