import numpy as np
import inspect
import copy
import sys
import os
import pandas as pd
from Functions import *
from Constraint import Constraint
from Intializations import *

params = pd.read_excel("input.xlsx")
problem=params["problem"][0].lower().strip()
algorithm_type=params["algorithm"][0]
heuristic_type=params["heuristic"][0]
N=int(params["N"][0])
c=params["c"][0]
try:
    c=int(c)
except:
    c=None
if(type(c)==int):
    c=int(c)
else:
    c=None
verbose=params["verbose"][1]
if(verbose==1):
    verbose=True
else:
    verbose=False
if(problem=="map_coloring"):
    print("Going to solve map coloring problem")
    additional_data= pd.read_excel("data_map_coloring.xlsx")
    values = [list(x) for x in additional_data.values]     
    csp_coloring= initializeColoringProblem(algorithm_type,heuristic_type,N,c,output_type="file"
                                            ,connections=values,verbose=verbose) 
    csp_coloring.solve()
elif(problem=="sodoku"):
    print("Going to solve sodoku problem")
    additional_data=pd.read_excel("data_sodoku.xlsx")
    values = [list(x) for x in additional_data.values]    
   
    csp_N_Sodoku= initializeSodokuProblem(algorithm_type,heuristic_type,N,values,verbose=verbose,output_type="file")
    csp_N_Sodoku.solve() 
else:
    print("Going to NQueens problem")
    csp_nQueens= initializeNQueensProblem(N,verbose=verbose,output_type="file")
    csp_nQueens.solve() 