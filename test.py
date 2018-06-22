import math


def get_bit(int, b):
    return (int >> b) & 1
    
def set_bit(int, b):
    return (int | (1 << b))
    
def clr_bit(int, b):
    return (int & ~(1 << b))
    
def create_bit_map(K, B):
    map = [[] for i in range(K)]
    
    bit = B
    while get_bit(K, bit) == 0:
        bit -= 1
    
    num_sections = int(math.pow(2, bit))
    length = int(math.pow(2, B - bit))
    
    num_divided_sections = clr_bit(K, bit)
    
    color = 0
    number = 0
    for sec in range(num_sections):
        if num_divided_sections > 0:
            for i in range(2):
                for j in range(length/2):
                    map[color].append(number)
                    number += 1
                color += 1
            num_divided_sections -= 1
        else:
            for j in range(length):
                map[color].append(number)
                number += 1
            color += 1
    return map
    

    
for a in range(1,9):
    print create_bit_map(a, 3)

