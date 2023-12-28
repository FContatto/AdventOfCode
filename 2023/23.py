words2 = '''#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#'''
def get_next_positions(hiking_map, pos):
    x, y = pos
    if hiking_map[x][y] == '^':
        return [(x - 1, y)]
    if hiking_map[x][y] == 'v':
        return [(x+1, y)]
    if hiking_map[x][y] == '<':
        return [(x, y-1)]
    if hiking_map[x][y] == '>':
        return [(x, y+1)]
    next_pos = []
    for i in [-1, 1]:
        x_n = x + i
        not_allowed = ['#', '^' if i == 1 else 'v']
        if x_n > 0 and (hiking_map[x_n][y] not in not_allowed):
            next_pos.append((x_n, y))
        y_n = y + i
        not_allowed = ['#', '<' if i == 1 else '>']
        if hiking_map[x][y_n] not in not_allowed:
            next_pos.append((x, y_n))

    return next_pos

def get_next_positions2(hiking_map, pos):
    x, y = pos
    next_pos = []
    for i in [-1, 1]:
        x_n = x + i
        if x_n > 0 and (hiking_map[x_n][y] != '#'):
            next_pos.append((x_n, y))
        y_n = y + i
        if hiking_map[x][y_n] != '#':
            next_pos.append((x, y_n))

    return next_pos

def calculate_corridors_dfs(hiking_map, start_pos):
    seen_dict = dict()
    seen = set()
    next_pos_ls = [start_pos]

    while len(next_pos_ls)>0:
        pos = next_pos_ls.pop()
        if pos in seen:
            continue
        seen.add(pos)
        next_pos_extend = get_next_positions(hiking_map, pos)
        count = 0
        while len(next_pos_extend) == 1:
            pass#pos =
        next_pos_ls.extend(next_pos_extend)


# TODO: for part 2, we need to create a graph whose nodes are all the (bi/tri)-furcation positions
# and the edges are the number of steps between each of these positions. The input set has 13 such nodes
# and the graph becomes much more tractable to apply depth-first search to. The current implementation,
# where we use a nested while loop to run down 1-way corridors takes way too long.

big_max = [0]
counter = [0]
def calculate_longest_path_dfs(hiking_map, start_pos, seen=None):
    if seen is None:
        seen = set()
    final_destination = (len(hiking_map) - 1, len(hiking_map[-1]) - 2)
    if start_pos == final_destination:
        counter[0]+=1
        if counter[0] % 10000==0:
            print(f'counter: {counter[0]}')
        return len(seen)
    seen.add(start_pos)
    max_dist = 0
    next_positions = [p for p in get_next_positions2(hiking_map, start_pos) if p not in seen]

    offset_seen = {start_pos}
    while (len(next_positions)==1):
        pos_offset = next_positions.pop()
        if pos_offset == final_destination:
            max_dist = len(seen)
            seen.difference_update(offset_seen)
            counter[0] += 1
            if counter[0] % 10000 == 0:
                print(f'counter: {counter[0]}, max: {big_max[0]}')
            return max_dist
        offset_seen.add(pos_offset)
        seen.add(pos_offset)
        next_positions = [p for p in get_next_positions2(hiking_map, pos_offset) if p not in seen]
    for next_pos in next_positions:
        if next_pos in seen:
            continue
        new_dist = calculate_longest_path_dfs(hiking_map, next_pos, seen)
        max_dist = max(max_dist, new_dist)
    if max_dist > big_max[0]:
        print(max_dist)
        big_max[0] = max_dist
    seen.difference_update(offset_seen)
    return max_dist

def calculate_length_longest_path(words):
    hiking_map = words.split('\n')
    print(len(hiking_map), len(hiking_map[0]))
    return calculate_longest_path_dfs(hiking_map, (0,1))

print(calculate_length_longest_path(words))