import time
import matplotlib.pyplot as plt
import networkx as nx
import csv
import random


class CNF:
    def __init__(self,Pnum) -> None:
        self.problem = Pnum
        self.variables = 0
        self.satisfiable = '?'
        self.clauses = []
        self.graph = nx.DiGraph()
        self.SCCTime = None
        self.DumbSatTime = None

    def add_clause(self,var1, var2):
        self.clauses.append([var1,var2])
        self.graph.add_edge(var1,var2)

#Returns CNFs from CSV file
def read_csv(file_name):
    cnfs = []
    clauses = 0
    with open(file_name,mode='r') as file:
        csvFile = csv.reader(file)
        for line in csvFile:
            tempcnf = CNF(int(line[1]))
            line_two = next(csvFile)
            tempcnf.variables = int(line_two[2])
            clauses = int(line_two[3])
            #add clauses to CNF
            for i in range(clauses):
                clause = next(csvFile)
                tempcnf.add_clause(int(clause[0]),int(clause[1]))
            cnfs.append(tempcnf)
    return cnfs

def two_sat(clauses, num_vars):
    graph = nx.DiGraph()
    #Creates list for all variables
    for i in range(1, num_vars+1):
        graph.add_node(i)
        graph.add_node(-i)
    #Creates implications. For every clause we find what assignments will make it true if either assigment is false
    for i, j in clauses:
        graph.add_edge(-i,j)
        graph.add_edge(-j,i)
    #finds strongly connected components
    scc_map = nx.strongly_connected_components(graph)
    # if a variable and it's complement is in the same scc, then it's not satisfiable
    for scc in scc_map:
        for val in scc:
            if -val in scc:
                return False
    return True

#DUMB SAT

def check(Wff,Nvars,Nclauses,Assignment):
# Run thru all possibilities for assignments to wff
# Starting at a given Assignment (typically array of Nvars+1 0's)
# At each iteration the assignment is "incremented" to next possible
# At the 2^Nvars+1'st iteration, stop - tried all assignments
    Satisfiable=False
    while (Assignment[Nvars+1]==0):
        # Iterate thru clauses, quit if not satisfiable
        for i in range(0,Nclauses): #Check i'th clause
            Clause=Wff[i]
            Satisfiable=False
            for j in range(0,len(Clause)): # check each literal
                Literal=Clause[j]
                if Literal>0: Lit=1
                else: Lit=0
                VarValue=Assignment[abs(Literal)] # look up literal's value
                if Lit==VarValue:
                    Satisfiable=True
                    break
            if Satisfiable==False: break
        if Satisfiable==True: break # exit if found a satisfying assignment
        # Last try did not satisfy; generate next assignment)
        for i in range(1,Nvars+2):
            if Assignment[i]==0:
                Assignment[i]=1
                break
            else: Assignment[i]=0
    return Satisfiable
    
def build_wff(Nvars,Nclauses,LitsPerClause):
    wff=[]
    for i in range(1,Nclauses+1):
        clause=[]
        for j in range(1,LitsPerClause+1):
            var=random.randint(1,Nvars)
            if random.randint(0,1)==0: var=-var
            clause.append(var)
        wff.append(clause)
    return wff

def test_wff(wff,Nvars,Nclauses):
    Assignment=list((0 for x in range(Nvars+2)))
    start = time.time() # Start timer
    SatFlag=check(wff,Nvars,Nclauses,Assignment)
    end = time.time() # End timer
    exec_time=int((end-start)*1e6)
    return [wff,Assignment,SatFlag,exec_time]


f1 = open("2SAT_Output.txt",'w')

cnfs = read_csv("2SAT.cnf")
for cnf in cnfs:
    start = time.time()
    if two_sat(cnf.clauses, cnf.variables):
        end = time.time()
        cnf.SCCTime = int((end-start)*1e6)
        cnf.satisfiable = 'S'
        f1.write(f"Problem {cnf.problem} is satisfiable and was solved in {cnf.SCCTime} miliseconds\n")
    else:
        end = time.time()
        cnf.SCCTime = int((end-start)*1e6)
        cnf.satisfiable = 'U'
        f1.write(f"Problem {cnf.problem} is unsatisfiable and was solved in {cnf.SCCTime} milisecons\n")

f1.close()

#Plot Results

Two_SAT_times = [x.SCCTime for x in cnfs]
Dumb_SAT_times = [x.DumbSatTime for x in cnfs]
Num_Clauses = [len(x.clauses) for x in cnfs]

plt.figure(figsize=(8,5))

plt.plot(Num_Clauses,Two_SAT_times,label = '2SAT', color = 'blue', marker = 'o')
plt.plot(Num_Clauses,Dumb_SAT_times,label = 'Dumb-SAT', color = 'red', marker = 'x')

plt.xlabel('Number of Clauses')
plt.ylabel('Execution Time (Seconds)')
plt.title('Execution Time Comparison: DumbSAT vs 2SAT')

# Show legend
plt.legend()

# Show grid
plt.grid(True)

# Display the plot
plt.show()