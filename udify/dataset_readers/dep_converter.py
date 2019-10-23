"""
Utilities for converting dependency structures to sequences

Adopted from dep2label
https://github.com/mstrise/dep2label
TODO, this can be made more readable by adding ROOT in frnot of the list, 
making the id's match the list position (currently word 1 is in position 0 in the list)
"""


def relEncoding(heads, strategy):
    for i in range(len(heads)):
        heads[i] = str(int(heads[i]) - (i + 1))
        if heads[i][0] != '-':
            heads[i] = '+' + heads[i]
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
    print('Encoder: Dependency conversion strategy 4 is not implemented yet, sorry')
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
        if heads[wordIdx] == '@@UNKNOWN@@':
            newHeads.append('0')
            continue
        if heads[wordIdx][0] == '-':
            newHeads.append(wordIdx + 1 - int(heads[wordIdx][1:]))
        else:
            newHeads.append(wordIdx + 1 + int(heads[wordIdx]))
    return newHeads

def relPosDecoding(heads, poss, strategy):
    #TODO find root to connect impossible cases?
    print(heads)
    print(poss)
    print()
    newHeads = []
    for wordIdx in range(len(heads)):
        direction = heads[wordIdx][0]
        distance = int(heads[wordIdx][1:].split(',')[0])
        relPos = heads[wordIdx][1:].split(',')[1]
        foundPos = 0
        found = False
        if relPos == 'ROOT':
            newHeads.append('0')
        elif direction == '-':
            if wordIdx == 0: #if word=first word, link to next word
                heads.append(str(wordIdx + 2))
            cands = list(range(0,wordIdx))
            cands.reverse()
            for headIdx in cands:
                if poss[headIdx] == relPos:
                    foundPos += 1
                    if foundPos == distance:
                        newHeads.append(str(headIdx+1))
                        found = True
                        break
            if not found:#if the link does not exist, link to prev word
                newHeads.append(str(headIdx))

        elif direction == '+':
            if wordIdx == len(heads)-1:#if word=last word, link to prev word
                newHeads.append(str(wordIdx))
            for headIdx in range(wordIdx+1,len(heads)):
                if poss[headIdx] == relPos:
                    foundPos += 1
                    if foundPos == distance:
                        newHeads.append(str(headIdx+1))
                        found = True
                        break
            if not found:#if the link does not exist, link to next word
                newHeads.append(str(headIdx+2))
        else:
            print("Error, invalid head: " + heads[wordIdx])
            newHeads.append('1')
    return newHeads

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

