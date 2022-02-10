from z3 import *
import array as arr
from itertools import combinations

def atleast_one(literals):
    return Or(literals)

def atmost_one(literals):
    c=[]
    for pair in combinations(literals,2):
        a, b = pair[0], pair[1]
        c += [Or([Not(a),Not(b)])]
    return And(c)

s = Solver()

k1 = 11
k1 = k1+1
dim = 6

rx = 2
ry = 1 
o = arr.array('i', [0, 0, 1, 2, 2])
x = arr.array('i', [1, 2, 3, 0, 3])
y = arr.array('i', [3, 5, 2, 3, 1])


cars = 5


H = [ [ [ Bool("h_%s_%s_%s" % (i, j, k)) for k in range(k1) ] for j in range(dim) ] for i in range(dim) ]
V = [ [ [ Bool("v_%s_%s_%s" % (i, j, k)) for k in range(k1) ] for j in range(dim) ] for i in range(dim) ]
R = [ [ [ Bool("r_%s_%s_%s" % (i, j, k)) for k in range(k1) ] for j in range(dim) ] for i in range(dim) ]
M = [ [ [ Bool("m_%s_%s_%s" % (i, j, k)) for k in range(k1) ] for j in range(dim) ] for i in range(dim) ]

for i in range(dim):
    for j in range(dim):
        H[i][j][0] = False
        V[i][j][0] = False
        M[i][j][0] = False
        R[i][j][0] = False

R[rx][ry][0] = True

for w in range(cars):
    if(o[w] == 0): 
        V[x[w]][y[w]][0] = True 
    elif(o[w] == 1): 
        H[x[w]][y[w]][0] = True   
    else: 
        M[x[w]][y[w]][0] = True

# for i in range(dim):
#     print()
#     for j in range(dim):
#         print(M[i][j][0], end=" ")

def updateH(k, i, j):
    temp = []
    for p in range(dim):
        for q in range(dim):
            if(((p == i) and (q == (j-1))) or ((p == i) and (q == j))):
                temp = temp  #donothing
            else:
                temp += [H[p][q][k+1] == H[p][q][k]]
    return And(temp)


def updateV(k, i, j):
    temp = []
    for p in range(dim):
        for q in range(dim):
            if(((p == (i-1)) and (q == j)) or ((p == i) and (q == j))):
                temp = temp #donothing
            else:
                temp += [V[p][q][k+1] == V[p][q][k]]

    return And(temp)


def updateR(k, i, j):
    temp = []
    for p in range(dim):
        for q in range(dim):
            if(((p == i) and (q == (j-1))) or ((p == i) and (q == j))):
                temp = temp #donothing
            else:
                temp += [R[p][q][k+1] == R[p][q][k]]
    return And(temp)



def updateVRM(k):
    temp = []
    for p in range(dim):
        for q in range(dim):
            temp += [V[p][q][k+1] == V[p][q][k]]
            temp += [R[p][q][k+1] == R[p][q][k]] 
            temp += [M[p][q][k+1] == M[p][q][k]]

    return And(temp)


def updateHRM(k):
    temp = []
    for p in range(dim):
        for q in range(dim):
            temp += [H[p][q][k+1] == H[p][q][k]] 
            temp += [R[p][q][k+1] == R[p][q][k]]
            temp += [M[p][q][k+1] == M[p][q][k]]

    return And(temp)


def updateHVM(k):
    temp = []
    for p in range(dim):
        for q in range(dim):
            temp += [V[p][q][k+1] == V[p][q][k]]
            temp += [H[p][q][k+1] == H[p][q][k]]
            temp += [M[p][q][k+1] == M[p][q][k]]

    return And(temp)


for k in range (k1-1):
    temp = []
    for i in range(dim):
        for j in range(1,dim):
            temp +=   [And(H[i][j][k],
                           Not(V[i][j-1][k]),
                           Not(V[i-1][j-1][k]),
                           Not(M[i][j-1][k]),
                           Or(Not(j > 1), Not(H[i][j-2][k])),
                           Or(Not(j > 1), Not(R[i][j-2][k])),
                           H[i][j-1][k+1],
                           Not(H[i][j][k+1]),
                           updateH(k, i, j),
                           updateVRM(k),
                          )
                      ]

    for i in range(dim):
        for j in range(dim-2):  
            temp +=   [And(H[i][j][k],
                           Not(V[i][j+2][k]),
                           Not(V[i-1][j+2][k]),
                           Not(M[i][j+2][k]),
                           Not(H[i][j+2][k]),
                           Not(R[i][j+2][k]),
                           H[i][j+1][k+1],
                           Not(H[i][j][k+1]),
                           updateH(k, i, j+1),
                           updateVRM(k),
                          )
            ]
    for i in range(1,dim):
        for j in range(dim):
            temp += [And(V[i][j][k],
                         Not(H[i-1][j][k]),
                         Not(H[i-1][j-1][k]),
                         Not(M[i-1][j][k]),
                         Or(Not(i > 1), Not(V[i-2][j][k])),
                         Not(R[i-1][j][k]),
                         Not(R[i-1][j-1][k]),
                         V[i-1][j][k+1],
                         Not(V[i][j][k+1]),
                         updateV(k, i, j),
                         updateHRM(k),                     
                      )
                      ]

    for i in range(dim-2):
        for j in range(dim):
            temp += [And(V[i][j][k],
                         Not(H[i+2][j][k]),
                         Not(H[i+2][j-1][k]),
                         Not(M[i+2][j][k]),
                         Not(V[i+2][j][k]),
                         Not(R[i+2][j][k]),
                         Not(R[i+2][j-1][k]),
                         V[i+1][j][k+1],
                         Not(V[i][j][k+1]),
                         updateV(k, i+1, j),
                         updateHRM(k),                       
                        )
                    ]
                        
    for i in range(dim):
        for j in range(dim-2): 
            temp += [And(R[i][j][k],
                         Not(V[i][j+2][k]),
                         Not(V[i-1][j+2][k]),
                         Not(M[i][j+2][k]),                     
                         Not(H[i][j+2][k]),
                         R[i][j+1][k+1],
                         Not(R[i][j][k+1]),
                         updateR(k, i, j+1),
                         updateHVM(k),
                        ) 
                    ]
             
    s.add(atmost_one(temp))
    s.add(atleast_one(temp))
    
condcheck = []
for k in range(k1):
    condcheck += [R[rx][dim-2][k]]

s.add(Or(condcheck))

result = s.check()
model = s.model()

for k in range(1,k1):
    for i in range(dim):
        for j in range(dim):
            if(is_false(model[H[i][j][k-1]]) and is_true(model[H[i][j][k]])):
                if(is_false(model[H[i][j+1][k-1]])):
                    print ("H", i, j)
                else:
                    print ("H", i, j+1)
            elif(is_false(model[V[i][j][k-1]]) and is_true(model[V[i][j][k]])):
                if(is_false(model[V[i+1][j][k-1]])):
                    print ("V", i, j)
                else:
                    print ("V", i+1, j)
            elif(is_false(model[R[i][j][k-1]]) and is_true(model[R[i][j][k]])):
                if(is_false(model[R[i][j+1][k-1]])):
                    print ("R", i, j)
                else:
                    print ("R", i, j+1)


