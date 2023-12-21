def get_start_position(words):
    for i,w in enumerate(words):
        for j,c in enumerate(w):
            if c=='S':
                return i, j
     
def calc_dist(words):
    s_i, s_j = get_start_position(words)
    i, j = s_i+1, s_j
    direction = 'u'
    dist = 0
    while (i!=s_i) or (j!=s_j):
        dist+=1
        if words[i][j]=='|':
            delta = 1 if direction=='u' else -1
            i+=delta
        elif words[i][j]=='-':
            delta = 1 if direction=='l' else -1
            j+=delta
        elif words[i][j]=='L':
            if direction =='u':
                direction = 'l'
                j+=1
            else:
                direction = 'd'
                i-=1
        elif words[i][j]=='J':
            if direction =='u':
                direction = 'r'
                j-=1
            else:
                direction = 'd'
                i-=1
        elif words[i][j]=='7':
            if direction =='l':
                direction = 'u'
                i+=1
            else:
                direction = 'r'
                j-=1
        elif words[i][j]=='F':
            if direction =='r':
                direction = 'u'
                i+=1
            else:
                direction = 'l'
                j+=1        
    return (dist+1)//2
def get_loop_points(words):
    s_i, s_j = get_start_position(words)
    loop_points = set({(s_i,s_j)})
    i, j = s_i+1, s_j
    direction = 'u'
    while (i!=s_i) or (j!=s_j):
        loop_points.add((i,j))
        if words[i][j]=='|':
            delta = 1 if direction=='u' else -1
            i+=delta
        elif words[i][j]=='-':
            delta = 1 if direction=='l' else -1
            j+=delta
        elif words[i][j]=='L':
            if direction =='u':
                direction = 'l'
                j+=1
            else:
                direction = 'd'
                i-=1
        elif words[i][j]=='J':
            if direction =='u':
                direction = 'r'
                j-=1
            else:
                direction = 'd'
                i-=1
        elif words[i][j]=='7':
            if direction =='l':
                direction = 'u'
                i+=1
            else:
                direction = 'r'
                j-=1
        elif words[i][j]=='F':
            if direction =='r':
                direction = 'u'
                i+=1
            else:
                direction = 'l'
                j+=1        
    return loop_points

def calculate_area(words):
    loop_points = get_loop_points(words)
    area = 0
    for i,w in enumerate(words):
        prev_pipe = None
        inside_loop = False
        for j,c in enumerate(w):
            if ((i,j) in loop_points):
                if words[i][j]!='-':
                    if ((words[i][j]=='J' and prev_pipe=='L') or
                        ((words[i][j]=='7' or words[i][j]=='S') and prev_pipe=='F') or
                        words[i][j] in ['|', 'F', 'L']):
                        inside_loop = not(inside_loop)
                    prev_pipe = words[i][j]
            else:
                area += inside_loop

    return area
   
#print(words[20])
print(calculate_area(words))