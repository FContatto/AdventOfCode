words2 = 'rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7'
 
 def calc_hash(word):
     curr_value = 0
     for c in word:
         curr_value += ord(c)
         curr_value = (curr_value * 17) % 256
     return curr_value
 
 
 def calc_hash_sum(words):
     return sum(calc_hash(w) for w in words.split(','))
 
 class Node:
     def __init__(self, focal_len):
         self.next = None
         self.prev = None
         self.focal_len = focal_len
 
 class Box:
     def __init__(self):
         self.lens_head = None
         self.lens_hash = dict()
 
     def insert(self, lens, focal_len):
         if lens not in self.lens_hash:
             len_node = Node(focal_len)
             if self.lens_head is None:
                 self.lens_head = len_node
             else:
                 self.lens_head.next = len_node
                 len_node.prev = self.lens_head
                 self.lens_head = len_node
             self.lens_hash[lens] = len_node
             return
         self.lens_hash[lens].focal_len = focal_len
 
     def remove(self, lens):
         if lens not in self.lens_hash:
             return
         lens_node = self.lens_hash[lens]
         next = lens_node.next
         prev = lens_node.prev
         if next is not None:
             next.prev = prev
         if prev is not None:
             prev.next = next
         if lens_node.next is None:
             self.lens_head = prev
         del self.lens_hash[lens]
 
 
 
     def focus_power(self):
         node = self.lens_head
         slot_pos = len(self.lens_hash)
         power = 0
         while node is not None:
             power += slot_pos * node.focal_len
             slot_pos -= 1
             node = node.prev
         return power
 
 
 def fill_boxes(words):
     boxes = [Box() for _ in range(256)]
     for w in words.split(','):
         if w[-1]=='-':
             lens = w[:-1]
             hash_val = calc_hash(lens)
             boxes[hash_val].remove(lens)
         else:
             lens, focal_len = w.split('=')
             focal_len=int(focal_len)
             hash_val = calc_hash(lens)
             boxes[hash_val].insert(lens, focal_len)
     return boxes
 def calc_total_focussing_power(words):
     boxes = fill_boxes(words)
     total_power = 0
     for i, b in enumerate(boxes):
         total_power += (i+1)*b.focus_power()
     return total_power
 
 print(calc_total_focussing_power(words2))