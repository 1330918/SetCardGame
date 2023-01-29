#%%
# ------------------
# IMPORTING MODULES
# ------------------

import numpy as np
import itertools
import pygame as pg
import sys

#-------------------------------------
# DEFINITION OF CLASSES AND FUNCTIONS
# ------------------------------------

class Card:
    """Creates a single card."""   
    def __init__(self, colour, shape, filling, number):
        """Initialize card attributes.
            > Arguments:
                colour, shape, filling, number -> to be defined in lists."""
        self.c = colour
        self.s = shape
        self.f = filling
        self.n = number
        
    def __str__(self):
        """Returns a string of the card."""
        return self.c + self.s + self.f + self.n
      
class Deck:
    """This class makes a card deck and it has executable methods that are used in the SET card game."""
    def __init__(self):
        """Initialize deck attributes."""
        self.all_cards = []
        self.build()
        
    def build(self):
        """Building up the deck from single cards.
           Creates a dictionary with the vector combinations of all cards in the deck."""          
        global vector_dict
        vector_dict = {}
        v = 0
        for i, c in enumerate(colours):
            for j, s in enumerate(shape):
                for k, f in enumerate(filling):
                    for l, n in enumerate(number):
                            C = Card(c, s, f, n)
                            self.all_cards.append(str(C))
                            vector_dict.update({v: [i,j,k,l]})
                            v += 1
        
    def aslist(self):
        """Returns the deck as a list."""
        return self.all_cards
    
    def shuffle():
        """Shuffles the deck."""
        deck = Deck().aslist()
        np.random.shuffle(deck)
        return deck

    def comparison(deck_to_compare):
        """Compares twelve cards by their vector values.
           Returns boolean lists for the comparison of three cards with each other.
            > Arguments:
                deck_to_compare -> the deck from which to compare the cards."""
        normal_deck = Deck().aslist()
        card_vectors = []
        for x in range(12):
            index = normal_deck.index(deck_to_compare[x])
            card_vectors.append(vector_dict[index])
                        
        def iterate_dict(D):
            """Makes an iterative dictionary, where each iteration yields a new dictionary.
                > Arguments:
                    D -> dictionary to iterate."""
            keys, values = zip(*D.items())
            for row in itertools.product(*values):
                yield dict(zip(keys, row))
         
        # create dictionaries of all possible card combinations        
        C = {"card1": card_vectors[:], "card2": card_vectors[1:], "card3": card_vectors[2:]}       
        C_lst = list(iterate_dict(C))
        
        # make boolean lists that include the similarities and differences between the card vectors
        # comparison1 compares card one and card two
        # comparison2 compares card two and card three
        # comparison3 compares card one and card three
        comparison1 = []; comparison2 = []; comparison3 = []       
        for j in range(len(C_lst)):
            if card_vectors.index(C_lst[j]['card1']) < card_vectors.index(C_lst[j]['card2']) < card_vectors.index(C_lst[j]['card3']):
                for i in range(4):
                    comparison1.append(C_lst[j]['card1'][i] == C_lst[j]['card2'][i])
                    comparison2.append(C_lst[j]['card2'][i] == C_lst[j]['card3'][i])
                    comparison3.append(C_lst[j]['card1'][i] == C_lst[j]['card3'][i])
        return comparison1, comparison2, comparison3
    
    def all_sets(deck_to_compare):
        """Returns all possible SETs in the current twelve cards.
            > Arguments:
                deck_to_compare -> the deck from which to search for SETs."""
        comparison1, comparison2, comparison3 = Deck.comparison(deck_to_compare)
        SETlist = []
        
        # every card consists of four vectors, so the comparison between cards should only look at four values at a time
        check1 = 0; check2 = 4    
        while check2 <= len(comparison1):
            # if the comparison between all cards matches, it is a SET
            if comparison1[check1:check2] == comparison2[check1:check2] == comparison3[check1:check2]:
                SETlist.append(True)
            else:   
                SETlist.append(False)
            check1 += 4
            check2 += 4
            
        # find the numerical combination of cards that correspond to the SET
        # first, create a dictionary for all possible combinations (sorted from low to high)
        combinationsdict = {}
        p = 0
        for i in range(1,13):
            for j in range(i+1, 13):
                for k in range(j+1, 13):
                    combinationsdict.update({p:[i,j,k]})
                    p += 1 
        # find the indices at which three cards form a SET
        # these indices correspond to the indices in the combinations dictionary, so that we know which exact three cards form a SET
        indices = [i for i, x in enumerate(SETlist) if x == True]        
        sets = []
        for index in indices:
            sets.append(combinationsdict[index])
        return sets
        
    def one_set(deck_to_compare):
        """Returns a single SET, randomly chosen from the possible SETs.
            > Arguments:
                deck_to_compare -> the deck from which to search for SETs."""
        sets = Deck.all_sets(deck_to_compare)
        if len(sets) > 0:
            nr = np.random.randint(len(sets))
            oneset = sets[nr]
            return oneset

class Label():
    """Creates labels to display on the Pygame window."""
    def __init__(self, text, location, background, txtcolour, font, fontsize, size, bold=False, italic=False, underline=False):
        """Initialize label attributes.
            > Arguments:
                text, location, background, txtcolour, font, fontsize,
                size, bold, italic, underline -> all text characteristics."""
        self.font = pg.font.SysFont(font, fontsize, bold, italic)
        if underline == True:
            self.font.set_underline(True)
        self.text = text
        self.colour = txtcolour
        self.bg = background
        self.size = size
        self.loc = location
        
        self.text_txt = self.font.render(self.text, True, self.colour)
        self.text_rect = self.text_txt.get_rect(center=[s//3 for s in self.size])
        self.surface = pg.surface.Surface(size)
        self.rect = self.surface.get_rect(center=[l for l in self.loc]) 
        
    def draw(self):
        """Display the label on the screen."""
        self.surface.fill(self.bg)
        self.surface.blit(self.text_txt, self.text_rect)
        screen.blit(self.surface, self.rect)
    
    def update(self, new_text="", transparent=None):
        """Update a label with new text.
            > Arguments: 
                new_text -> the text that will be displayed.
                transparent -> makes the text surface transparent."""
        self.text = new_text
        self.text_txt = self.font.render(self.text, True, self.colour)
        if transparent == True:
            self.rect = pg.draw.rect(screen, black, self.rect, 1)
            screen.blit(self.text_txt, self.rect)           
        else:
            self.surface.fill(self.bg)
            self.surface.blit(self.text_txt, self.text_rect)
            screen.blit(self.surface, self.rect)

class Game():
    """Class that controls the actions within a Set game."""
    def __init__(self, SETchoice=None, countdown=False):
        """Initialize game attributes.
            > Arguments:
                SETchoice -> the choice of SET by a player.
                countdown -> if True, the counter has reached zero and the computer finds a SET."""
        self.sets = Deck.all_sets(used_cards)
        self.one_set = Deck.one_set(used_cards)
        if not countdown:
            self.choice = SETchoice
        if countdown:
            self.choice = self.one_set
        
    def is_set(self):
        """Checks whether the chosen SET is valid."""
        print("choice is", self.choice)
        if self.choice in self.sets:
            found_set = True
        else:
            found_set = False
        return found_set  
            
    def change_cards(self):
        """Replaces the cards from the chosen SET with new cards from the original deck.
           Displays the new cards on the screen.
           Checks for a Cap Set, and replace cards if needed.
           Keeps track of the number of cards left in the game."""
        new_cards = []
        # replace the three chosen cards with new cards and load the new cards on the screen
        for i in range(3):
            card = pg.image.load('ProgWis/Cards/' + cards[0] + '.png')
            screen.blit(card, (margins[self.choice[i]-1][0], margins[self.choice[i]-1][1]))
            new_cards.append(cards.pop(0))
            # len(used_cards) should always be twelve in order to compare the correct cards for a SET
            used_cards.remove(used_cards[self.choice[i]-(i+1)])
        # replace the removed used cards with the new cards
        for j in range(3):
            used_cards.insert(self.choice[j]-1, new_cards[j])
        # find SETs within the new used cards deck
        self.sets = Deck.all_sets(used_cards)
        self.one_set = Deck.one_set(used_cards)
        
        # Cap Set scenario
        while len(self.sets) == 0 and len(cards) > 0:
            # print("------------NO SETS-------------") ## OPTIONAL PRINT
            R = 0
            new_cards = [0 for K in range(12)]
            # make sure the new cards are the three right-sided cards
            # these cards have positions 3, 7 and 11 (cards 4, 8 and 12)
            # repeat the card replacement steps
            for k in range(3, 12, 4):
                extra_card = pg.image.load('ProgWis/Cards/' + cards[0] + '.png')
                screen.blit(extra_card, (margins[k][0], margins[k][1]))
                new_cards[k] = cards.pop(0)
                del used_cards[k-R]
                R += 1
            for l in range(3, 12, 4):
                used_cards.insert(l, new_cards[l])
            self.sets = Deck.all_sets(used_cards)
            self.one_set = Deck.one_set(used_cards)
            if len(self.sets) > 0:
                break
        
        # empty the choice list and update the number of cards
        self.choice = []    
        print(self.sets) ## OPTIONAL PRINT
        cards_left_label.update(f"Number of cards left: {len(cards)}")
        pg.display.update()
        
        # the game ends if there are no cards left
        if len(cards) == 0:
            Game.lost_or_won()           
            
    def lost_or_won():
        """This function marks the finished game and all processes are stopped.
           Updates the screen display with a win, lose or tie message."""
        game_finish_label.draw()
        # a player wins the game if they have found more SETs than the computer
        if player_sets_found > computer_sets_found:
            lost_won = "WON"
        elif player_sets_found < computer_sets_found:
            lost_won = "LOST"
        elif player_sets_found == computer_sets_found:
            lost_won = "TIED"
        # update the labels and stop the countdown timer
        lost_or_won_label.update(f"You have {lost_won}!", transparent=True)
        pg.time.set_timer(timer_event, 0)
        pg.display.update()
        # boolean condition that prevents Pygame from handling more input
        # this makes sure that the game cannot be played anymore after it has finished
        global finished
        finished = True

# -------------------
# DEFINING VARIABLES
# -------------------

# card characteristics
# every Set card consists of a colour, shape, filling and the number of shapes on one card
colours = ['green', 'purple', 'red']
shape = ['oval', 'rectangle', 'squiggle']
filling = ['filled', 'empty', 'dots']
number = ['1', '2', '3']  

# text colours
white = (255, 255, 255)
offwhite = (255,250,240)
black = (0, 0, 0)
red = (255, 0, 0)
green = (162,205,90)
yellow = (255,215,0)

# defining the deck that will be used during the game
deck = Deck.shuffle()
cards = deck.copy()

# defining window features
window_width = 900
window_height = 660
margins = [(50,10), (200,10), (350,10), (500,10), (50,225), (200,225), (350,225), (500,225), (50,450), (200,450), (350,450), (500,450)]

# choose the difficulty of the game by altering the countdown duration
# time is in seconds
difficulties = {'easy':120, 'medium':60, 'hard':30}
timermax = difficulties['medium']
time = timermax

# some more variables that get modified during the game
used_cards = []
player_sets_found = 0
computer_sets_found = 0
choice = ""
 
# ------------------------------
# SETTING UP THE PYGAME DISPLAY
# ------------------------------

# setting up the screen and the clock
pg.init()
screen = pg.display.set_mode((window_width, window_height))
screen.fill(black)
pg.display.set_caption("SET card game") 
clock = pg.time.Clock()
timer_event = pg.USEREVENT+1
pg.time.set_timer(timer_event, 1000)

# make all the labels that will be visible in the game
player_sets_label = Label("Sets found: 0", (720,100), black, offwhite, "berlinsansfb", 20, (200,50))
computer_sets_label = Label("Computer Sets: 0", (740,150), black, offwhite, "berlinsansfb", 20, (220,50))
set_choice_label = Label("Your Set:", (730,250), black, white, "malgungothic", 26, (250,50), bold=True, underline=True)
wrong_choice_label = Label("INCORRECT SET", (790,300), black, red, "malgungothic", 24, (300,30))
cards_left_label = Label(f"Number of cards left: {len(cards)-12}", (800,540), black, green, "candara", 18, (300,30),bold=True, italic=True)
time_label = Label(str(time), (800,600), black, yellow, "berlinsansfb", 60, (120,110))
game_finish_label = Label("The game has finished", (800,400), black, white, "rockwellnova", 22, (360,30))
lost_or_won_label = Label("", (750,430), black, white, "rockwellnova", 25, (220,30), bold=True)

# draw the labels on the screen
player_sets_label.draw()
computer_sets_label.draw()
set_choice_label.draw()
cards_left_label.draw()
time_label.draw()

# load the first twelve cards on the screen and update the used cards
for i in range(len(margins)):
    card = pg.image.load('ProgWis/Cards/' + cards[0] + '.png')
    screen.blit(card, (margins[i][0], margins[i][1]))
    used_card = cards.pop(0)
    used_cards.append(used_card)
    
pg.display.flip()
  
# first SETs, optional print
SETS = Deck.all_sets(used_cards)
print(SETS)

# ----------
# MAIN LOOP
# ----------

# boolean variables that control the game
finished = False
input_active = True
running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()    
            
    # actions if the game is not over yet
    if not finished:
        clock.tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
             
            # timer countdown  
            elif event.type == timer_event:
                time -= 1
                time_label.update(str(time))
                # the computer wins a SET if the time reaches zero
                if time == 0:
                    computer_sets_found += 1
                    computer_sets_label.update(f"Computer Sets: {computer_sets_found}")
                    # change cards and reset the timer
                    computer = Game(countdown = True)
                    computer.change_cards()
                    time = timermax
            
            # method to choose a SET: click anywhere on the screen and type the card numbers (separated by commas) and hit 'return'
            elif event.type == pg.MOUSEBUTTONDOWN:
                input_active = True
                choice = ""
                wrong_choice_label.update("")
        
            elif event.type == pg.KEYDOWN and input_active:
                if event.key == pg.K_RETURN:
                    input_active = False                
                elif event.key == pg.K_BACKSPACE:
                    choice = choice[:-1]
                else:
                    choice += event.unicode
            
            # after having entered a SET
            if not input_active:
                SET = []
                SET.append(choice)                
                
                # condition to make sure the correct input is given
                allowed_input = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', ',']
                if all(x in allowed_input for x in SET[0]) and SET[0][-1] != ',':
                    S = [i.split(',') for i in SET][0]
                    if len(S) == 3:
                        SETchoice = [eval(y) for y in S]
                else:
                    found_set = False
                
                player = Game(SETchoice)
                # check for correct SET
                found_set = player.is_set()
                
                # if correct, reset timer and continue the game actions with the chosen SET
                if found_set:
                    time = timermax
                    player_sets_found += 1
                    player_sets_label.update(f"Sets found: {player_sets_found}")
                    player.change_cards()
                    # return to choosing a SET
                    input_active = True
                
                # choose a new SET if the input was incorrect
                if not found_set:
                    wrong_choice_label.update("INCORRECT SET")
                    input_active = True
                
            set_choice_label.update(f"Your Set: {choice}")
            
        pg.display.flip()

