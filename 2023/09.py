def read_sequence(word):
    return [int(n) for n in word.split()]

def predict_next(sequence):
    if all(i==0 for i in sequence):
        return 0
    next_nb = predict_next([sequence[i+1]-sequence[i] for i in range(len(sequence)-1)])
    return sequence[0]-next_nb
   
def calc_sum(words):
    return sum(predict_next(read_sequence(w)) for w in words)
 
print(calc_sum(words))