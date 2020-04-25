def get_tile_distribution():
  return {'A': 9,
          'B': 2,
          'C': 2,
          'D': 4,
          'E': 2,
          'F': 2,
          'G': 3,
          'H': 2,
          'I': 9,
          'J': 1,
          'K': 1,
          'L': 4,
          'M': 2,
          'N': 6,
          'O': 8,
          'P': 2,
          'Q': 1,
          'R': 6,
          'S': 4,
          'T': 6,
          'U': 4,
          'V': 2,
          'W': 2,
          'X': 1,
          'Y': 2,
          'Z': 1}


def get_empty_tile_distribution():
  return {'A': 0,
          'B': 0,
          'C': 0,
          'D': 0,
          'E': 0,
          'F': 0,
          'G': 0,
          'H': 0,
          'I': 0,
          'J': 0,
          'K': 0,
          'L': 0,
          'M': 0,
          'N': 0,
          'O': 0,
          'P': 0,
          'Q': 0,
          'R': 0,
          'S': 0,
          'T': 0,
          'U': 0,
          'V': 0,
          'W': 0,
          'X': 0,
          'Y': 0,
          'Z': 0}

def get_game_rules():
  return {
    'min_word_length': 4
  }
  
  
# dist1 is a subset of dist2
def subtract_distributions(dist1, dist2):
  for key in dist2.keys():
    dist2[key] -= dist1[key]
  return dist2
    
    
# word: a string
# distribution: a dictionary mapping letters to counts
def word_is_subset(word, available_dist):
  word_dist = Counter(word)
  return distribution_is_subset(word_dist, available_dist)


# is dist1 a sebset of dist2?
def distribution_is_subset(dist1, dist2):
  for k in set.keys():
    if not k in dist2:
      return False
    if dist2[k] < dist1[k]:
      return False
  return True


# merge two dictionaries, adding all shared keys
# NOTE: not currently used
def merge_distributions(dist1, dist2):
  all_keys = set(dist1.keys() + dist2.keys())
  merged = {}
  for k in list(all_keys):
    merged[k] = 0
    if k in dist1:
      merged[k] += dist1[k]
    if k in dist2:
      merged[k] += dist2[k]
  return merged  


def load_scrabble_dictionary():
  with open('scrabble_dictionary.txt') as f:
    valid_words = [line.strip() for line in f.readlines()]
    return set(valid_words)