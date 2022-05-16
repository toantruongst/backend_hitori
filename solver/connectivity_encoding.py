import numpy as np
    
class ConnectivityEncoding:
    def __init__(self, size, value, solver):
        self.size = size
        self.value_of_cell = value
        self.solver = solver
        self.canDraw = np.full((self.size, self.size), False, dtype=bool)
        self.zones = np.full((self.size, self.size), 0, dtype=int) # full 0 zone
        self.path = np.full((self.size, self.size, self.size, self.size), 0, dtype=int)
        self.white = np.full((self.size, self.size), 0, dtype=int) # full 0 white
        # self.max_var_in_borad = 0
        self.number_of_vars = 0
        self.number_of_clauses = 0

    def encode_vars(self):
        # Tim cac o cung hang co the boi den co gia tri bang nhau
        for i in range(self.size):                       
            for j in range(self.size):            
                for k in range(j+1, self.size):
                    if self.value_of_cell[i][j] == self.value_of_cell[i][k]:
                        self.canDraw[i][j] = True
                        self.canDraw[i][k] = True

        # Tim cac o cung cot co the boi den co gia tri bang nhau
        for j in range(self.size):
            for i in range(self.size - 1):
                for k in range(i+1, self.size):
                    if self.value_of_cell[i][j] == self.value_of_cell[k][j]:
                        self.canDraw[i][j] = True
                        self.canDraw[k][j] = True


        # Gan gia tri vao tung o trang
        for i in range(self.size):
            for j in range(self.size):
                if self.canDraw[i][j]:
                    self.number_of_vars += 1
                    self.white[i][j] = self.number_of_vars
                    
        # self.max_var_in_borad = self.number_of_vars

        # zones
        zone_number = 0

        for i in range(self.size):
            for j in range(self.size):
                if self.canDraw[i][j] and self.zones[i][j] == 0:
                    zone_number += 1
                    self.find_zone(i,j,zone_number)
        
        # set path
        for i in range(self.size):
            for j in range(self.size):
                for k in range(self.size):
                    for h in range(self.size):
                        if self.zones[i][j] != 0 and self.zones[i][j] == self.zones[k][h] and self.path[i][j][k][h] == 0:
                            self.number_of_vars += 1
                            self.path[i][j][k][h] = self.number_of_vars


    def find_zone(self, i, j, zone_number):
        self.zones[i][j] = zone_number
        if i+1 < self.size and j+1 < self.size and self.canDraw[i+1][j+1] and self.zones[i+1][j+1] == 0:
            self.find_zone(i+1, j+1, zone_number)
        if i-1 >= 0 and j+1 < self.size and self.canDraw[i-1][j+1] and self.zones[i-1][j+1] == 0:
            self.find_zone(i-1, j+1, zone_number)
        if i+1 < self.size and j-1 >= 0 and self.canDraw[i+1][j-1] and self.zones[i+1][j-1] == 0:
            self.find_zone(i+1, j-1, zone_number)
        if i-1 >= 0 and j-1 >= 0 and self.canDraw[i-1][j-1] and self.zones[i-1][j-1] == 0:
            self.find_zone(i-1, j-1, zone_number)
    
    def in_matrix(self, x, y):
        return x >= 0 and x < self.size and y >= 0 and y < self.size
    
    def diff(self, x, y, a, b):
        return x!=a or y!=b

    # CNF Rule 1
    def cnf_rule_01(self):
        for i in range(self.size):
            for j in range(self.size):
                for k in range(j+1, self.size):
                    if self.value_of_cell[i][j] == self.value_of_cell[i][k]:
                        self.solver.addClauses([-1 * self.white[i][j], -1*self.white[i][k]])
        
        for j in range(self.size):
            for i in range(self.size - 1):
                for k in range(i+1, self.size):
                    if self.value_of_cell[i][j] == self.value_of_cell[k][j]:
                        self.solver.addClauses([-1*self.white[i][j],-1*self.white[k][j]])
    
    # CNF Rule 2
    def cnf_rule_02(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.canDraw[i][j]:         
                    if i-1 >= 0 and self.canDraw[i-1][j]:
                        self.solver.addClauses([self.white[i][j], self.white[i-1][j]])

                    if j-1 >= 0 and self.canDraw[i][j-1]:
                        self.solver.addClauses([self.white[i][j],self.white[i][j-1]])
    
    # Rule 3
    def cnf_rule_03(self):
        # (x,y) Bien thi di vao trong

        for i in range(self.size):
            for j in range(self.size):
                if self.canDraw[i][j]:
                    self.solver.addClauses([-self.path[i][j][i][j]])
                
                    if self.in_matrix(i+1, j+1) and self.canDraw[i+1][j+1]:
                        if i == 0 or i == self.size-1 or j == 0 or j == self.size-1:
                            self.solver.addClauses([self.white[i][j], self.white[i+1][j+1], self.path[i][j][i+1][j+1]])
                            
                        elif i+1 == 0 or i+1 == self.size-1 or j+1 == 0 or j+1 == self.size-1:
                            self.solver.addClauses([self.white[i][j], self.white[i+1][j+1], self.path[i+1][j+1][i][j]])
                        else:
                            self.solver.addClauses([self.white[i][j], self.white[i+1][j+1], self.path[i][j][i+1][j+1], self.path[i+1][j+1][i][j]])
                    
                    if self.in_matrix(i+1, j-1) and self.canDraw[i+1][j-1]:
                        if i == 0 or i == self.size-1 or j == 0 or j == self.size-1:
                            self.solver.addClauses([self.white[i][j], self.white[i+1][j-1], self.path[i][j][i+1][j-1]])

                        if i+1 == 0 or i+1 == self.size-1 or j-1 == 0 or j-1 == self.size-1:
                            self.solver.addClauses([self.white[i][j], self.white[i+1][j-1], self.path[i+1][j-1][i][j]])

                        if i > 0 and i < self.size-1 and j > 0 and j < self.size-1 and i+1 > 0 and i+1 < self.size-1 and j-1 > 0 and j-1 < self.size-1:
                            self.solver.addClauses([self.white[i][j], self.white[i+1][j-1], self.path[i][j][i+1][j-1], self.path[i+1][j-1][i][j]])

        for i in range(self.size):
            for j in range(self.size):
                if self.canDraw[i][j]:
                    if self.in_matrix(i+1, j+1) and self.in_matrix(i+1, j-1) and self.canDraw[i+1][j+1] and self.canDraw[i+1][j-1]:
                        self.solver.addClauses([-self.path[i+1][j+1][i][j], -self.path[i+1][j-1][i][j]])
                    if self.in_matrix(i+1, j+1) and self.in_matrix(i-1, j+1) and self.canDraw[i+1][j+1] and self.canDraw[i-1][j+1]:
                        self.solver.addClauses([-self.path[i+1][j+1][i][j], -self.path[i-1][j+1][i][j]])
                    if self.in_matrix(i+1, j+1) and self.in_matrix(i-1, j-1) and self.canDraw[i+1][j+1] and self.canDraw[i-1][j-1]:
                        self.solver.addClauses([-self.path[i+1][j+1][i][j], -self.path[i-1][j-1][i][j]])
                    if self.in_matrix(i+1, j-1) and self.in_matrix(i-1, j-1) and self.canDraw[i+1][j-1] and self.canDraw[i-1][j-1]:
                        self.solver.addClauses([-self.path[i+1][j-1][i][j], -self.path[i-1][j-1][i][j]])
                    if self.in_matrix(i+1, j-1) and self.in_matrix(i-1, j+1) and self.canDraw[i+1][j-1] and self.canDraw[i-1][j+1]:
                        self.solver.addClauses([-self.path[i+1][j-1][i][j], -self.path[i-1][j+1][i][j]])
                    if self.in_matrix(i-1, j+1) and self.in_matrix(i-1, j-1) and self.canDraw[i-1][j+1] and self.canDraw[i-1][j-1]:
                        self.solver.addClauses([-self.path[i-1][j+1][i][j], -self.path[i-1][j-1][i][j]])

        # Path(x,y,a,b) and Path(a,b,a+1,b+1)=> Path(x,y,a+1,b+1) and 
        for i in range(self.size):
            for j in range(self.size):
                for k in range(self.size):
                    for h in range(self.size):
                        if self.diff(i, j, k, h) and self.zones[k][h] == self.zones[i][j] and self.zones[i][j] != 0:
                            if self.in_matrix(k+1, h+1) and self.zones[k+1][h+1] == self.zones[i][j]:
                                self.solver.addClauses([-self.path[i][j][k][h], -self.path[k][h][k+1][h+1], self.path[i][j][k+1][h+1]])
                            if self.in_matrix(k+1, h-1) and self.zones[k+1][h-1] == self.zones[i][j]:
                                self.solver.addClauses([-self.path[i][j][k][h], -self.path[k][h][k+1][h-1], self.path[i][j][k+1][h-1]])
                            if self.in_matrix(k-1, h+1) and self.zones[k-1][h+1] == self.zones[i][j]:
                                self.solver.addClauses([-self.path[i][j][k][h], -self.path[k][h][k-1][h+1], self.path[i][j][k-1][h+1]])
                            if self.in_matrix(k-1, h-1) and self.zones[k-1][h-1] == self.zones[i][j]:
                                self.solver.addClauses([-self.path[i][j][k][h], -self.path[k][h][k-1][h-1], self.path[i][j][k-1][h-1]])   
    # print(self.zones)
    def get_number_of_variables(self):
        return self.number_of_vars
