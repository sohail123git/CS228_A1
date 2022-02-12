from z3 import *
from itertools import combinations
def atmost_one(literals):
    s= [Bool("s_%i" % (x))for y in len(literals))]
    c=[]
    c += [Or([Not(literal[0]),s[0]])]
    for i in range(1,len(literals)-1):
        a = Or([literals[i],s[i-1]])
        c += [Or([Not(a),s[i]])]
        c += [Or([Not(s[i-1]),Not(literals[i])])]
    c += [Or([Not(s[len(literals)-1]),Not(literals[len(literals)-1])])]
    return And(c)

def atleast_one(literals):
    return Or(literals)

    
turns = 17
n = 6
idH = 2
idV = 2
idM = 2
M = [[[[Bool("m_%i_%i_%i_%i" % (k,t,i,j))for j in range(n)]for i in range(n)]for t in range(turns)]for k in range(idM)]
V = [[[[Bool("v_%i_%i_%i_%i" % (k,t,i,j))for j in range(n)]for i in range(n)]for t in range(turns)]for k in range(idV)]
H = [[[[Bool("h_%i_%i_%i_%i" % (k,t,i,j))for j in range(n)]for i in range(n)]for t in range(turns)]for k in range(idH)]
HML = [[Bool("hml_%i_%i" % (x,t))for t in range(turns-1)]for x in range(idH)]
HMR = [[Bool("hmr_%i_%i" % (x,t))for t in range(turns-1)]for x in range(idH)]
VMU = [[Bool("vmu_%i_%i" % (x,t))for t in range(turns-1)]for x in range(idV)]
VMD = [[Bool("vmd_%i_%i" % (x,t))for t in range(turns-1)]for x in range(idV)]
s=Solver()

for turn in range(turns-1):
    temp=[]
    for id in range(idH):
        temp += [HML[id][turn]]
        temp += [HMR[id][turn]]
    for id in range(idV):
        temp += [VMU[id][turn]]
        temp += [VMD[id][turn]]
    s.add(atleast_one(temp))
    s.add(atmost_one(temp))


# Each cell will have atmost one car or mine at a position at a time 
for turn in range(turns):
    for i in range(n):
        for j in range(n):
            temp=[]
            for id in range (idH):
                temp += [H[id][turn][i][j]]
            for id in range (idM):
                temp += [M[id][turn][i][j]]
            for id in range (idV):
                temp += [V[id][turn][i][j]]
            s.add(atmost_one(temp))

# Each mine will have one position at a time
for turn in range(turns):
    for id in range(idM):
        temp = []
        for i in range(n):
            for j in range(n):
                temp += [M[id][turn][i][j]]
        s.add(atmost_one(temp))
        s.add(atleast_one(temp))

print("reached the beginning")
# Each vertical car can have only 2 positions at a time
for turn in range(turns):
    for id in range(idV):
        temp = []
        for i in range(n):
            for j in range(n):
                temp += [Not(V[id][turn][i][j])]
        temp3 = []
        for pair in combinations(temp,2):
            temp2 = temp.copy()
            a, b = pair[0], pair[1]
            temp2.remove(a)
            temp2.remove(b)
            temp2 += [Not(a)]
            temp2 += [Not(b)]
            temp3 += [And(temp2)]
        s.add(Or(temp3))

# Each Horizontal car can have only 2 positions at a time
for turn in range(turns):
    for id in range(idH):
        temp = []
        for i in range(n):
            for j in range(n):
                temp += [Not(H[id][turn][i][j])]
        temp3 = []
        for pair in combinations(temp,2):
            temp2 = temp.copy()
            a, b = pair[0], pair[1]
            temp2.remove(a)
            temp2.remove(b)
            temp2 += [Not(a)]
            temp2 += [Not(b)]
            temp3 += [And(temp2)]
        s.add(Or(temp3))

print("ending")
# constraint that adjacent boxes should be taken for a car
for turn in range(turns):
    for id in range (idV):
        temp = []
        for i in range(1,n-1):
            for j in range(n):
                temp += [And([V[id][turn][i][j],V[id][turn][i+1][j]])]
                temp += [And([V[id][turn][i][j],V[id][turn][i-1][j]])]
        s.add(Or(temp))
for turn in range(turns):
    for id in range (idH):
        temp = []
        for i in range(n):
            for j in range(1,n-1):
                temp += [And([H[id][turn][i][j],H[id][turn][i][j-1]])]
                temp += [And([H[id][turn][i][j],H[id][turn][i][j+1]])]
        s.add(Or(temp))

# mines never move
for id in range (idM):
    for i in range(n):
        for j in range(n): 
            temp = []
            for turn in range(turns):
                    if turn<turns-1:
                        temp += [Or([Not(M[id][turn][i][j]),M[id][turn+1][i][j]])]
            s.add(And(temp))

# Simulating the motion Horizontal car moves right
for id in range (idH):
    for t in range(turns-1):
        for i in range(n):
            for j in range(n): 
                if j>0:
                    s.add(Or([Not(And([HML[id][t],H[id][t][i][j]])),H[id][t+1][i][j-1]]))
                    s.add(Or([Not(And([Not(HML[id][t]),Not(HMR[id][t]),H[id][t][i][j]])),H[id][t+1][i][j]]))
                else:
                    s.add(Or([Not(HML[id][t]),Not(H[id][t][i][j])]))
                    s.add(Or([Not(And([Not(HML[id][t]),Not(HMR[id][t]),H[id][t][i][j]])),H[id][t+1][i][j]]))
for id in range (idH):
    for t in range(turns-1):
        for i in range(n):
            for j in range(n):
                if j<n-1: 
                    s.add(Or([Not(And([HMR[id][t],H[id][t][i][j]])),H[id][t+1][i][j+1]]))
                    s.add(Or([Not(And([Not(HML[id][t]),Not(HMR[id][t]),H[id][t][i][j]])),H[id][t+1][i][j]]))
                else:
                    s.add(Or([Not(HMR[id][t]),Not(H[id][t][i][j])]))
                    s.add(Or([Not(And([Not(HML[id][t]),Not(HMR[id][t]),H[id][t][i][j]])),H[id][t+1][i][j]]))
for id in range (idV):
    for t in range(turns-1):
        for i in range(n):
            for j in range(n):
                if i>0: 
                    s.add(Or([Not(And([VMU[id][t],V[id][t][i][j]])),V[id][t+1][i-1][j]]))
                    s.add(Or([Not(And([Not(VMU[id][t]),Not(VMD[id][t]),V[id][t][i][j]])),V[id][t+1][i][j]]))
                else:
                    s.add(Or([Not(VMU[id][t]),Not(V[id][t][i][j])]))
                    s.add(Or([Not(And([Not(VMU[id][t]),Not(VMD[id][t]),V[id][t][i][j]])),V[id][t+1][i][j]]))
for id in range (idV):
    for t in range(turns-1):
        for i in range(n):
            for j in range(n):
                if i<n-1: 
                    s.add(Or([Not(And([VMD[id][t],V[id][t][i][j]])),V[id][t+1][i+1][j]]))
                    s.add(Or([Not(And([Not(VMU[id][t]),Not(VMD[id][t]),V[id][t][i][j]])),V[id][t+1][i][j]]))
                else:
                    s.add(Or([Not(VMD[id][t]),Not(V[id][t][i][j])]))
                    s.add(Or([Not(And([Not(VMU[id][t]),Not(VMD[id][t]),V[id][t][i][j]])),V[id][t+1][i][j]]))

temp = []
for turn in range(turns):
    for i in range(n):
        temp += [H[0][turn][i][n-1]]
s.add(atleast_one(temp))      

s.add(H[0][0][2][1])
s.add(H[0][0][2][2])
s.add(H[1][0][3][2])
s.add(H[1][0][3][3])
s.add(V[0][0][1][3])
s.add(V[0][0][2][3])
s.add(V[1][0][2][5])
s.add(V[1][0][3][5])
s.add(M[0][0][0][3])
s.add(M[1][0][3][1])

print("----SIMULATING------")
print(s.check())
m = s.model()
for t in range(turns):
  print("_______________________")
  for i in range(n):
    line=""
    for j in range(n):
        flag=False
        for id in range(idM):
            if m.evaluate(M[id][t][i][j]):
                line+="M "
                flag=True
        for id in range(idH):
            if m.evaluate(H[id][t][i][j]):
                if(id==0):
                    line+="R "
                else:
                    line+="H "
                flag=True
        for id in range(idV):
            if m.evaluate(V[id][t][i][j]):
                line+="V "
                flag=True
        if not flag:
            line+="O "
    print(line)
print("--------")
for turn in range(turns-1):
    for id in range(idV):
        print("----------")
        if m.evaluate(VMD[id][turn]):
            print("DOWN")
        if m.evaluate(VMU[id][turn]):
            print("UP")
