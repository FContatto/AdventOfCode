 words2 = '''R 6 (#70c710)
 D 5 (#0dc571)
 L 2 (#5713f0)
 D 2 (#d2c081)
 R 2 (#59c680)
 D 2 (#411b91)
 L 5 (#8ceee2)
 U 2 (#caa173)
 L 1 (#1b58a2)
 U 2 (#caa171)
 R 2 (#7807d2)
 U 3 (#a77fa3)
 L 2 (#015232)
 U 2 (#7a21e3)'''
 def calculate_dimensions(words):
     x, y = 0, 0
     min_x, max_x, min_y, max_y = 0, 0, 0, 0
     for w in words:
         direction, length = w.split()[:2]
         length = int(length)
         if direction == 'D':
             x+=length
             max_x = max(max_x, x)
         elif direction =='U':
             x-=length
             min_x = min(min_x, x)
         elif direction =='R':
             y+=length
             max_y = max(max_y, y)
         else:
             y-=length
             min_y = min(min_y, y)
     starting_pos = (-min_x, -min_y)
     return starting_pos, max_x-min_x+1, max_y-min_y+1
 
 
 def read_from_colour_data(words):
     new_words = []
     for w in words:
         hex_code = w.split()[-1]
         direction_code = hex_code[-2]
         direction = 'U'
         if direction_code=='0':
             direction = 'R'
         elif direction_code=='1':
             direction = 'D'
         elif direction_code=='2':
             direction = 'L'
         length = int(hex_code[2:-2], 16)
         new_words.append(f'{direction} {length}')
     return new_words
 
 def turns_clockwise(words):
     #calculated the winding number of the boundary
     directions_dict = {'R': 0, 'D': 1, 'L': 2, 'U': 3}
     return sum([2*int((directions_dict[words[(i+1) % len(words)][0]]
                       - directions_dict[words[i][0]]) in [1, -3])-1
                for i in range(len(words))]) == 4
 
 def parse_word(word):
     direction, length = word.split()[:2]
     length = int(length)
     return direction, length
 def calc_volume(words):
     words = words.split('\n')
     words = read_from_colour_data(words)
     starting_pos, x_len, y_len = calculate_dimensions(words) #y_len not used here
     x,y= starting_pos
     row_fills = [[] for _ in range(x_len)]
     volume = 0
     boundary_turns_clockwise = turns_clockwise(words)  # tells us whether the lagoon is on the right of the boundary
     for i,w in enumerate(words):
         direction, length = parse_word(w)
         if direction in ['D', 'U']:
             row_fills[x].append((y, direction))
             for _ in range(length):
                 x += 2 * int(direction == 'D') - 1
                 row_fills[x].append((y, direction))
         else:
             y += (2*int(direction=='R')-1)*length
         if i<len(words)-2:
             # pit-shaped boundaries are not accounted for in the final volume calculation
             # so we add those contributions here
             direction2, length2 = parse_word(words[i+1])
             direction3, _ = parse_word(words[i + 2])
             pit_shapes = [('D','R','U'),('U', 'L', 'D')] if boundary_turns_clockwise else [('D','L','U'),('U', 'R', 'D')]
             if (direction, direction2, direction3) in pit_shapes:
                 volume += length2-1
 
     for row in row_fills:
         prev_boundary_idx = 0
         open_boundary_prev = False
         r = sorted(row)
         for i,j in r:
             open_boundary = (j == 'U') if boundary_turns_clockwise else j == 'D'
             if open_boundary:
                 if not open_boundary_prev:
                     prev_boundary_idx = i
             else:
                 volume += i - prev_boundary_idx + 1
                 prev_boundary_idx = i + 1
             open_boundary_prev = open_boundary
     return volume
 
 
 print(calc_volume(words))