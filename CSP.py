import copy
import numpy as np
from Functions import *
from Constraint import Constraint
class CSP:
    def __init__(self, domains,constraints,algorithm,printMethod,pickType="naive"
                 ,additional=None,variables=None,assigned=None,output_type="stdout",verbose=False):
        self.pickType=pickType

        if(variables==None):
            self.variables = np.full(len(domains), 0)
        else:
            self.variables =variables
        if(assigned==None):
            self.assigned= np.full(len(domains),0)
        else:
            self.assigned=assigned

        try:
            os.remove("./output.txt")
        except OSError:
            pass
        try:
            os.remove("./trace.txt")
        except OSError:
            pass
        
        self.domains = domains
        self.initialDomains = copy.deepcopy(domains)
        self.constraints = constraints
        self.algorithm=algorithm
        self.solutionNumber = 1
        self.printMethod=printMethod
        self.additional=additional
        self.output_type=output_type
        self.verbose=verbose
        
    def solve(self):
        if(self.algorithm=="bt"):
            self.backtracking(0)
        elif(self.algorithm=="fcc"):
            self.ForwardChecking(0)
        elif(self.algorithm=="ac3"):
            self.ArcConsistency(0)
    def backtracking(self,level):
    #Check if all the variables are assigned
        if(self.verbose):
            print_out(self.printMethod,"Entering level "+str(level),self.output_type,"trace",False)
#             print_out(self.printMethod,self.assigned,self.output_type,"output",False)

        if allAssigned(self.variables,self.assigned):
#             print("Gonna print self.assigned of level "+str(level))
#             print(self.assigned)
            print_out(self.printMethod,"Solution number "+str(self.solutionNumber)+" : ",self.output_type,"output",False)
            print_out(self.printMethod,self.variables,self.output_type,"output",True)
            self.solutionNumber=self.solutionNumber+1
            #Return for more solutions, exit for one solution
            return
        #Else
        #Pick one unassigned variable
        index = pickUnassignedVariable(self.variables,self.assigned,self.domains,self.constraints,self.pickType,self.additional)
        self.assigned[index]=1
        #Now, loop through the domain of the picked variable
#         print(self.domains)
        for d in self.domains[index]:
            self.variables[index]=int(d)
            if(self.verbose):
                print_out(self.printMethod,"Gonna print variables for domain element "+str(d)
                          ,self.output_type,"trace",False)
            print_out(self.printMethod,self.variables,self.output_type,"trace",True)

#             print("variables : " + str(self.variables))
#             printBoard(self.variables)
#             print("assigned : " + str(self.assigned))
            #Suppose that the picked variable is okay
            ok = True
            #Loop through every constraint C and test if assignment is ok
            for C in self.constraints:
#                 print(C.check(self.variables,self.assigned))
#                 print(self.variables)
                if C.check(self.variables,self.assigned,self.additional) == False:
                    if(self.verbose):
                        print_out(self.printMethod,"A constraint is unsatisfied for this one, skipping"
                                  ,self.output_type,"trace",False)
                    ok = False

            if(ok):
                if(self.verbose):print_out(self.printMethod,"The domain variable is validated, going to next level"
                                             ,self.output_type,"trace",False)
                self.backtracking(level+1)
            if(index<len(self.assigned)-1):
                self.assigned[index+1]=0
        
        return
    def ForwardChecking(self,level):
    #Check if all the variables are assigned
        if(self.verbose):
            print_out(self.printMethod,"Entering level "+str(level),self.output_type,"trace",False)
#             print_out(self.printMethod,self.assigned,self.output_type,"output",False)
        if allAssigned(self.variables,self.assigned):
#             print("Gonna print self.assigned of level "+str(level))
#             print(self.assigned)
            self.solutionNumber=self.solutionNumber+1
            print_out(self.printMethod,"Solution number "+str(self.solutionNumber)+" : ",self.output_type,"output",False)
            print_out(self.printMethod,self.variables,self.output_type,"output",True)
            #Return for more solutions, exit for one solution
            return
        #Else
        #Pick one unassigned variable
        index = pickUnassignedVariable(self.variables,self.assigned,self.domains,self.constraints,self.pickType,self.additional)
        self.assigned[index]=1
        #Now, loop through the domain of the picked variable
        for d in self.domains[index]:
            self.variables[index]=int(d)
            if(self.verbose):
                print_out(self.printMethod,"Gonna print variables for domain element "+str(d)
                          ,self.output_type,"trace",False)
                print_out(self.printMethod,self.variables,self.output_type,"trace",True)
#             print("variables : " + str(self.variables))
#             print("assigned : " + str(self.assigned))
#             print("domains : "+str(self.domains))
#             printBoard(self.variables)
            #Suppose that the picked variable is okay
            DomainEmpty = False
            #Save the domain
            toBeRestored = copy.deepcopy(self.domains)
            #Loop through every constraint C and test if assignment is ok
            for C in self.constraints:
#                 print(C.check(self.variables,self.assigned))
                if FCCheck(C,self.variables,self.assigned,self.domains,self.additional) == True:
                    DomainEmpty = True
                    if(self.verbose):
                        print_out(self.printMethod,"FCC returns that this domain variable isn't assignable"
                                  ,self.output_type,"trace",False)
                    break
            if(not DomainEmpty):
#                 print("Okay were good until now : "+str(self.variables))
                if(self.verbose):
                        print_out(self.printMethod,"The domain variable is validated, going to next level"
                                  ,self.output_type,"trace",False)
                self.ForwardChecking(level+1)

            #Restore the domains like before the FCC
            self.domains=toBeRestored
            if(index<len(self.assigned)-1):
                self.assigned[index+1]=0    
    def ArcConsistency(self,level):
            copyDomains = copy.deepcopy(self.domains)
#           For every Arc:
            for index, x in enumerate(self.variables):
                for jindex, y in enumerate(self.variables):
                    if(jindex>index):
                        self.assigned[index]=1
                        self.assigned[jindex]=1
#                       Set the both nodes as assigned
#                       Now for every constraint, if a variable has no possible variable
#                       to pick from with it, that's an inconsistent arc
                        for C in self.constraints:
                            jj=0
                            for aindex,a  in enumerate(self.domains[index]):
                                numY = len(self.domains[index])
                                for bindex,b in enumerate(self.domains[jindex]):
                                    self.variables[index]=self.domains[index][aindex]
                                    self.variables[jindex]=self.domains[jindex][bindex]
                                    
                                    if(C.check(self.variables,self.assigned,self.additional)==False):
                                        numY=numY-1
                                if numY == 0:

                                    del(copyDomains[index][jj])
                                    jj=jj-1

                                jj=jj+1
                                    
                        self.assigned[index]=0
                        self.assigned[jindex]=0
            #Now test if there is an empty domain: no solution possible
            #       if there is a unique solution print it
            #       else, call backtracking
            self.domains=copyDomains
            for domain in self.domains:
                if len(domain)==0:
                    print_out(self.printMethod,"No possible solutions can be found "+
                              str(self.solutionNumber)+" : ",self.output_type,"output",False)

                    
                    return
            for domain in self.domains:
                if len(domain)>1:
                    self.backtracking(0)
                    return
            print_out("One possible solution : ",self.variables,self.output_type,"output",False)
            result=[]
            for element in self.domains:
                result.append(element)
            print_out(result,self.variables,self.output_type,"output",True)

            return
        
        