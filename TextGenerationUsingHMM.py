import numpy as np


def initialize_pos(pi):
    r = np.random.random()
    cumulative_distribution = np.cumsum(pi)
    for q, probability in enumerate(cumulative_distribution):
        if r <= probability:
            return q


def textGen(pi, A, B, tl, dictionary):
    text = []
    current_state = initialize_pos(pi)
    for _ in range(tl):
        word = np.random.choice(dictionary, p=B[current_state])
        text.append(word)
        next_state = np.random.choice(len(pi), p=A[current_state])
        current_state = next_state
    return text


def main():
    first_line = input().strip().split()
    m = int(first_line[0])  
    n = int(first_line[1])  
    tl = int(first_line[2]) 
    
    pi = list(map(float, input().strip().split()))
    
    A = []
    for _ in range(m):
        row = list(map(float, input().strip().split()))
        A.append(row)
    
    B = []
    for _ in range(m):
        row = list(map(float, input().strip().split()))
        B.append(row)
    return m, n, tl, pi, A, B

if __name__ == "__main__":
    m, n, tl, pi, A, B = main()
    
    dictionary = []    
    for i in range(0,n) :
        dictionary.append(i)
    np.random.seed(0)
    text = textGen(pi, A, B, tl, dictionary)
    for i in range(len(text)) :
        print(text[i], end = " ")

