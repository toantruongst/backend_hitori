mat = [
        [1,   2,  3,  4,  5],
        [6,   7,  8,  9, 10],
        [11, 12, 13, 14, 15],
        [16, 17, 18, 19, 20],
        [21, 22, 23, 24, 25],
    ]

possiblePath = [
        [True, False, False, True, True],
        [False, False, True, True, True],
        [True, True, False, True, True],
        [True, True, True, False, False],
        [False, False, True, True, False],
    ]

def get_index(a, v):
    if v in a:
        return a.index(v)
    else:
        return -1


path = []
def findPaths(m):

    findPathsUtil(m,2,0,path)
    
def checkCirle(path, size):
    if len(path) < 4:
        return False
    xTail = (path[0]-1) % size
    yTail = (path[0]-1)//size
    xHead = (path[len(path) - 1]-1) % size
    yHead = (path[len(path) - 1]-1) // size
    
    if abs(xTail-xHead)==1 and abs(yTail-yHead)==1:
        return True;
    return False



def checkChain(path, size):
    lengthPath = len(path)
    if lengthPath < 2:
        return False
    xTail = (path[0]-1) % size
    yTail = (path[0]-1)//size
    xHead = (path[lengthPath - 1]-1) % size
    yHead = (path[lengthPath - 1]-1) // size

    if (xTail ==0 or yTail == 0 or xTail == (size-1) or yTail== (size-1)) and (xHead ==0 or yHead == 0 or xHead == (size-1) or yHead== (size-1)):
        return True
    return False


     
def findPathsUtil(size,i,j,path):

    if(not possiblePath[i][j]):
        return path
    #kiem tra xem đường đã đi qua chưa
    if get_index(path,mat[i][j]) < 0:
        path.append(mat[i][j])

    temp = []

    #Tim kiem lat luot qua cac cell den dich
    for a in [-1, 1]:
        for b in [-1, 1]:
            if (i + a) < size and (i + a) >= 0 and (j + b) >= 0 and (j + b) < size and (get_index(path,mat[i + a][j + b]) < 0) and possiblePath[i][j] :
                findPathsUtil(size, i+a, j+b, path)
    
    if checkCirle(path, size) or checkChain(path,size): 
        print(path)
    
    path.pop()
    return
 
if __name__ == '__main__':
    # maze = [[1,2,3],
    #         [4,5,6],
    #         [7,8,9]]
    findPaths(5)
