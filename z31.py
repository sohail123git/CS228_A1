from z3 import *
from itertools import combinations
def atmost_one(literals):
    c=[]
    for pair in combinations(literals,2):
        a, b = pair[0], pair[1]
        c += [Or([Not(a),Not(b)])]
    return And(c)
def atleast_one(literals):
    return Or(literals)
turns = 1
n = 4
idH = 1
idV = 4
idM =1
M = [[[[Bool("m_%i_%i_%i_%i" % (k,t,i,j))for j in range(n)]for i in range(n)]for t in range(turns)]for k in range(idM)]
V = [[[[Bool("v_%i_%i_%i_%i" % (k,t,i,j))for j in range(n)]for i in range(n)]for t in range(turns)]for k in range(idV)]
H = [[[[Bool("h_%i_%i_%i_%i" % (k,t,i,j))for j in range(n)]for i in range(n)]for t in range(turns)]for k in range(idH)]

s=Solver()

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

# Each vertical car can have only 2 positions at a time
for turn in range(turns):
    for id in range(idV):
        temp = []
        for i in range(n):
            for j in range(n):
                temp += [V[id][turn][i][j]]
        temp2 = []
        for pair in combinations(temp,2):
            c = []
            a, b = pair[0], pair[1]
            c += [a]
            c += [b]
            for p in range(n):
                for q in range(n):
                    if (not(V[id][turn][p][q]==a) and not(V[id][turn][p][q]==b)):
                        c += [Not(V[id][turn][p][q])]
            temp2 += [And(c)]
        s.add(Or(temp2))

# Each Horizontal car can have only 2 positions at a time
for turn in range(turns):
    for id in range(idH):
        temp = []
        for i in range(n):
            for j in range(n):
                temp += [H[id][turn][i][j]]
        temp2 = []
        for pair in combinations(temp,2):
            c = []
            a, b = pair[0], pair[1]
            c += [a]
            c += [b]
            for p in range(n):
                for q in range(n):
                    if (not(H[id][turn][p][q]==a) and not(H[id][turn][p][q]==b)):
                        c += [Not(H[id][turn][p][q])]
            temp2 += [And(c)]
        s.add(Or(temp2))
print(s.check())

m = s.model()
t=0
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
                line+="H "
                flag=True
        for id in range(idV):
            if m.evaluate(V[id][t][i][j]):
                line+="V "
                flag=True
        if not flag:
            line+="O "
    print(line)