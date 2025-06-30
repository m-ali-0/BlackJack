import time

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




def type_text(text, delay=0.005, newline = True, width = 100):
    if width:
        pad = (width - len(text)) // 2
        print(' ' * pad, end='') 
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    if newline:
        print()
        
        
def get_answer(forw, pocket = None):
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
        if pocket >= 1000:
            type_text("1.$100    2.$250    3.$500    4.$1000    5.custom (min $50)    : ", newline=False)
        elif pocket >= 500:
            type_text("1.$100    2.$250    3.$500    4.custom (min $50)    : ", newline=False)
        elif pocket >= 250:
            type_text("1.$100    2.$250    3.custom (min $50)    : ", newline=False)
        elif pocket >= 100:
            type_text("1.$100    2.custom (min $50)    : ", newline=False)
        else:
            type_text("custom (min $50)    : ", newline=False)
        return input().strip()
    
    if forw == 'restart':
        type_text('Do you want to restart the game? 1.yes or 2.no : ', newline=False)
        return input().strip()
        
