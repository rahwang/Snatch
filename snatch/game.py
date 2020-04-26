
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
from utilities import get_tile_distribution, get_empty_tile_distribution
from utilities import get_game_rules
from utilities import load_scrabble_dictionary
from utilities import word_is_subset
from utilities import distribution_is_subset
from utilities import subtract_distributions
from utilities import weighted_random_choice_from_distribution



class Board():

  def __init__(self, num_tiles, tile_distribution):
    self.tiles_in_play = get_empty_tile_distribution()
    self.tiles_remaining = get_tile_distribution()

    random.seed()

  def flip(self):
    if len(self.tiles_remaining) == 0:
      return
    chosen_letter = weighted_random_choice_from_distribution(self.tiles_remaining)
    self.flip_letter(chosen_letter)

  def flip_letter(self, letter):
    self.tiles_remaining[letter] -= 1
    self.tiles_in_play[letter] += 1

  def claim_letter(self, letter):
    self.tiles_in_play[letter] -= 1

  def get_number_tiles_remaining(self):
    counter = 0
    for tile in self.tiles_remaining.keys():
      counter += self.tiles_remaining[tile]
    return counter

  def get_number_tiles_in_play(self):
    counter = 0
    for tile in self.tiles_in_play.keys():
      counter += self.tiles_in_play[tile]
    return counter

  def get_number_of_letter_in_play(self, letter):
    return self.tiles_in_play[letter]



class Game(object):

  # tile_distribution: {letter: count ...}
  # game_rules: specifies parameters like minimum word length

  def __init__(self, dictionary, tile_distribution, game_rules):

    self.dictionary = dictionary
    self.board = Board(num_tiles=88, tile_distribution=tile_distribution)
    self.players = []
    self.min_word_length = game_rules['min_word_length']

  def add_player(self, name):
    self.players.append(Player(name))

  def check_word(self, new_word):

    # Check that it is long enough
    if len(new_word) < self.min_word_length:
      print('Words must be at least {} letters long!'.format(self.min_word_length))
      return False

    # Check that it is a valid dictionary word
    if not new_word in self.dictionary:
      print('Invalid word!')
      return False
    
    new_word_dist = Counter(new_word)

    for player in self.players:
      
      # Take a player word, see if it's a part of the new word. If it is, 
      # see if the remaining letters are in the main board state
      for player_word in player.words:
        if word_is_subset(player_word, Counter(new_word)):
          player_word_dist = Counter(player_word)
          remaining_dist = subtract_distributions(player_word_dist, new_word_dist)

          if distribution_is_subset(remaining_dist, self.board.tiles_in_play):
            return True

    # If word wasn't formable from any player words, see if it is formable
    # from only center tiles
    return word_is_subset(new_word, self.board.tiles_in_play)


class Player(object):

  def __init__(self, name):
    self.name = name
    self.words = []

  def add_word(self, word):
    self.words.append(word)
