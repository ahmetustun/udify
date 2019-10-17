

def getNumRoots(heads):
    counter = 0
    for headIdx in heads:
        if headIdx == '0':
            counter += 1
    return counter

def findRoot(heads):
    heads[0] = '0'
    return heads

def findBestRoot(heads):
    rootIdx = -1
    for nodeIdx in range(len(heads)):
        if heads[nodeIdx] == '0':
            if rootIdx == -1:
                rootIdx = nodeIdx 
            else:
                heads[nodeIdx] = str(rootIdx + 1)
    return heads

def getRoot(heads):
    for nodeIdx in range(len(heads)):
        if heads[nodeIdx] == '0':
            return nodeIdx
    return -1

def fixOutOfIndex(heads):
    rootIdx = getRoot(heads) + 1
    for nodeIdx in range(len(heads)):
        if int(heads[nodeIdx]) < 0:
            heads[nodeIdx] = str(rootIdx)
        elif int(heads[nodeIdx]) > len(heads):
            heads[nodeIdx] = str(rootIdx)
    return heads

def traverse(heads, idx, found):
    #print('TRAVERSE', idx, found)
    found.add(idx)
    for childIdx in range(len(heads)):
        if int(heads[childIdx]) != idx + 1:
            continue
        #print('from ', idx, ' searching for ', childIdx)
        if childIdx not in found:
            found = traverse(heads, childIdx, found)
        else:
            print('found twice: ', idx)
    return found

def fixCircle(heads):
    return heads

def fixHomeless(heads):
    visited = traverse(heads, getRoot(heads), set())
    if len(visited) == len(heads):
        return heads
    for homelessIdx in range(len(heads)):
        if homelessIdx not in visited:
            #leftmost of homeless subtree will be child of root
            heads[homelessIdx] = str(getRoot(heads) + 1)
            break
    fixHomeless(heads)
    return heads

#TODO take root probabilities into account?
def fix_tree(heads, verbose=False):
    if verbose:
        print(heads)
    numRoots = getNumRoots(heads)
    # cant the following 2 be merged?
    if numRoots == 0:
        heads = findRoot(heads)
    elif numRoots > 1:
        heads = findBestRoot(heads)
    if verbose:
        print('NumRoots: ', numRoots, ". Fixed:")
        print(heads)
    heads = fixOutOfIndex(heads)
    if verbose:
        print('fix outOfIndex: \n' + str(heads))
    #heads = fixCircle(heads)
    #if verbose:
    #    print('fix circle: \n' + str(heads))
    heads = fixHomeless(heads)
    if verbose:
        print('fix homeless: \n' + str(heads))
        print()
    return heads


if __name__ == '__main__':
    # correct 
    heads = ['4','1','1','0','4','4']
    fix_tree(heads, verbose=True)

    # no root
    heads = ['4','1','1','1','6','4']
    fix_tree(heads, verbose=True)
    
    # out of index + no root
    heads = ['-1','1','1','1','6','8']
    fix_tree(heads, verbose=True)
    
    #multiple roots
    heads = ['0','1','1','0','6','0']
    fix_tree(heads, verbose=True)

    #circular + homeless
    heads = ['4','1','1','0','6','5']
    fix_tree(heads, verbose=True)

    #1 word sent
    heads = ['0']
    fix_tree(heads, verbose=True)

    

