#!/usr/bin/env python
# coding: utf-8
# Author: Patrick Malatesta
# Date: Dec 2018

# importing emoji and storing them into a dictionary

import emoji
imageDict = dict()
fin = open('emoji_names.txt',"r")
lines = fin.readlines()
for i, el in enumerate(lines):
    imageDict[i+1] = emoji.emojize(el.strip())

#     print(i+1,imageDict[i+1],end=' ')


# creating the deck adding the cards on a dictionary with key=card ID and value=emojiIDs

# nIm - 1 must be prime
# Cards must have 3, 4, 6 or 8 images
# in our game we need 8 images per card
nIm = 8
n = nIm - 1
r = range(n)
rp1 = range(n+1)
c = 0

#initializing the dictionary that will contain the deck
deck = dict()

# First card
c += 1
#creating empty set to store emojiIDs
imageIDs = set()
for i in rp1:
    #adding the emoji IDs to the set
    imageIDs.add(i+1)
#adding the card to the dictionary
deck[c]=imageIDs
print()

#we will use the same technique of creating a set to store the emojiIDs and then adding the card

# n following cards 
imageIDs = set()
for j in r:
    c = c+1
    imageIDs.add(1)
    deck[c]=imageIDs
    
    imageIDs = set()
    for k in r:
        imageIDs.add(1)
        imageIDs.add(n+2 + n*j +k)
        deck[c]=imageIDs
        
# n x n following cards
for i in r:
    imageIDs = set()
    for j in r:
        c = c+1
        imageIDs.add(i+2)
        deck[c]=imageIDs
        
        imageIDs = set()
        for k in r:
            imageIDs.add(i+2)
            imageIDs.add((n+1 +n*k + (i*k+j) % n)+1)
            deck[c]=imageIDs


# creating check_validity function


# by default the function is NOT verbose
def check_validity(deck, verbose = False):
    #we compare all the cards with each other
    for card in deck:
        for other_card in deck:
            # we don't need to compare the same cards
            if card != other_card:
                #if verbose is set as True we print each comparison executed in the loop
                if verbose:
                    print('checking card n.', card, 'with card n.', other_card )
                    # with set intersectin function we create a new set containing the result 
                    check = deck[card].intersection(deck[other_card])
                    print ('the image in common has ID ', check, 'there is ', len(check), ' image in common')
                    # if the set has lenght > 1 (if there is more that 1 image in common) we print error and exit lopp
                    if len(check) > 1:
                        print ('deck is not valid')
                        return 
                # same operation will be carried out without print statement
                else:
                    check = deck[card].intersection(deck[other_card])
                    if len(check) > 1:
                        print ('deck is not valid')
                        return 
                    
    #if the last check is equal to 1 the deck is ok
    if len(check) == 1:
        print('deck is ok')


# check if the deck is valid validity(deck, verbose = True)
# check_validity(deck)


# creating DobbleCard Class
#  __init__ method that uses card ID to get the imagesIDs
#  __repr__ method to represent the card as requested


class DobbleCard():
    #__init__ method uses card ID to get the emojis IDs
    def __init__(self, cardID):
        self.imagesIDs = deck[cardID]
    # created a __repr__ method that will display the card as requested         
    def __repr__(self):
        #create an empty tuple that will store the images
        self.images = ()
        for x in self.imagesIDs:
            # adding the images to the list 
            self.images += (imageDict[x],)
        # the return statement will give as output the desired card layout
        return ("\n".join(["".join(self.images[i:i+3]) for i in range(0,len(self.images),3)]))
            


# creating DobbleDeck Class 
# __init__ method crates a deck with the amount of cards requested calling the add_card method
# add_card generates a random key and add the corresponding card to the deck
# remove_card will remove the played card from the deck
# play_card will generate a random index based on the deck size, display the corresponding card and then remove it from the deck

#importing random module to pick random cards
import random

class DobbleDeck():
    #we set a standard of 57 cards per deck
    def __init__ (self, card_number = 57):
        #creating empty list that will contain my_deck
        self.my_deck = []
        #with the loop add as many card as requested
        for c in range(0, card_number):
            # calling the add.card method to add random cards to my_deck
            self.add_card()
       
    def add_card(self):

        #generating a random key to pick any random card from the deck dictionary in range (1,57)
        key = random.randint(1, 57)
        #adding to my_deck a card based on the random key generated
        self.my_deck += [DobbleCard(key)]
        #genereating a random key for the add_card method allows to have always a different deck of any size
    
    def remove_card(self, i):
        #with the pop function I remove the played card based on its index
        self.my_deck.pop(i)
        
    def play_card(self):
        #generating a random number within the lenght of my_deck
        r = random.randint(0, len(self.my_deck)-1)
        #the played card will be picket from my_deck based on the generated random index
        self.played_card = self.my_deck[r]
        #if the played card is not the last one in the deck I remove it
        if len(self.my_deck) > 1:
            self.remove_card(r)
        return self.played_card
        


# Creating function with the game logic

def run_dobble():
    print('==========  WELCOME TO DOBBLE  =========')
    
    #first we make sure that the user enters a number
    while True:
        try:
            #ask user how many cards to play
            card_number = int(input('How many cards (<56) '))
        except ValueError:
            #if user doesn't enter a number print error and ask for another input
            print("That's not a valid number!")
        else:
            #if user enters a number exit the loop and proceed
            break
            
    #we also want to make sure that the number entered is valid
    while card_number >= 56 or card_number <=0:
        print("Wrong amount of card selected. Please try again")
        card_number = int(input('How many cards (<56) '))
    else:
        print("if you want to record a draw type \"d\" or \"D\"")
        #create a deck with the requested amount of cards (+1) instantiating DobbleDeck Class
        deck = DobbleDeck(card_number+1)
        #initialize the counter for points
        a_counter = 0
        b_counter = 0
        #initialize the counter for game
        game_counter = 1
        
        #at this point we play the first 2 cards
        #creating cards calling play_card method and casting them into strings
        left_card = str(deck.play_card())
        right_card = str(deck.play_card())
        #to create the effect of card side-by-side we slice the cards casted into strings
        print(left_card[0:3],'         ', right_card[0:3])
        print(left_card[4:7],'         ', right_card[4:7])
        print(left_card[8:10],'           ', right_card[8:10])
        
        winner = input('Who wins? (A or B)') 
        #we check for errors when user has to input who wins the game
        while winner not in ['a','A','b','B','d','D']:
            print('sorry wrong input, try again!')
            winner = input('Who wins? (A or B)')
        else:
            #if user enters valid character we increment the counter or print that is a draw
            if winner == 'a' or winner == 'A':
                a_counter += 1
            elif winner == 'b' or winner == 'B':
                b_counter += 1
            elif winner == 'd' or winner == 'D':
                print('That\'s a draw!')
            
            #after the first 2 cards we keep playing for as many cards as initially requested
            while game_counter < card_number: 
                #the card on the left-hand side now gets the value of the previous card on the right-hand side
                left_card = right_card
                #the right-hand side card is a new card called with the play_card method
                right_card = str(deck.play_card())
                #we use the same technique to print the cards
                print(left_card[0:3],'         ', right_card[0:3])
                print(left_card[4:7],'         ', right_card[4:7])
                print(left_card[8:10],'           ', right_card[8:10])
                #we increment game counter
                game_counter +=1
                winner = input('Who wins? (A or B)')
                
                #we do again the error checking and increment the counters
                while winner not in ['a','A','b','B','d','D']:
                    print('sorry wrong input, try again!')
                    winner = input('Who wins? (A or B)')
                else:
                    if winner == 'a' or winner == 'A':
                        a_counter += 1
                    elif winner == 'b' or winner == 'B':
                        b_counter += 1
                    elif winner == 'd' or winner == 'D':
                        print('That\'s a draw!')
            print() 
            #when all the cards all played we print the final score and the winner
            print ('Score')
            print ('A:', a_counter)
            print ('B:', b_counter)
            print()
            if a_counter > b_counter:
                print ('Player A wins!')
            elif b_counter > a_counter:
                print ('Player B wins!')
            else:
                print ('That\'s a draw!')


run_dobble()




