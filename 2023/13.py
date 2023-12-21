import numpy as np
 
 def calc_note_rows(pattern):
     candidate_rows = []
     for i in range(pattern.shape[0]-1):
         if np.sum(pattern[i]!=pattern[i+1])<=1:
             candidate_rows.append(i)
     for i_m in candidate_rows:
         is_note = True
         smudge_fixed = False
         for i in range(i_m+1):
             mirror_index = 2*i_m-i + 1
             if mirror_index<pattern.shape[0]:
                 nb_differences = np.sum(pattern[i] != pattern[mirror_index])
                 if nb_differences>1 or (nb_differences == 1 and smudge_fixed):
                     is_note = False
                     smudge_fixed = False
                     break
                 smudge_fixed = smudge_fixed or (nb_differences == 1)
         if is_note and smudge_fixed:
             return i_m+1
     return 0
 
 def calc_note(pattern):
     rows_note = 100 * calc_note_rows(pattern)
     if rows_note==0:
         rows_note = calc_note_rows(np.transpose(pattern))
     return rows_note
 
 def calculate_total_note(words):
     pattern = []
     total_note = 0
     for w in words:
         if w != '':
             pattern.append(list(w))
         else:
             total_note += calc_note(np.asarray(pattern))
             pattern = []
     total_note += calc_note(np.asarray(pattern))
     return total_note
 
 print(calculate_total_note(words))