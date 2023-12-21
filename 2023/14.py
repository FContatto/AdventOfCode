import numpy as np
 def calculate_total_load(words):
     total_load = 0
     for j in range(len(words[0])):
         current_limit = len(words)
         for i, w in enumerate(words):
             if w[j] == 'O':
                 total_load += current_limit
                 current_limit -= 1
             elif w[j] == '#':
                 current_limit = len(words) - i - 1
     return total_load
 
 
 def tilt_up(words):
     for j in range(len(words[0])):
         current_limit = 0
         for i, w in enumerate(words):
             if w[j] == 'O':
                 words[current_limit][j] = 'O'
                 if i>current_limit:
                     w[j] = '.'
                 current_limit += 1
             elif w[j] == '#':
                 current_limit = i + 1
 
 def do_cycle(words):
     tilt_up(words)
     for _ in range(3):
         words = np.rot90(words, -1) #rotate clockwise
         tilt_up(words)
 
 
 def calculate_load(words):
     total_load = 0
     for j in range(len(words[0])):
         for i, w in enumerate(words):
             if w[j] == 'O':
                 total_load += len(words) - i
     return total_load
 
 
 def platforms_equal(words1, words2):
     return all(words1[i][j] == words2[i][j] for i in range(len(words1)) for j in range(len(words1[i])))
 
 def find_period_length(words, non_periodic_config_len):
     # the number of configurations is finite, so eventually we will reach repeated configurations
     # and periodic behaviour takes place
     words_copy = words.copy()
     for i in range(non_periodic_config_len):
         do_cycle(words_copy)
 
     words_copy2 = words_copy.copy()
     do_cycle(words_copy2)
     period_len = 1
     while not platforms_equal(words_copy, words_copy2):
         period_len += 1
         if period_len > non_periodic_config_len:
             raise Exception('Could not find period')
         do_cycle(words_copy2)
     return period_len
 def calculate_total_load_after_cycles(words, nb_cycles):
     words = [list(w) for w in words]
     non_periodic_config_len = 100 # the non-periodic length is heuristic
     words = np.asarray(words)
     if nb_cycles < non_periodic_config_len: # if nb_cycles not too big, just calculate the load
         for i in range(nb_cycles):
             do_cycle(words)
         return calculate_load(words)
 
     period_len = find_period_length(words, non_periodic_config_len)
 
     for _ in range(non_periodic_config_len):
         do_cycle(words)
     nb_cycles -= non_periodic_config_len
     nb_cycles = nb_cycles % period_len
     for _ in range(nb_cycles):
         do_cycle(words)
 
     return calculate_load(words)
 
 print(calculate_total_load_after_cycles(words, 1_000_000_000))