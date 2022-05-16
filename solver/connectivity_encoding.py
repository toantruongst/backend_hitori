import numpy as np
    
class ConnectivityEncoding:
    def __init__(self, size, value, solver):
        self.size = size
        self.cellValue = value
        self.solver = solver
        self.canDraw = np.full((self.size, self.size), False, dtype=bool)
        self.IndexOfVar = np.full((self.size, self.size, self.size, self.size), 0, dtype=int)
        self.index = np.full((self.size, self.size), 0, dtype=int) # full 0 index
        self.numberVars = 0
        self.number_of_clauses = 0

    def setVarDefault(self):
        for i in range(self.size):
            for j in range(self.size):
                self.numberVars +=1
                self.index[i][j] = self.numberVars

    def inMatrix(self, x, y):
        return x >= 0 and x < self.size and y >= 0 and y < self.size
    
    def diff(self, x, y, a, b):
        return x!=a or y!=b

    # CNF Rule 1
    def cnfRule1(self):
        for i in range(self.size):
            for j in range(self.size-1):
                for k in range(j+1, self.size):
                    if self.cellValue[i][j] == self.cellValue[i][k]:
                        self.solver.addClauses([-1 * self.index[i][j], -1*self.index[i][k]])
                        self.canDraw[i][j] = True
                        self.canDraw[i][k] = True
                    if self.cellValue[j][i] == self.cellValue[k][i]:
                        self.solver.addClauses([-1*self.index[j][i],-1*self.index[k][i]])
                        self.canDraw[j][i] = True
                        self.canDraw[k][i] = True
        
        for i in range(self.size):
            for j in range(self.size):
                if (not self.canDraw[i][j]):
                    self.solver.addClauses([self.index[i][j]])
    
    # CNF Rule 2
    def cnfRule2(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.canDraw[i][j]:         
                    if i-1 >= 0 and self.canDraw[i-1][j]:
                        self.solver.addClauses([self.index[i][j], self.index[i-1][j]])

                    if j-1 >= 0 and self.canDraw[i][j-1]:
                        self.solver.addClauses([self.index[i][j],self.index[i][j-1]])

    def setVar(self):
        for i in range(self.size):
            for j in range(self.size):
                for k in range(self.size):
                    for h in range(self.size):
                        if self.canDraw[i][j] and self.canDraw[k][h] and (self.IndexOfVar[i][j][k][h]==0):
                            self.numberVars +=1
                            self.IndexOfVar[i][j][k][h] = self.numberVars;
                        
    
    # Rule 3
    def cnfRule3(self):
        # (x,y) Bien thi di vao trong

        for i in range(self.size):
            for j in range(self.size):
                if self.canDraw[i][j]:
                    self.solver.addClauses([-self.IndexOfVar[i][j][i][j]])
                
                    if self.inMatrix(i+1, j+1) and self.canDraw[i+1][j+1]:
                        if i == 0 or i == self.size-1 or j == 0 or j == self.size-1:
                            self.solver.addClauses([self.index[i][j], self.index[i+1][j+1], self.IndexOfVar[i][j][i+1][j+1]])
                            
                        elif i+1 == 0 or i+1 == self.size-1 or j+1 == 0 or j+1 == self.size-1:
                            self.solver.addClauses([self.index[i][j], self.index[i+1][j+1], self.IndexOfVar[i+1][j+1][i][j]])
                        else:
                            self.solver.addClauses([self.index[i][j], self.index[i+1][j+1], self.IndexOfVar[i][j][i+1][j+1], self.IndexOfVar[i+1][j+1][i][j]])
                    
                    if self.inMatrix(i+1, j-1) and self.canDraw[i+1][j-1]:
                        if i == 0 or i == self.size-1 or j == 0 or j == self.size-1:
                            self.solver.addClauses([self.index[i][j], self.index[i+1][j-1], self.IndexOfVar[i][j][i+1][j-1]])

                        if i+1 == 0 or i+1 == self.size-1 or j-1 == 0 or j-1 == self.size-1:
                            self.solver.addClauses([self.index[i][j], self.index[i+1][j-1], self.IndexOfVar[i+1][j-1][i][j]])

                        if i > 0 and i < self.size-1 and j > 0 and j < self.size-1 and i+1 > 0 and i+1 < self.size-1 and j-1 > 0 and j-1 < self.size-1:
                            self.solver.addClauses([self.index[i][j], self.index[i+1][j-1], self.IndexOfVar[i][j][i+1][j-1], self.IndexOfVar[i+1][j-1][i][j]])

        for i in range(self.size):
            for j in range(self.size):
                if self.canDraw[i][j]:
                    if self.inMatrix(i+1, j+1) and self.inMatrix(i+1, j-1) and self.canDraw[i+1][j+1] and self.canDraw[i+1][j-1]:
                        self.solver.addClauses([-self.IndexOfVar[i+1][j+1][i][j], -self.IndexOfVar[i+1][j-1][i][j]])
                    if self.inMatrix(i+1, j+1) and self.inMatrix(i-1, j+1) and self.canDraw[i+1][j+1] and self.canDraw[i-1][j+1]:
                        self.solver.addClauses([-self.IndexOfVar[i+1][j+1][i][j], -self.IndexOfVar[i-1][j+1][i][j]])
                    if self.inMatrix(i+1, j+1) and self.inMatrix(i-1, j-1) and self.canDraw[i+1][j+1] and self.canDraw[i-1][j-1]:
                        self.solver.addClauses([-self.IndexOfVar[i+1][j+1][i][j], -self.IndexOfVar[i-1][j-1][i][j]])
                    if self.inMatrix(i+1, j-1) and self.inMatrix(i-1, j-1) and self.canDraw[i+1][j-1] and self.canDraw[i-1][j-1]:
                        self.solver.addClauses([-self.IndexOfVar[i+1][j-1][i][j], -self.IndexOfVar[i-1][j-1][i][j]])
                    if self.inMatrix(i+1, j-1) and self.inMatrix(i-1, j+1) and self.canDraw[i+1][j-1] and self.canDraw[i-1][j+1]:
                        self.solver.addClauses([-self.IndexOfVar[i+1][j-1][i][j], -self.IndexOfVar[i-1][j+1][i][j]])
                    if self.inMatrix(i-1, j+1) and self.inMatrix(i-1, j-1) and self.canDraw[i-1][j+1] and self.canDraw[i-1][j-1]:
                        self.solver.addClauses([-self.IndexOfVar[i-1][j+1][i][j], -self.IndexOfVar[i-1][j-1][i][j]])

        # Path(x,y,a,b) and Path(a,b,a+1,b+1)=> Path(x,y,a+1,b+1) and 
        for i in range(self.size):
            for j in range(self.size):
                for k in range(self.size):
                    for h in range(self.size):
                        if self.diff(i, j, k, h) and self.canDraw[i][j] and self.canDraw[k][h]:
                            if self.inMatrix(k+1, h+1) and self.canDraw[k+1][h+1]:
                                self.solver.addClauses([-self.IndexOfVar[i][j][k][h], -self.IndexOfVar[k][h][k+1][h+1], self.IndexOfVar[i][j][k+1][h+1]])
                            if self.inMatrix(k+1, h-1) and self.canDraw[k+1][h-1]:
                                self.solver.addClauses([-self.IndexOfVar[i][j][k][h], -self.IndexOfVar[k][h][k+1][h-1], self.IndexOfVar[i][j][k+1][h-1]])
                            if self.inMatrix(k-1, h+1) and self.canDraw[k-1][h+1]:
                                self.solver.addClauses([-self.IndexOfVar[i][j][k][h], -self.IndexOfVar[k][h][k-1][h+1], self.IndexOfVar[i][j][k-1][h+1]])
                            if self.inMatrix(k-1, h-1) and self.canDraw[k-1][h-1]:
                                self.solver.addClauses([-self.IndexOfVar[i][j][k][h], -self.IndexOfVar[k][h][k-1][h-1], self.IndexOfVar[i][j][k-1][h-1]])   
    # print(self.zones)
    def get_number_of_variables(self):
        return self.numberVars
