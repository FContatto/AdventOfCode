import heapq
 
 def update_heap(words, node, heap_nodes, seen):
     loss, pos, straight_streak, direction = node
     x, y = pos
     min_streak = 4
     max_streak = 10
     if direction in ['r', 'l']:
         if (x + min_streak < len(words)) and (((x + min_streak, y), min_streak, 'd') not in seen):
             heapq.heappush(heap_nodes, (loss + sum(words[x+i][y] for i in range(1, min_streak+1)),
                                         (x + min_streak, y), min_streak, 'd'))
         if (x - min_streak >= 0) and (((x - min_streak, y), min_streak, 'u') not in seen):
             heapq.heappush(heap_nodes, (loss + sum(words[x-i][y] for i in range(1, min_streak+1)),
                                         (x - min_streak, y), min_streak, 'u'))
         if (straight_streak >= min_streak) and (straight_streak < max_streak):
             delta_y = int(direction == 'r')
             if (y + delta_y >= 0) and (y + delta_y < len(words[x])) and (((x, y + delta_y), straight_streak + 1,
                                                                           direction) not in seen):
                 heapq.heappush(heap_nodes, (loss + words[x][y + delta_y], (x, y + delta_y),
                                             straight_streak + 1, direction))
     else:
         if (y + min_streak< len(words[x])) and (((x, y+ min_streak), min_streak, 'r') not in seen):
             heapq.heappush(heap_nodes, (loss+sum(words[x][y + i] for i in range(1, min_streak+1)),
                                         (x, y + min_streak), min_streak, 'r'))
         if (y- min_streak >= 0) and (((x, y- min_streak), min_streak, 'l') not in seen):
             heapq.heappush(heap_nodes, (loss + sum(words[x][y - i] for i in range(1, min_streak+1)),
                                         (x, y- min_streak), min_streak, 'l'))
         if (straight_streak >= min_streak) and (straight_streak < max_streak):
             delta_x = int(direction == 'd')
             if (x + delta_x >= 0) and (x + delta_x < len(words)) and (((x + delta_x, y), straight_streak + 1,
                                                                           direction) not in seen):
                 heapq.heappush(heap_nodes, (loss + words[x + delta_x][y],
                                             (x + delta_x, y), straight_streak + 1,
                                                  direction))
 
 
 def dijkstra_loss_calc(words, heap_nodes, seen):
     while True:
         next_node = heapq.heappop(heap_nodes)
         heap_loss, pos, straight_streak, direction = next_node
         node = (pos, straight_streak, direction)
         while node in seen:
             next_node = heapq.heappop(heap_nodes)
             heap_loss, pos, straight_streak, direction = next_node
             node = (pos, straight_streak, direction)
         seen.add(node)
         x,y = pos
         if (x==len(words)-1) and (y==len(words[x])-1):
             return heap_loss
         update_heap(words, next_node, heap_nodes, seen)
 
 def find_min_total_loss(words):
     words = [[int(n) for n in row] for row in words]
     min_loss = None
     for direction in ['r', 'd']:
         heap_nodes = [(0, (0,0), 0, direction)]
         seen = set()
         if min_loss is None:
             min_loss = dijkstra_loss_calc(words, heap_nodes, seen)
         else:
             min_loss = min(min_loss, dijkstra_loss_calc(words, heap_nodes, seen))
     return min_loss
 print(find_min_total_loss(words))