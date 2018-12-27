import copy
import numpy as np
import inspect
import sys
import os
from Constraint import Constraint

"""
*Utility function*
checks if all the variables are assigned,
meaning that all the variables are different from infinity
"""
def allAssigned(variables,assigned):
    for isAssigned in assigned :
        if isAssigned == 0:
            return False
    return True
"""
*Utility Function*
Returns the index of one unassigned variable, for the moment,
we are going to return the first unassigned variable
"""
def pickUnassignedVariable(variables,assigned,domains,constraints,pickType="naive",additional=True):
    if(pickType=="naive"):
        return naive(variables,assigned)
    elif(pickType=="MRV"):
        return MRV(variables,assigned,domains,constraints,additional)

"""
*Utility Function*
Receives an array of queen positions and print them in a board 
"""
def printBoard(positions):
    n = len(positions)
    for i in range(n):
        for j in range(n):
            if(positions[j]==i):
                print("Q",end=' ')
            else:
                print("o",end=' ')
        print()
"""Naive pick function just pick the first one unassigned"""
def naive(variables,assigned):
    for idx, isAssigned in enumerate(assigned) :
        if isAssigned ==  0:
            return idx
"""
*Normal Print*
"""
def normalPrint(positions):
    print(positions)
"""
MRV Constraint
"""    
def MRV(variables,assigned,domains,constraints,additional=None):
    maxD=-999999
    copyVariables = copy.deepcopy(variables)
    copyAssigned = copy.deepcopy(assigned)
    
    for idx, isAssigned in enumerate(assigned):
        if isAssigned == 0:
            num = len(domains[idx])
            for didx,d in enumerate(domains[idx]):
                copyVariables[idx]=d
                copyAssigned[idx]=1
                for C in constraints :
                    if(C.check(variables,assigned,additional)==False):
                        num=num-1
                if(maxD<num):
                    maxD= num
                    idxMax= idx
    return idxMax
"""
Forward Checking the constraint
"""
def FCCheck(C,variables,assigned,domains,additional=True):
#     print("===============")
    #For array of domains in domains list
    localDomains= copy.deepcopy(domains)
    localVariables= copy.deepcopy(variables)
    for index, D in enumerate(localDomains):
        #If that value isn't assigned
        if(assigned[index]==0):
            #for every value d of that Domain
            #Make it assigned for the moment
            assigned[index]=1
#             print("index : "+str(index))
            #index to delete
            jj=0
            for jindex , d in enumerate(D):
                #Affect the value to that index of the variables
                localVariables[index]=d
#                 print("d : "+str(d)+" jindex: "+str(jindex))
                #Now check if the constraint isn't satisfied
#                 print("localVariables : "+ str(localVariables))
#                 print("domains : "+ str(domains))
                if(C.check(localVariables,assigned,additional)==False):
                    #delete that value from the domain
#                     print("will be deleted : "+ str(domains[index][jj]))
                    del(domains[index][jj])
                    jj=jj-1
                jj=jj+1
            assigned[index]=0
    
#         print("===============")
        if(len(domains[index])==0):
                return True
    return False
"""This is the test for NQueens Constraint"""
def testNQueens(values,assigned):
    isUsed={}
    for idx, x  in enumerate(values):
        #if the element isn't yet assigned, just return true
        if(assigned[idx]==0):
            continue
        #if the element isn't already used, mark it as used, and go on
        if(isUsed.get(x)!=1):
            isUsed[x]=1
        #Else return false, since this means that the two elements are on the same row
        else:
            return False
        #Here we are going to test the elements, if they are on the same diagonal or not
        for idy, y in enumerate(values):
            if(assigned[idy]==1):
                if(idx!=idy):
                    if(abs(x-y)==abs(idx-idy)):
                        return False
    return True
"""This is the test for Coloring Constraint"""
def testColors(assignement,assigned,connections):
    #For every connection in the list of the connections
    for c in connections:
    #if the variables implied by that connection are assigned
        if(assigned[int(c[0])]==1)and(assigned[int(c[1])]==1):
    #if they are the same then return false
            if(assignement[int(c[0])]==assignement[int(c[1])]):
                return False
    #we finnished without returning so just return true
    return True
"""Utility function to print formatted sodoku"""
def sodokuFormater(arr):
    N=int(np.sqrt(len(arr)))
    if N==9:
        n=3
    elif N==4:
        n=2
    elif N==3:
        n=3
    else:
        n=int(np.sqrt(N))
    print('|--------------------|')
    print("|",end="")
    for i,x in enumerate(arr):
        if(str(x)=='.'):
            print(".", end=" ")
        else:
            print(x,end=" ")
        if(i+1)%n==0:
            print("|",end="")
        if (i+1)%N == 0:
            print()
            print("|",end="")
        if(i+1)/N%n==0:
            print('--------------------|')
            if(i<len(arr)):
                print("|",end="")

def testSodoku(X,assigned):
    N= int(np.sqrt(len(X)))
    for j in range(N):
        s= [x for i,x in enumerate(X) if ((i % N-j)==0)and assigned[i]==1 and X[i]!='.']
        if(len(np.unique(s))!=len(s)):
            return False
        ss= [x for i,x in enumerate(X) if i<j*N and j>1*N and assigned[i]==1 and X[i]!='.']
        if len(np.unique(ss))!=len(ss):
            return False
    return testSquares(X,assigned)
def testSquares(sodoku,assigned):
    A={}
#     print("I am inside test squares")
#     sodokuFormater(sodoku)
    N = int(np.sqrt(len(sodoku)))
    if(N==3):
        sN=3
    elif(N==4):
        sN=2
    elif(N==9):
        sN=3
    else:
        sN= int(np.sqrt(N))
    squares={}
    for idx,x in enumerate(sodoku):
        i=int((idx / N))%N
        j=idx%N
    #     print(str(i)+" "+str(j))
        idd= str(int(i/sN))+str(int(j/sN))
        if(A.get(idd)==None):
            A[idd]=[x]
        else:
            if(assigned[idx]==1 and sodoku[idx]!='.'):
                A[idd].append(x)
    for element in A:
        if(len(np.unique(A[element]))!=len(A[element])):
#             print("False")
            return False
#     print("True")
    return True    
"""output function"""
def print_out(printMethod,text,type_o="stdout",name="output",isSolution=False):
    original = sys.stdout
    if(type_o=="file"):
        sys.stdout = open('./'+name+'.txt', 'a+')
    if(isSolution):
        printMethod(text)
    else:
        print(text)
    sys.stdout = original

def testColoring(x,y,connections):
    for z in connections :
        if((y[int(z[0])]==1)and (y[int(z[1])]==1)and (x[int(z[0])]==x[int(z[1])])):
            return False
    return True