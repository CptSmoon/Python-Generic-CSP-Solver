import copy
import numpy as np
import inspect
import copy
import sys
from Functions import *
from Constraint import Constraint
from CSP import CSP
def initializeNQueensProblem(n,verbose=False,output_type="stdout"):
    """
    Let's try n queens game now
    For the constraints, all the elements should be different, so that no two queens are on the same row
    and
    no queens are on the same diagonal
    """
    domains=[]
    for i in range(n):
        domains.append(list(range(n)))
    constraints = [Constraint(lambda x,y : testNQueens(x,y))]
    csp_nQueens  = CSP(domains,constraints,"bt",printBoard,pickType="MRV",output_type=output_type,verbose=verbose)
    return csp_nQueens


def initializeColoringProblem(algorithm,heuristic,n_towns,n_colors,connections,verbose=False,output_type="stdout"):
    """
    Let's try Coloring problem now
    For the constraints, no connected cities should have same color, that's all
    """
    domains=[]
    for i in range(n_towns):
        domains.append(list(range(n_colors)))
    #The constraint takes x which is the assignment and y the isAssigned and z the connections    
    constraints=[]
    constraints.append(Constraint(lambda x,y,z: testColoring(x,y,z)))
    
    csp_coloring=CSP(domains,constraints,algorithm,print,heuristic,additional=connections,output_type=output_type,verbose=verbose)
    return csp_coloring

def initializeSodokuProblem(algorithm,heuristic,N,preset,verbose=True,output_type="stdout"):
    """
    Let's try Sodoku problem now
    For the presetted, we receive a list of coordinates from (1 to N, 1 to N) and from 1 to N denoting value
    We have to initialize addit
    """
    if(N==9):
        n=9
    elif(N==3):
        n=9
    elif(N==4):
        n=4
    domains=[]
    for i in range(N*N):
        domains.append(list(range(n+1))[1:])
    constraints=[]
    constraints.append(Constraint(lambda x,y: testSodoku(x,y)))
    values=np.full(N*N,'.')
    assigned=np.full(N*N,0)

    for i in preset:
        x,y,v=i
        index= (x-1)*N+y-1
        values[index]=int(v)
        assigned[index]=1
    values=list(values)
    assigned=list(assigned)
    sodokuFormater(values)
    
    csp_n_sodoku=CSP(domains,constraints,algorithm,sodokuFormater,heuristic,None,values,assigned,output_type=output_type,
                     verbose=True)
    return csp_n_sodoku
