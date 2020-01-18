#   Q: You are given a stream of 'n' elements, where 'n' can't be known before in time.
#   Can you 'randomly' store 'k' elements out of the 'n' elements in O(k) space?
#   All the 'indices' stored should be equally likely (k/n)

#   A: Let's say there exists a func(p,k) which stores 'k' random indices,
#   when parsed over a set of 'p' elements. Let's say we try to extend this.
#   The probability that p+1 should be stored by func(p+1, k) is k/(p + 1).
#   So, will choose to store p+1 th element using this. Since func(p, k) stores
#   each index with equal chance of k/p, choose any one of the elements
#   As a result, chance of any index (which is not p + 1) getting stored is
#   [(1- (k/p+1)) [not selecting p+1] +
#   (k/(p+1)) * (k-1)/k [when selecting p+1, chance of a given index not being dropped]
#   ] * (k/p) [i.e. chance that it was store by func(p, k)]
#   = [ 1 - k/(p+1) + (k-1)/(p+1))] * (k/p) = [p/p+1]*(k/p)
#   = k/ (p+1)
#   This proves the func(p, k) is extensible while retaining the property of 'uniformly' storing k/p+1 index

#   Algorithm:
#   Let S be the stream, C be the container used
#   While S is not empty:
#       p = p + 1 (length of stream so far)
#       if p <= k:
#           C.push(S.pop())
#       else:
#           if toss(bias_for_head=k/(p+1)) is head:
#               i = choose([1,k])
#               C.pop(i)
#               C.push(S.pop())
#           else:
#               S.pop()

#   We will simulate and observe over repeated experiments
#   We would 'expect' each 'index' to be stored around K/N times.

import random

experiments = 100000

N = random.choice(range(10, 50))
K = random.choice(range(1, N))


def stream_of_elements():
    """

    :return:
    """
    p = 0
    global N

    while p < N:
        yield p
        p = p + 1


count_of_index_stored = [0 for x in range(N)]

for experiment in range(experiments):

    C = [-1 for x in range(K)]

    index = 1

    for element in stream_of_elements():

        if index <= K:
            C[index - 1] = element
        else:
            if random.choice(range(index)) < K:
                C[random.choice(range(K))] = element

        index = index + 1

    for stored_element in C:
        count_of_index_stored[stored_element] += 1

print(" N: ", N, " K: ", K,
      "\n MINIMUM TIMES AN INDEX IS STORED:", min(count_of_index_stored),
      "\n MAXIMUM TIMES AN INDEX IS STORED: ", max(count_of_index_stored),
      "\n EXPECTED TIMES AN INDEX IS TO BE STORED: ", int(experiments*(K/N)))
