"""
Binary Constraint
This class will contain the contraint
it will have a check method, returning true or false, based on the assignement
somehow, it has got to store a condition when intializing it

"""
class Constraint:
    def __init__(self, condition):
        self.condition = condition
    #check checks if assignement is coherent with the constraint
    def check(self,assignement,assigned,additional=None):
        if(additional == None):
            return self.condition(assignement,assigned)
        else:
            return self.condition(assignement,assigned,additional)