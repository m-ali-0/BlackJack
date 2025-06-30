import Utils, Player, Deck, Game
delay = .4
 
deck = Deck.Deck()
player = Player.Player("Player",deck)
dealer = Player.Player('Dealer',deck)


def main():
    cont = True
    Utils.print_msg('hi')
    while cont:
        if not Game.play_blackjack(player, dealer, deck):
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
        
    Utils.print_msg('bye')
    
try:
    main()
except KeyboardInterrupt as err:
    Utils.type_text('Program stopped by user. Thanks for playing!')
    exit()