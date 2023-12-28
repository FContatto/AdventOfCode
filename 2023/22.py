words2 ='''1,0,1~1,2,1
 0,0,2~2,0,2
 0,2,3~2,2,3
 0,0,4~0,2,4
 2,0,5~2,2,5
 0,1,6~2,1,6
 1,1,8~1,1,9'''
from collections import defaultdict
class Brick:
    def __init__(self, brick_nb, brick_str):
        self.nb = brick_nb
        end_str_1, end_str_2 = brick_str.split('~')
        end_1 = tuple(int(i) for i in end_str_1.split(','))
        end_2 = tuple(int(i) for i in end_str_2.split(','))
        if end_1[2]<end_2[2]:
            self.end1 = end_1
            self.end2 = end_2
            self.direction='z'
        elif end_2[2]<end_1[2]:
            self.end1 = end_2
            self.end2 = end_1
            self.direction = 'z'
        elif end_1[1]<end_2[1]:
            self.end1 = end_1
            self.end2 = end_2
            self.direction = 'y'
        elif end_2[1]<end_1[1]:
            self.end1 = end_2
            self.end2 = end_1
            self.direction = 'y'
        else:
            self.end1, self.end2 = sorted([end_1, end_2])
            self.direction = 'x'
def height(self):
    assert self.end2[2]-self.end1[2]+1>0
    return self.end2[2]-self.end1[2]+1

def length(self):
    return sum(self.end2[i]-self.end1[i] for i in range(3))

def get_coords(self, i):
    return tuple(sorted([self.end1[i], self.end2[i]]))

def coord_overlap(self, other, i):
    other_min, other_max = other.get_coords(i)
    c_min, c_max = self.get_coords(i)
    return not(c_min>other_max or c_max<other_min)
    
def overlaps(self, other):
    return self.coord_overlap(other, 0) and self.coord_overlap(other, 1)

def get_all_coords(self):
    return [(i,j,k) for i in range(self.end1[0], self.end2[0]+1)
        for j in range(self.end1[1], self.end2[1]+1)
        for k in range(self.end1[2], self.end2[2]+1)]

def fall(self, z):
    height = self.height()
    self.end1 = (self.end1[0], self.end1[1], z)
    self.end2 = (self.end2[0], self.end2[1], z+height-1)

def __lt__(self, other):
    return self.end1[2]<other.end1[2]

def parse_words(words):
    bricks_ls = sorted([Brick(i, w) for i, w in enumerate(words.split('\n'))])
    return bricks_ls

def fall_the_bricks(bricks_ls):
    covered_heights = dict()
    for b in bricks_ls:
        current_height_to_fall = 1
        for x, y, z in b.get_all_coords():
            current_height_to_fall = max(current_height_to_fall, covered_heights.get((x, y), 0) + 1)
            b.fall(current_height_to_fall)
        for x, y, _ in b.get_all_coords():
            covered_heights[(x, y)] = b.end2[2]
    bricks_sorted = sorted([(b.end2[2], b) for b in bricks_ls], reverse=True)
    bricks_sorted = [b for _, b in bricks_sorted]
    return bricks_sorted
    
def calculate_nb_disintegrate(words):
    bricks_ls = parse_words(words)
    bricks_felled = fall_the_bricks(bricks_ls)
    top_z_dict = defaultdict(list)
    brick_can_be_removed = [True for _ in range(len(bricks_felled))]
    for b in bricks_felled:
        top_z_dict[b.end2[2]].append(b)
    for b in bricks_felled:
        supporting_bricks = [b2 for b2 in top_z_dict[b.end1[2]-1] if b.overlaps(b2)]
        if len(supporting_bricks)==1:
            brick_can_be_removed[supporting_bricks[0].nb] = False
    return sum(brick_can_be_removed)

def calculate_total_falls(words):
    bricks_ls = parse_words(words)
    bricks_felled = fall_the_bricks(bricks_ls)
    top_z_dict = defaultdict(list)
    bricks_that_would_fall = [set() for _ in range(len(bricks_felled))]
    for b in bricks_felled:
        top_z_dict[b.end2[2]].append(b)
    bottom_z_dict = defaultdict(list)
    for b in bricks_felled:
        bottom_z_dict[b.end1[2]].append(b)

    supported_by_dict = dict()
    supports_dict = dict()
    for b in bricks_felled:
        supporting_bricks = [b2.nb for b2 in top_z_dict[b.end1[2]-1] if b.overlaps(b2)]
        supported_by_dict[b.nb] = set(supporting_bricks)
        if len(supporting_bricks)==1:
            bricks_that_would_fall[supporting_bricks[0]].add(b.nb)
        supported_by_bricks = [b2.nb for b2 in bottom_z_dict[b.end2[2]+1] if b.overlaps(b2)]
        supports_dict[b.nb] = set(supported_by_bricks)

    for b in bricks_felled:
    new_fallen_bricks = bricks_that_would_fall[b.nb]
    while len(new_fallen_bricks)>0:
        new_fallen_bricks = bricks_that_would_fall[b.nb]
        all_supported_bricks = set()
        for n in new_fallen_bricks:
            all_supported_bricks = all_supported_bricks.union(supports_dict[n])
        all_supported_bricks = all_supported_bricks-new_fallen_bricks
        new_fallen_bricks = set()
        for s_b in all_supported_bricks:
            if supported_by_dict[s_b].issubset(bricks_that_would_fall[b.nb]):
                new_fallen_bricks.add(s_b)
        bricks_that_would_fall[b.nb] = bricks_that_would_fall[b.nb].union(new_fallen_bricks)
    return sum(len(fall_s) for fall_s in bricks_that_would_fall)

#print(calculate_nb_disintegrate(words))
print(calculate_total_falls(words))