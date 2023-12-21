words2 = '''...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........'''
from collections import deque


def get_start_position(plot_map):
    for i, r in enumerate(plot_map):
        for j, c in enumerate(r):
            if c == 'S':
                return (i, j)
    return None


def get_possible_moves_2(plot_map, pos):
    x, y = pos
    possible_moves = []
    for i in [-1, 1]:
        x_n = (x + i) % len(plot_map)
        y_n = y % len(plot_map[x_n])
        if (plot_map[x_n][y_n] == '.'):
            possible_moves.append((x + i, y))
        x_n = x % len(plot_map)
        y_n = (y + i) % len(plot_map[x_n])
        if (plot_map[x_n][y_n] == '.'):
            possible_moves.append((x, y + i))
    return possible_moves


def get_possible_moves(plot_map, pos):
    x, y = pos
    possible_moves = []
    for i in [-1, 1]:
        if (x + i < len(plot_map)) and (x + i >= 0) and (plot_map[x + i][y] == '.'):
            possible_moves.append((x + i, y))
        if (y + i < len(plot_map[x])) and (y + i >= 0) and (plot_map[x][y + i] == '.'):
            possible_moves.append((x, y + i))
    return possible_moves


def calc_dists_bfs(pos, plot_map, nb_steps_max):
    seen = {pos: 0}
    next_queue = deque([pos])
    while len(next_queue) > 0:
        next_pos = next_queue.pop()
        dist = seen[next_pos]

        for p in get_possible_moves(plot_map, next_pos):
            if (dist < nb_steps_max) and (p not in seen):
                next_queue.appendleft(p)
                seen[p] = dist + 1
    return seen


def calc_nb_of_reachable_plots(words, nb_steps_max, start_position=None):
    plot_map = words
    if type(words) is str:
        plot_map = [list(r) for r in words.split('\n')]
    if start_position is None:
        start_position = get_start_position(plot_map)
        x, y = start_position
        plot_map[x][y] = '.'
    seen = calc_dists_bfs(start_position, plot_map, nb_steps_max)
    parity_step_max = nb_steps_max % 2
    return sum((d % 2 == parity_step_max) for d in seen.values())


def calc_nb_of_reachable_plots_bounded(plot_map, nb_steps_max, start_position, max_dist, max_plot_nb_per_parity):
    if nb_steps_max==0:
        return 1
    if nb_steps_max<0:
        return 0
    if nb_steps_max >= max_dist:
        return max_plot_nb_per_parity[nb_steps_max % 2]
    return calc_nb_of_reachable_plots(plot_map, nb_steps_max, start_position)


def calculate_infty_reachable_plots_from_right_corner(plot_map, bottom_right_corner_max_steps_vert, start_pos):
    dists_dict = calc_dists_bfs(start_pos, plot_map, bottom_right_corner_max_steps_vert)
    max_dist = max(dists_dict.values())
    max_plot_nb_per_parity = {
        0: sum(v % 2 == 0 for v in dists_dict.values()),
        1: sum(v % 2 == 1 for v in dists_dict.values())
    }
    cache = dict()
    for i in range(bottom_right_corner_max_steps_vert // len(plot_map) + 1):
        max_steps_for_cache = bottom_right_corner_max_steps_vert % len(plot_map) + i * len(plot_map)
        max_steps_for_cache_copy = max_steps_for_cache
        nb_plots = 0
        while max_steps_for_cache_copy >= 0:
            if max_steps_for_cache_copy in cache:
                nb_plots += cache[max_steps_for_cache_copy]
                break
            nb_plots += calc_nb_of_reachable_plots_bounded(plot_map, max_steps_for_cache_copy, start_pos,
                                                           max_dist, max_plot_nb_per_parity)
            max_steps_for_cache_copy -= len(plot_map[-1])
        cache[max_steps_for_cache] = nb_plots
    final_result = 0
    while bottom_right_corner_max_steps_vert >= 0:
        bottom_right_corner_max_steps = bottom_right_corner_max_steps_vert
        if bottom_right_corner_max_steps in cache:
            final_result += cache[bottom_right_corner_max_steps]
        else:
            print('not right, should never reach this as height and width of the map are equal')
            while bottom_right_corner_max_steps >= 0:
                if bottom_right_corner_max_steps in cache:
                    final_result += cache[bottom_right_corner_max_steps]
                    break

                nb_plots = calc_nb_of_reachable_plots_bounded(plot_map, bottom_right_corner_max_steps, start_pos,
                                                              max_dist, max_plot_nb_per_parity)

                final_result += nb_plots
                bottom_right_corner_max_steps -= len(plot_map[-1])
        bottom_right_corner_max_steps_vert -= len(plot_map)

    return final_result

def calculate_infty_reachable_plots_straight(plot_map, bottom_right_corner_max_steps_vert, start_pos):
    dists_dict = calc_dists_bfs(start_pos, plot_map, bottom_right_corner_max_steps_vert)
    max_dist = max(dists_dict.values())
    max_plot_nb_per_parity = {
        0: sum(v % 2 == 0 for v in dists_dict.values()),
        1: sum(v % 2 == 1 for v in dists_dict.values())
    }
    cache = dict()
    for i in range(bottom_right_corner_max_steps_vert // len(plot_map) + 1):
        max_steps_for_cache = bottom_right_corner_max_steps_vert % len(plot_map) + i * len(plot_map)
        max_steps_for_cache_copy = max_steps_for_cache
        nb_plots = 0
        while max_steps_for_cache_copy >= 0:
            if max_steps_for_cache_copy in cache:
                nb_plots += cache[max_steps_for_cache_copy]
                break
            nb_plots += calc_nb_of_reachable_plots_bounded(plot_map, max_steps_for_cache_copy, start_pos,
                                                           max_dist, max_plot_nb_per_parity)
            max_steps_for_cache_copy -= len(plot_map[-1])
        cache[max_steps_for_cache] = nb_plots

    final_result = 0
    bottom_right_corner_max_steps = bottom_right_corner_max_steps_vert
    if bottom_right_corner_max_steps in cache:
        return cache[bottom_right_corner_max_steps]
    else:
        print('not right, should never reach this and height and width of the map are equal')
        while bottom_right_corner_max_steps >= 0:
            if bottom_right_corner_max_steps in cache:
                final_result += cache[bottom_right_corner_max_steps]
                break

            nb_plots = calc_nb_of_reachable_plots_bounded(plot_map, bottom_right_corner_max_steps, start_pos,
                                                          max_dist, max_plot_nb_per_parity)

            final_result += nb_plots
            bottom_right_corner_max_steps -= len(plot_map[-1])

    return final_result


def calc_nb_of_reachable_plots2(words, nb_steps_max, start_position=None):
    plot_map = words
    if type(words) is str:
        plot_map = [list(r) for r in words.split('\n')]
    if start_position is None:
        start_position = get_start_position(plot_map)
        x, y = start_position
        plot_map[x][y] = '.'
    x, y = start_position
    # the algorithm only works assuming this (which my dataset satisfies):
    assert all(plot_map[i][y] == '.' for i in range(len(plot_map)))
    assert all(plot_map[x][j] == '.' for j in range(len(plot_map[x])))
    final_result = calc_nb_of_reachable_plots(plot_map, nb_steps_max, start_position)
    #### quadrants
    bottom_right_corner_max_steps_vert = nb_steps_max - (x + 1) - (y + 1)
    final_result += calculate_infty_reachable_plots_from_right_corner(plot_map, bottom_right_corner_max_steps_vert,
                                                                      (len(plot_map) - 1, len(plot_map[-1]) - 1))
    top_right_corner_max_steps_vert = nb_steps_max - (len(plot_map) - x) - (y + 1)
    final_result += calculate_infty_reachable_plots_from_right_corner(plot_map, top_right_corner_max_steps_vert,
                                                                      (0, len(plot_map[-1]) - 1))
    bottom_left_corner_max_steps_vert = nb_steps_max - (x + 1) - (len(plot_map[-1]) - y)
    final_result += calculate_infty_reachable_plots_from_right_corner(plot_map, bottom_left_corner_max_steps_vert,
                                                                      (len(plot_map) - 1, 0))
    top_left_corner_max_steps_vert = nb_steps_max - (len(plot_map) - x) - (len(plot_map[-1]) - y)
    final_result += calculate_infty_reachable_plots_from_right_corner(plot_map, top_left_corner_max_steps_vert,
                                                                      (0, 0))


    ### straight corridors
    bottom_right_corner_max_steps_vert = nb_steps_max - (x + 1)
    final_result += calculate_infty_reachable_plots_straight(plot_map, bottom_right_corner_max_steps_vert,
                                                                      (len(plot_map) - 1, y))
    top_right_corner_max_steps_vert = nb_steps_max - (len(plot_map) - x)
    final_result += calculate_infty_reachable_plots_straight(plot_map, top_right_corner_max_steps_vert,
                                                                      (0, y))
    bottom_left_corner_max_steps_vert = nb_steps_max - (len(plot_map[-1]) - y)
    final_result += calculate_infty_reachable_plots_straight(plot_map, bottom_left_corner_max_steps_vert,
                                                                      (x, 0))
    top_left_corner_max_steps_vert = nb_steps_max - (y+1)
    final_result += calculate_infty_reachable_plots_straight(plot_map, top_left_corner_max_steps_vert,
                                                                      (x, len(plot_map[-1]) - 1))


    return final_result


print(calc_nb_of_reachable_plots(words, 64) == 3658)
print(calc_nb_of_reachable_plots2(words, 26501365) == 608193767979991)