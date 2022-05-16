import numpy as np
from solver.support import *

class ChainAndCircle:
    def __init__(self, size, value, solver):
        self.size = size
        self.cellValue = value
        self.canDraw = np.full((self.size, self.size), False, dtype=bool)
        self.solver = solver
        self.numberVars = 0
        self.index = np.full((self.size, self.size), 0, dtype=int)

    def setVar(self):
        for i in range(self.size):
            for j in range(self.size):
                self.numberVars +=1
                self.index[i][j] = self.numberVars

    # CNF Rule 1
    def cnfRule1(self):
        for i in range(self.size):
            for j in range(self.size-1):
                for k in range(j + 1, self.size):
                    if self.cellValue[i][j] == self.cellValue[i][k]:
                        # Tren 1 hang chi co 1 gia tri xuat hien
                        self.solver.addClauses([-1 * self.index[i][j], -1*self.index[i][k]])
                        self.canDraw[i][j] = True
                        self.canDraw[i][k] = True

                    if self.cellValue[j][i] == self.cellValue[k][i]:
                        # Tren 1 cot chi co 1 gia tri xuat hien
                        self.solver.addClauses([-1 * self.index[j][i], -1*self.index[k][i]])
                        self.canDraw[j][i] = True
                        self.canDraw[k][i] = True

        # Dat cac menh de cho cac o chac chan giu lai
        for i in range(self.size):
            for j in range(self.size):
                if (not self.canDraw[i][j]):
                    self.solver.addClauses([self.index[i][j]])

    # CNF Rule 2
    def cnfRule2(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.canDraw[i][j]:
                    if ((i+1 < self.size) and self.canDraw[i+1][j]):
                        self.solver.addClauses([self.index[i][j], self.index[i+1][j]])

                    if ((j+1 < self.size) and self.canDraw[i][j+1]):
                        self.solver.addClauses([self.index[i][j], self.index[i][j+1]])


    def checkCirle(self, path, size):
        if len(path) < 4:
            return False
        xTail = (path[0]-1) % size
        yTail = (path[0]-1)//size
        xHead = (path[len(path) - 1]-1) % size
        yHead = (path[len(path) - 1]-1) // size
    
        if abs(xTail-xHead)==1 and abs(yTail-yHead)==1:
            return True;
        return False



    def checkChain(self, path, size):
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






     
    def findPathsUtil(self, size, i, j, path):

        if(not self.canDraw[i][j]):
            return path
    #kiem tra xem đường đã đi qua chưa
        if get_index(path,self.index[i][j]) < 0:
            path.append(self.index[i][j])

    #Tim kiem lat luot qua cac cell den het
        for a in [-1, 1]:
            for b in [-1, 1]:
                if (i + a) < size and (i + a) >= 0 and (j + b) >= 0 and (j + b) < size and (get_index(path,self.index[i + a][j + b]) < 0) and self.canDraw[i][j] :
                    self.findPathsUtil(self.size, i+a, j+b, path)
    #Kiem tra duong di co tao thanh vong tron hay Chain khong
        if self.checkCirle(path, size) or self.checkChain(path,size): 
            ints = np.full(len(path), 0, dtype=int)
            for i in range(len(path)):
                ints[i]=path[i]
            self.solver.addClauses(ints)
    
        path.pop()
        return

    # Rule 3
    def cnfRule3(self):
        path = []
        # bat dau tim cycle
        for i in range(self.size):
            for j in range(self.size):
                self.findPathsUtil(self.size, i, j, path)

        # # tim chain voi nhung o bat dau o bien cua bang
        # for i in range(self.size):
        #     chain = self.find_chain_tmp(i, 0, cycle)
        #     chain = self.find_chain_tmp(i, self.size-1, chain)

        # for j in range(1, self.size - 1):
        #     chain = self.find_chain_tmp(0, j, chain)
        #     chain = self.find_chain_tmp(self.size-1, j, chain)

    def get_result(self):
        return self.canDraw
    
    def get_number_of_variables(self):
        return self.numberVars