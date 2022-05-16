
class MINISAT:
    def __init__(self):
        self.clauses = []
        
    def addClauses(self, arr):
        self.clauses.append(arr)
    
    def get_number_of_clauses(self):
        return len(self.clauses)