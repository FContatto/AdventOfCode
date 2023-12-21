# part 1
def build_dict(words):
    map_dict = dict()
    for w in words[1:]:
        map_dict[w[:3]] = (w[7:10],w[12:15])
    return map_dict

def calc_number(words):
    lr_str = words[0]
    map_dict = build_dict(words)
    position = 'AAA'
    n = 0
    i_lr = 0
    while position!='ZZZ':
        n += 1
        idx = 0 if lr_str[i_lr]=='L' else 1
        position = map_dict[position][idx]
        i_lr = (i_lr+1)%len(lr_str)
    return n
   
print(calc_number(words))

#part 2

 def calc_number(words):
         lr_str = words[0]
         map_dict, start_nodes = build_dict_and_start(words)
         n = 0
         i_lr = 0
         print(14257/len(lr_str))
         #periods = [0 for _ in start_nodes]
         #start_nodes_original = [i for i in start_nodes]
         while any(s[-1] != 'Z' for s in start_nodes):
             n += 1
             idx = 0 if lr_str[i_lr] == 'L' else 1
 
             start_nodes = [map_dict[position][idx] for position in start_nodes]
             if (start_nodes[5][-1]=='Z'
                 #and (n % 543649 == 0) #0
                 #and (n % 11567 ==0) #4
                 # and (n % 42948271 ==0) #1
 #14257 #2
                 #16409 #3
                 #19099 #5
             ):
                 print(start_nodes)
                 print(n)
                 #print(n % 11567)
             # if n % 100_000_000 == 0:
             #     print(start_nodes)
             #     print(n)
             i_lr = (i_lr + 1) % len(lr_str)
             # if i_lr == 0:
             #    periods = [n if (start_nodes[i])]
         return n
 
 
     print(calc_number(words))