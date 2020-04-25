
# client

# Send a flip request
# Send a reigster player request  
# Send a check word request
# End game

# Server
# DONE intialize board
# check words
# End game, check score

import random
from collections import Counter
from utilities import get_tile_distribution
from utilities import get_game_rules
from utilities import load_scrabble_dictionary
from utilities import word_is_subset
from utilities import distribution_is_subset
from utilities import subtract_distributions



class Board(object):
  
  def __init__(self, num_tiles, tile_distribution):
    this.tiles_in_play = get_empty_tile_distribution()
    this.tiles_remaining = get_tile_distribution()
    
    random.seed()
    
    
  def __flip(self):
    if (get_number_tiles_remaining = 0):
      # end game here?
      return

    letters_available =  list(this.tiles_remaining.keys())
    letters_count = len(letters_available)
    random.shuffle(letters_available)
    random_index = random.randrange(0, letters_count)
    random_letter = letters_available[random_index]
    random_letter_remaining_count = get_number_of_letter_in_play(random_letter)

    while random_letter_remaining_count == 0:
      random_index += 1
      random_index %= letters_count
      random_letter = letters_available[random_index]
      random_letter_remaining_count = get_number_of_letter_in_play(random_letter)

    flip_letter(random_letter)
  
  
  def flip_letter(self, letter):
    this.tiles_remaining[letter] -= 1
    this.tiles_in_play[letter] += 1

    
  def claim_letter(self, letter):
    this.tiles_in_play[letter] -= 1

    
  def get_number_tiles_remaining():
    counter = 0
    for tile in this.tiles_remaining.keys():
      counter += this.tiles_remaining[tile]
    
    
  def get_number_tiles_in_play():
    counter = 0
    for tile in this.tiles_in_play.keys():
      counter += this.tiles_in_play[tile]
    
    
  def get_number_of_letter_in_play(letter):    
    return this.tiles_in_play[letter]
    
  
  
class Game(object):
  
  # tile_distribution: {letter: count ...}
  
  def __init__(self, dictionary, tile_distribution, game_rules):
    
    this.dictionary = dictionary
    this.board = Board(tile_distribution)
    this.players = []
    this.rules = game_rules
    
  
  def add_player(self, name):
    p = Player(name)
    this.players.append(p)
  
  
  def check_word(self, new_word):
    
    if not new_word in this.dictionary:
      print('Invalid word!')
      return False
    
    # check individual players
    # for player in players:
    #   for claimed_word in player.words:
    #     player_word_dist = Counter(claimed_word)
    #     available_dist = merge_distributions(player_word_dist, this.board.tiles_in_play)
    #     if word_is_subset(new_word, available_dist):
    #       return True # successful word steal
    #     else:
    #       pass
    
    new_word_dist = Counter(new_word)
    
    for player in players:
      for player_word in player.words:
        # make new_word_dist
        # convert player word to player_word_dist
        # subtract player_word_dist from new_word_dist
        # see if new_word_dist is subset of tiles_in_play_dist
        
        if word_is_subset(player_word, new_word):
          player_word_dist = Counter(player_word)
          remaining_dist = subtract_distributions(player_word_dist, new_word_dist)
          
          if distribution_is_subset(remaining_dist, this.board.tiles_in_play):
            return True
    
    return word_is_subset(new_word, this.board.tiles_in_play)
  
  
     # 1. take a player word, merge it with the board, see if new_word is in that bigger distribution
     # 2. Take a player word, see if its a part of the new word, if it is, see if the remaining letters are in the main board state
        
    # check letters in the center of the board
    """
    alphabet = this.board.tiles_in_play.keys()
    for letter in alphabet:
      number_available = get_number_in_play(letter)
      number_needed = new_word.count(letter) 
      if (number_needed > number_available):
        return False
    """                 
            
class Player(object):
  
  def __init__(self, name):
    this.name = name
    this.words = []
  
  def add_word(self, word):
    this.words.append(word)