import secrets, Utils

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
    
 
