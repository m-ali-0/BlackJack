import Utils

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


def play_blackjack(player, dealer, deck):
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
