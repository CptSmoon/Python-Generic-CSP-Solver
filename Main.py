import numpy as np
import inspect
import copy
import sys
import os
from Functions import *
from Constraint import Constraint
from Intializations import *




input_type=""
output_type=""
verbose=""
print("Choose input type : ")
print(" 1 : from console")
print(" 2 : from text file")
input_type=input()
while(input_type!="1" and input_type!="2"):
    print("Réessayez : ")
    input_type=input()
print("Choose output type : ")
print(" 1 : on console")
print(" 2 : on text file")

output_type=input()
while(output_type!="1" and output_type!="2" ):
    print("Réessayez")
    output_type=input()

if(output_type==1):
    output_type="stdout"
else:
    output_type="file"

print("Would you like to print the steps of the resolution ? : ")
print(" 1 : Yes")
print(" 2 : No")
verbose=input()
while(verbose!="1" and verbose!="2"):
    print("Réessayez")
    verbose=input()
if(verbose==2):
    verbose=False
else:
    verbose=True

print("What algorithm do you want to use ? : ")
print(" 1 : Backtrack")
print(" 2 : Forward Checking")
print(" 3 : AC3")
algorithm_type=input()
while(algorithm_type!="1" and algorithm_type!="2" and algorithm_type!="3"):
    print("Réessayez")
    algorithm_type=input()
if(algorithm_type=="1"):
    algorithm_type="bt"
elif(algorithm_type=="2"):
    algorithm_type="fcc"
else:
    algorithm_type="ac3"

print("What Heuristic do you want to use ? : ")
print(" 1 : MRV")
print(" 2 : LCV")
print(" 3 : DH")
heuristic_type=input()
while(heuristic_type!="1" and heuristic_type!="2" and heuristic_type!="3"):
    print("Réessayez")
    heuristic_type=input()
heuristic_type="MRV"

print("What problem do you want to solve ? : ")
print(" 1 : N Queens")
print(" 2 : Map Coloring")
print(" 3 : Sodoku")
print(" 4 : Something Else")
problem_type=input()
while(problem_type!="1" and problem_type!="2" and problem_type!="3" and problem_type!="4"):
    print("Réessayez")
    problem_type=input()

if problem_type=="1":
    print("Enter N between 1 and 10")
    N = int(input())
    csp_nQueens= initializeNQueensProblem(N,verbose=verbose,output_type=output_type)

    csp_nQueens.solve()
elif problem_type=="2":
    print("Enter N, the number of towns : ")
    N= int(input())
    print("Town numbers are : ")
    print(list(range(N)))
    print("Now enter the number of colors : ")
    c = int(input())
    print("Color numbers are : ")
    print(list(range(c)))
    print("Now enter the connections, print # # to finish : ")
    print("Format : town1 town2")
    adgency_list=[]
    t1=0
    t2=0
    while(t1 != '#'):
        while(True):
            try:
                t1,t2 = input().split(" ")
                if(t1=="#"):
                    break       
                t1=int(t1)
                t2=int(t2)
                break
            except ValueError:
                print("Retry please")
            
        if(t1 != '#'):
            adgency_list.append([t1,t2])
    csp_coloring= initializeColoringProblem(algorithm_type,heuristic_type,N,c,output_type=output_type,connections=adgency_list,verbose=verbose) 
    csp_coloring.solve()
elif problem_type=="3":
    print("Enter N, the number of columns (3, 4 or 9) : ")
    N= int(input())
    print("Now enter the predfined numbers, print # # # to finish : ")
    print("Format : row column value")
    adgency_list=[]
    t1=1
    t2=1
    t3=1
    while(t1 != '#'):
        while(True):
            try:
                t1,t2,t3 = input().split(" ")
                if(t1=="#"):
                    break       
                t1=int(t1)
                t2=int(t2)
                t3=int(t3)
                break
            except ValueError:
                print("Retry please")
            
        if(t1 != '#'):
            adgency_list.append([t1,t2,t3])
    csp_N_Sodoku= initializeSodokuProblem(algorithm_type,heuristic_type,N,adgency_list,verbose=verbose,output_type=output_type)
    csp_N_Sodoku.solve()





print("Voila Voila !")
"""
1 1 1
1 2 2
1 3 3
2 1 4
2 2 5
2 3 6
3 1 7
# # #
"""