"""
Utilities for converting dependency structures to sequences

Adopted from dep2label
https://github.com/mstrise/dep2label
"""


def relEncoding(heads, strategy):
    for i in range(len(heads)):
        heads[i] = str(int(heads[i]) - (i + 1))
    return heads

def relPosEncoding(heads, poss, strategy):
    newHeads = []
    for curIdx in range(len(heads)):
        headIdx = int(heads[curIdx]) - 1
        ownIdx = int(curIdx)
        if heads[curIdx] == '0':
            newHeads.append('-1,ROOT')
        elif headIdx < ownIdx:
            counter = 0# target is included in range
            for i in reversed(range(headIdx, ownIdx)):
                if poss[i] == poss[headIdx]:
                    counter += 1
            newHeads.append('-' + str(counter) + ',' + poss[headIdx])
        else:
            counter = 1# target is not included in range
            for i in range(ownIdx, headIdx):
                if poss[i] == poss[headIdx]:
                    counter += 1
            newHeads.append('+' + str(counter) + ',' + poss[headIdx])
    return newHeads

def bracketEncoding(heads, strategy):#pos?
    print('Dependency conversion strategy 4 is not implemented yet, sorry')
    exit(1)

#heads and poss are list of strings
def encode_dep_structure(heads, poss, strategy):
    if strategy == '1':
        return heads
    elif strategy == '2':
        return relEncoding(heads, strategy)
    elif strategy == '3':
        return relPosEncoding(heads, poss, strategy)
    elif strategy == '4':
        return bracketEncoding(heads, strategy)
    else:
        print('Dependency conversion strategy ' + strategy + ' is not known, please use a value between 1-4')

def relDecoding(heads, strategy):
    newHeads = []
    for wordIdx in range(len(heads)):
        if heads[wordIdx][0] == '-':
            newHeads.append(wordIdx + 1 - int(heads[wordIdx][1:]))
        else:
            newHeads.append(wordIdx + 1 + int(heads[wordIdx]))
    return newHeads

def relPosDecoding(heads, poss, strategy):
    print('Decoder: Dependency conversion strategy 3 is not implemented yet, sorry')
    exit(1)

def bracketingDecoding(heads, poss, strategy):
    print('Decoder: Dependency conversion strategy 4 is not implemented yet, sorry')
    exit(1)

def decode_dep_structure(heads, poss, strategy):
    if strategy == '1':
        return heads
    elif strategy == '2':
        return relDecoding(heads, strategy)
    elif strategy == '3':
        return relPosDecoding(heads, poss, strategy)
    elif strategy == '4':
        return bracketDecoding(heads, strategy)
    else:
        print('Dependency conversion strategy ' + strategy + ' is not known, please use a value between 1-4')
        exit(1)

