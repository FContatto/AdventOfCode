def parse_words(words):
    range_dict = dict()
    seeds_row = [int(s) for s in words[0].split(':')[1].split()]
    seeds = []
    for i in range(len(seeds_row)//2):
        seeds.append((seeds_row[2*i], seeds_row[2*i+1]))
    feature_dict = dict()
    for w in words[2:]:
        if w == '':
            continue
        if ':' in w:
            key,val = w.split()[0].split('-to-')
            feature_dict[val] = key
            range_dict[val] = []
            curr_list = range_dict[val]
            continue
        to_start, from_start, range_len = (int(s) for s in w.split())
        curr_list.append((to_start, from_start, range_len))
    return seeds, feature_dict, range_dict

def find_mapped_num(range_list, from_num):
    for from_start, to_start, range_len in range_list:
        if (from_num >= from_start) and (from_num<from_start+range_len):
            return to_start + from_num - from_start
    return from_num
   
def find_location(seed_range, feature_dict, range_dict):
    lowest_loc = 199900000000000
    for seed in range(seed_range[0], seed_range[1]):
        from_num = seed
        from_feat = 'location'
        while from_feat!='seed':
            if from_feat == 'seed':
                break
            range_list = range_dict[from_feat]
            from_feat = feature_dict[from_feat]
            from_num = find_mapped_num(range_list, from_num)
        lowest_loc = min(lowest_loc, from_num)
    return lowest_loc
   
def find_seed(seeds, loc):
    from_num = loc
    from_feat = 'location'
    while from_feat!='seed':
        range_list = range_dict[from_feat]
        from_feat = feature_dict[from_feat]
        from_num = find_mapped_num(range_list, from_num)
    for s, r in seeds:
        if (from_num>=s) and (from_num<s+r):
            return True
    return False

seeds, feature_dict, range_dict = parse_words(words)
for loc in range(60_000_000):
    if loc%1_000_000==0:
        print(loc)
    if find_seed(seeds, loc):
        print(loc)
        break