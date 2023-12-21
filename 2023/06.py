import math
def calc_roots(comp_length, record):
    return -math.ceil((comp_length-math.sqrt(comp_length*comp_length-4*record))/2)+math.ceil((comp_length+math.sqrt(comp_length*comp_length-4*record))/2)