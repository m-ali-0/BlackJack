import Utils

class Player:
    def __init__(self, name, deck, pocket = 1000, bet = 0):
        self.name = name
        self.hand = [deck.deal_card(), deck.deal_card()]
        self.pocket = pocket
        self.bet = bet
        self.secH = []
        self.secB = None
        self.splitcheck = 0
        self.splitted = False
    
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
            ans = Utils.get_answer('bet', self.pocket)
            if ans == '1': amt = 100
            elif ans == '2': amt = 250
            elif ans == '3': amt = 500
            elif ans == '4': amt = 1000
            elif ans.strip().isdigit(): amt = int(ans.strip())
            else: 
                Utils.type_text('Enter valid answer you mf!:')
                amt = 0
                
            if amt < 50:
                Utils.type_text("Minimum bet is $50.")
            elif amt > self.pocket:
                Utils.type_text("You don't have enough money for that bet.")
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
            val = sum(Utils.values[card[0]] for card in self.secH)
            aces = sum(1 for card in self.secH if card[0] == 'A')
        else:
            val = sum(Utils.values[card[0]] for card in self.hand)
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
                    res += f'{Utils.call[card[0]]} of {card[1]}'
                    if card != self.secH[-1]:
                        res += ', '
            else:
                for card in self.hand:
                    res += f'{Utils.call[card[0]]} of {card[1]}'
                    if card != self.hand[-1]:
                        res += ', '
        elif hm == 'money':
            res += f'${self.pocket}'
        return res

    def show_hand(self, reveal_all=True, hnd = 0):
        label = "Your" if self.name == "Player" else f"{self.name}'s"
        if not reveal_all:
            return f"{label} hand: {Utils.call[self.hand[0][0]]} of {self.hand[0][1]}, ()?()"
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
    
    def play_hand(self, deck, second = False):
    
    
        while self.value() < 21:
            double = self.can_double()
            split = self.can_split() 

            if split:
                move = Utils.get_answer('hsds')
            elif double:
                move = Utils.get_answer('hsd')
            else:
                move = Utils.get_answer('hs')
        
            if move == '1':
                self.add_card(deck, second)
                if not second:
                    Utils.type_text(self.show_hand())
                else: 
                    Utils.type_text(self.show_hand(hnd=2))
            elif move == '2':
                break
            elif move == '3' and double:
                self.play_double(deck)
                break
            elif move == '4' and split:
                self.play_split(deck)
                break
            

    
    def can_split(self):
        res = self.can_double() and self.hand[0][0] == self.hand[1][0]\
            and not self.splitcheck
        self.splitcheck +=1
        return  res
    
    def play_split(self, deck):
        self.splitted = True
        self.secH.append(self.hand.pop())
        self.secB = self.bet
        self.addMoney(-1)
        
        self.add_card(deck)
        Utils.type_text(self.show_hand(hnd=1))
        self.play_hand(deck)
        
        self.add_card(deck,True)
        Utils.type_text(self.show_hand(hnd=2))
        self.play_hand(deck, True)
        
    
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
            Utils.type_text(self.show_hand(hnd=2))
        else:
            self.addMoney(-1)
            self.bet *= 2
            self.add_card(deck)
            if not self.splitted: 
                Utils.type_text(self.show_hand())
            else: 
                Utils.type_text(self.show_hand(hnd= 1))
                
    