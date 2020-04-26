
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

  def claim_letter_distribution(self, dist):
    for letter, count in dist.items():
      for i in range(count):
        self.board.claim_letter(letter)

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

  # to run whenever a player presses enter
  def player_calls_word(self, taking_player, new_word):
    result = check_word(new_word)

    if result['success']:

      if result['player'] is None:
        self.build_word_from_in_play(word, player)

      else:   # check word found a player to steal from
        self.snatch_word(old_word=result['old_word'],
                        new_word=new_word,
                        taking_player=taking_player,
                        robbed_player=result['player'])

  def snatch_word(old_word, new_word, taking_player, robbed_player):
    new_letters = subtract_distributions(Counter(old_word), Counter(new_word))
    self.board.claim_letter_distribution(new_letters)
    robbed_player.remove(old_word)
    taking_player.append(new_word)

  def build_word_from_in_play(word, player):
    self.board.claim_letter_distribution(Counter(word))
    player.append(new_word)

  def add_player(self, name):
    self.players.append(Player(name))

  # Returns dictionary with values:
  #     success:      True only if the word is valid and formable
  #     player:       the Player to steal from, if a steal is possible (otherwise None)
  #     old_word:     the word to steal, if a steal is possible (otherwise None)
  def check_word(self, new_word):

    # Check that it is long enough
    if len(new_word) < self.min_word_length:
      print('Words must be at least {} letters long!'.format(self.min_word_length))
      return {'success': False, 'player': None, 'old_word': None}

    # Check that it is a valid dictionary word
    if not new_word in self.dictionary:
      print('Invalid word!')
      return {'success': False, 'player': None, 'old_word': None}
    
    new_word_dist = Counter(new_word)

    for player in self.players:      
      for old_word in player.words:

        # For a steal to be possible:
        # - the new word must be longer
        # - the old word must be a subset of the new word
        if len(new_word) > len(old_word) and word_is_subset(old_word, Counter(new_word)):
          old_word_dist = Counter(old_word)
          remaining_dist = subtract_distributions(old_word_dist, new_word_dist)

          # - the remaining letters of the new word that aren't in the old word
          # must be in the main board state
          if distribution_is_subset(remaining_dist, self.board.tiles_in_play):
            return {'success': True, 'player': player, 'old_word': old_word}

    # Word couldn't be formed with any player words.
    # Check if it can be formed only from center
    if word_is_subset(new_word, self.board.tiles_in_play):
      return {'success': True, 'player': None, 'old_word': None}
    else:
      return {'success': False, 'player': None, 'old_word': None}


class Player(object):

  def __init__(self, name):
    self.name = name
    self.words = []

  def add_word(self, word):
    self.words.append(word)
