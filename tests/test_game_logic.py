from snatch.utilities import get_tile_distribution, load_scrabble_dictionary, get_empty_tile_distribution, get_game_rules
from snatch.game import Board, Game

def test_board_init():
  b = Board(num_tiles=88, tile_distribution=get_tile_distribution())

  assert(b.get_number_tiles_in_play() == 0)
  assert(b.get_number_tiles_remaining() == 88)


def test_flip():
  tile_distribution = get_tile_distribution()
  b = Board(num_tiles=88, tile_distribution=tile_distribution)

  b.flip()

  assert(b.get_number_tiles_in_play() == 1)
  assert(b.get_number_tiles_remaining() == 87)


def test_flip_letter():
  tile_distribution = get_tile_distribution()
  b = Board(num_tiles=88, tile_distribution=tile_distribution)

  initial_Bs = b.tiles_remaining["B"]
  b.flip_letter("B")

  assert(b.get_number_tiles_in_play() == 1)
  assert(b.get_number_tiles_remaining() == 87)
  assert(b.tiles_in_play["B"] == 1)
  assert(b.tiles_remaining["B"] == initial_Bs-1)

  b.flip_letter("A")
  b.flip_letter("N")
  b.flip_letter("A")
  b.flip_letter("N")
  b.flip_letter("A")

  assert(b.tiles_in_play['B'] == 1)
  assert(b.tiles_in_play['A'] == 3)
  assert(b.tiles_in_play['Z'] == 0)
  assert(b.tiles_remaining['B'] == 1)      # assumes initial count of 2
  assert(b.tiles_remaining['A'] == 6)      # assumes initial count of 9


# Given a word, check whether it's a valid play
def test_check_word():

  valid_words = load_scrabble_dictionary()
  tile_distribution = get_tile_distribution()
  game_rules = get_game_rules()

  g = Game(valid_words, tile_distribution, game_rules)

  g.add_player('JP')
  g.add_player('RH')
  g.add_player('JB')

  g.board.tiles_in_play = {'A': 3, 'B': 1, 'N': 2}

  # test pulling letters only from board center
  assert(g.check_word('BANANA') == True)
  assert(g.check_word('BANANAS') == False)
  assert(g.check_word('BAN') == True)
  assert(g.check_word('BANK') == False)
  assert(g.check_word('BANANANA') == False)

  # test pulling letters from players
  g.board.tiles_in_play = {'A': 1, 'B': 1, 'N': 2}
  g.players[0].add_word("A")

  assert(g.check_word('BANANA') == False)

  g.players[1].add_word("A")

  assert(g.check_word('BANANA') == False)

  g.players[1].add_word("AA")

  assert(g.check_word('BANANA') == True)
