def calculate_nb_energised(words, initial_direction):
     seen = set()
     next_to_visit = [initial_direction]
     while len(next_to_visit)>0:
         next_dir = next_to_visit.pop()
         if next_dir in seen:
             continue
         (x,y), d = next_dir
         if (x<0) or (x>=len(words)) or (y<0) or (y>=len(words[x])):
             continue
         seen.add(next_dir)
         c = words[x][y]
         if c=='.':
             if d=='l':
                 next_to_visit.append(((x, y+1), d))
             elif d=='r':
                 next_to_visit.append(((x, y - 1), d))
             elif d=='u':
                 next_to_visit.append(((x+1, y), d))
             elif d == 'd':
                 next_to_visit.append(((x - 1, y), d))
         elif c=='/':
             if d=='l':
                 next_to_visit.append(((x-1, y), 'd'))
             elif d=='r':
                 next_to_visit.append(((x+1, y), 'u'))
             elif d=='u':
                 next_to_visit.append(((x, y-1), 'r'))
             elif d == 'd':
                 next_to_visit.append(((x, y+1), 'l'))
         elif c=='\\':
             if d=='l':
                 next_to_visit.append(((x+1, y), 'u'))
             elif d=='r':
                 next_to_visit.append(((x-1, y), 'd'))
             elif d=='u':
                 next_to_visit.append(((x, y+1), 'l'))
             elif d == 'd':
                 next_to_visit.append(((x, y-1), 'r'))
         elif c=='-':
             if d == 'l':
                 next_to_visit.append(((x, y + 1), d))
             elif d == 'r':
                 next_to_visit.append(((x, y - 1), d))
             else:
                 next_to_visit.append(((x, y-1), 'r'))
                 next_to_visit.append(((x, y + 1), 'l'))
         else:
             if d == 'u':
                 next_to_visit.append(((x+1, y), d))
             elif d == 'd':
                 next_to_visit.append(((x-1, y), d))
             else:
                 next_to_visit.append(((x-1, y), 'd'))
                 next_to_visit.append(((x+1, y), 'u'))
     return len(set((x,y) for (x,y), _ in seen))
 
 def find_max_energised(words):
     max_top = max(calculate_nb_energised(words, ((0, y), 'u')) for y in range(len(words[0])))
     max_bottom = max(calculate_nb_energised(words, ((len(words)-1, y), 'd')) for y in range(len(words[0])))
     max_left = max(calculate_nb_energised(words, ((x,0), 'l')) for x in range(len(words)))
     max_right = max(calculate_nb_energised(words, ((x, len(words[x])-1), 'r')) for x in range(len(words)))
     return max(max_top, max_bottom, max_left, max_right)
 print(find_max_energised(words))