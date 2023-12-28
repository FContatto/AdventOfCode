words2 = '''19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3'''

from decimal import Decimal #although even Decimal doesn't handle float integers with the required precision
def parse_words(words):
    hails_str_ls = words.split('\n')
    hails = []
    for h_str in hails_str_ls:
        pos_str, v_str = h_str.split(' @ ')
        x, y, z = pos_str.split(', ')
        vx, vy, vz = v_str.split(', ')
        hails.append(((int(x), int(y), int(z)), (int(vx), int(vy), int(vz))))
    return hails


def calculate_hail_y_z_coord(hail, x):
    p, v = hail
    x_p, y_p, z_p = Decimal(p[0]),Decimal(p[1]),Decimal(p[2])
    v_x, v_y, v_z = Decimal(v[0]),Decimal(v[1]),Decimal(v[2])
    return y_p - x_p * v_y / v_x + v_y / v_x * x, z_p - x_p * v_z / v_x + v_z / v_x * x


def calculate_intersection_coords_and_t(hail_1, hail_2):
    p_1, v_1 = hail_1
    p_2, v_2 = hail_2
    x1, y1, _ = p_1
    x2, y2, _ = p_2
    vx1, vy1, _ = v_1
    vx2, vy2, _ = v_2
    denominator = vy2 * vx1 - vy1 * vx2
    if denominator == 0:
        # the lines are parallel
        # we assume the trajectory lines are not the same
        return None
    if vx1 ==0 or vx2 == 0:
        return None
    x_inter = Decimal((y1 - y2) * vx2 * vx1 - x1 * vx2 * vy1 + x2 * vx1 * vy2) / Decimal(denominator)
    y_inter, z_inter = calculate_hail_y_z_coord(hail_2, x_inter)
    t = min(Decimal(x_inter - x1) / Decimal(vx1), Decimal(x_inter - x2) / Decimal(vx2))
    return x_inter, y_inter, z_inter, t

def check_intersect_in_limits(hail_1, hail_2, test_limit_1, test_limit_2):
    intersection_data = calculate_intersection_coords_and_t(hail_1, hail_2)
    if intersection_data is None:
        return False
    x, y, _, t = intersection_data
    return t > 0 and x >= test_limit_1 and x <= test_limit_2 and y >= test_limit_1 and y <= test_limit_2


def calc_intersections(words, test_limit_1, test_limit_2):
    hails = parse_words(words)
    nb_coll = 0
    for i in range(len(hails) - 1):
        for j in range(i + 1, len(hails)):
            h1 = hails[i]
            h2 = hails[j]
            nb_coll += check_intersect_in_limits(h1, h2, test_limit_1, test_limit_2)

    return nb_coll

def calculate_coords_rock(words):
    hails = parse_words(words)
    counter =0
    #the velocity should be around the same order of magnitude as that of the input data
    #interval size was determined empirically.
    #we guess various velocities for the rock, subtract from the hails' and look for the intersection point of all
    #the hails' trajectories. Using the first 3 hails as a first estimate is enough.
    for v_x in range(-200, 200):
        for v_y in range(-200, 200):
            for v_z in range(-300, 300):
                counter += 1
                if counter % 1000000 ==0:
                    print(counter, v_x)
                x_inter, y_inter, z_inter, t_inter = None, None, None, None
                for i in range(2):
                    p1, v1 = hails[i]
                    h1 = (p1, (v1[0]-v_x,v1[1]-v_y, v1[2]-v_z))
                    for j in range(i + 1, 3):
                        p2,v2 = hails[j]
                        h2 = (p2, (v2[0] - v_x, v2[1] - v_y, v2[2] - v_z))
                        inter_data = calculate_intersection_coords_and_t(h1, h2)
                        inter_data_2 = calculate_intersection_coords_and_t(h2, h1)
                        if (inter_data is None) or abs(inter_data[2] - inter_data_2[2])>0.01:
                            break
                        x_inter_new, y_inter_new, z_inter_new, t_inter_new = inter_data
                        if(x_inter_new % 1<0.001 and y_inter_new % 1<0.001
                                and z_inter_new % 1<0.001 and t_inter_new % 1<0.001
                         and t_inter_new>0):
                            if x_inter is None:
                                x_inter, y_inter, z_inter, t_inter = x_inter_new, y_inter_new, z_inter_new, t_inter_new
                                continue
                            if(abs(inter_data[0]-x_inter)<0.001
                            and abs(inter_data[1]-y_inter)<0.001
                            and abs(inter_data[2]-z_inter)<0.001):
                                #sanity check
                                for h in hails:
                                    p, v = h
                                    y_inter_check, z_inter_check = calculate_hail_y_z_coord((p, (v[0]-v_x, v[1]-v_y, v[2]-v_z)), x_inter)
                                    if abs(z_inter_check - z_inter)>0.01:
                                        break
                                return (x_inter, y_inter, z_inter, v_x, v_y,v_z, t_inter)
    return None

#print(calc_intersections(words, 200000000000000, 400000000000000))
#print(calc_intersections(words2, 7, 27))
print(calculate_coords_rock(words))