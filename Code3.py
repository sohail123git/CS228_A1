from z3 import *
import sys
import array as arr
from itertools import combinations
import time
inputtext = []
lines = -1
with open(sys.argv[1]) as f:
    contents = f.read()
    for entry in contents.split('\n'):
        lines += 1
        inputtext.append(entry.split(','))


s = Solver()
k1 = int(inputtext[0][1])
k1 = k1+1
dim = int(inputtext[0][0])

rx = int(inputtext[1][0])
ry = int(inputtext[1][1])

o = []
x = []
y = []

h = []
v = []

for i in range(dim):
    h.append(False)
    v.append(False)


for i in range(2, lines):
    o.append(int(inputtext[i][0]))
    x.append(int(inputtext[i][1]))
    y.append(int(inputtext[i][2]))

cars = lines-2 #cars+mines-redcar


H = [ [ [ Bool("h_%s_%s_%s" % (i, j, k)) for k in range(k1) ] for j in range(dim) ] for i in range(dim) ]
V = [ [ [ Bool("v_%s_%s_%s" % (i, j, k)) for k in range(k1) ] for j in range(dim) ] for i in range(dim) ]
M = [ [ Bool("m_%s_%s" % (i, j)) for j in range(dim) ] for i in range(dim) ]

for i in range(dim):
    for j in range(dim):
        H[i][j][0] = False
        V[i][j][0] = False
        M[i][j] = False

H[rx][ry][0] = True
h[rx] = True

for w in range(cars):
    if(o[w] == 0): 
        V[x[w]][y[w]][0] = True 
        v[y[w]] = True
    elif(o[w] == 1): 
        H[x[w]][y[w]][0] = True   
        h[x[w]] = True
    else: 
        M[x[w]][y[w]] = True

valfinal = []

for k in range(k1-1):
    temp = []
    for p in range(dim*dim):
        i = int(p/dim)
        j = p%dim
        temp += [H[i][j][k+1] == H[i][j][k]]
        temp += [V[i][j][k+1] == V[i][j][k]]     
    valfinal.append(temp)

def updateH(k, i, j):
    valfinal[k][2*dim*i + 2*j] = True
    valfinal[k][2*dim*i + 2*(j-1)] = True
    return And(valfinal[k])

def updateV(k, i, j):
    valfinal[k][2*dim*i + 2*j + 1] = True
    valfinal[k][2*dim*(i-1) + 2*j + 1] = True
    return And(valfinal[k])


for k in range (k1-1):
    temp = []
    for i in range(dim):
        for j in range(dim):
            if (j > 0) and h[i] and (j<(dim-1)) and not(M[i][j-1]) and not(M[i][j]) and not(M[i][j+1]):
                    temp +=   [And(H[i][j][k],
                                    Not(V[i][j-1][k]),
                                    Not(V[i-1][j-1][k]),
                                    Or(Not(j > 1), Not(H[i][j-2][k])),
                                    H[i][j-1][k+1],
                                    Not(H[i][j][k+1]),
                                    updateH(k, i, j)
                                    )
                                ]          
                    valfinal[k][2*dim*i + 2*j] = H[i][j][k+1] == H[i][j][k]
                    valfinal[k][2*dim*i + 2*(j-1)] = H[i][j-1][k+1] == H[i][j-1][k]
                    

            if (j < (dim-2)) and h[i] and not(M[i][j]) and not(M[i][j+1]) and not(M[i][j+2]):
                    temp +=   [And(H[i][j][k],
                                Not(V[i][j+2][k]),
                                Not(V[i-1][j+2][k]),
                                Not(H[i][j+2][k]),
                                H[i][j+1][k+1],
                                Not(H[i][j][k+1]),
                                updateH(k, i, j+1),
                                )
                            ]    
                    valfinal[k][2*dim*i + 2*j] = H[i][j][k+1] == H[i][j][k]
                    valfinal[k][2*dim*i + 2*(j+1)] = H[i][j+1][k+1] == H[i][j+1][k]

            if (i>0) and v[j] and (i<(dim-1)) and not(M[i-1][j]) and not(M[i][j]) and not(M[i+1][j]):
                    temp += [And(V[i][j][k],
                                Not(H[i-1][j][k]),
                                Not(H[i-1][j-1][k]),
                                Or(Not(i > 1), Not(V[i-2][j][k])),
                                V[i-1][j][k+1],
                                Not(V[i][j][k+1]),
                                updateV(k, i, j),                
                            )
                            ]
                    valfinal[k][2*dim*(i-1) + 2*j + 1] = V[i-1][j][k+1] == V[i-1][j][k]
                    valfinal[k][2*dim*i + 2*j + 1] = V[i][j][k+1] == V[i][j][k]

            if (i < (dim-2)) and v[j] and not(M[i][j]) and not(M[i+1][j]) and not(M[i+2][j]):
                    temp += [And(V[i][j][k],
                                Not(H[i+2][j][k]),
                                Not(H[i+2][j-1][k]),
                                Not(V[i+2][j][k]),
                                V[i+1][j][k+1],
                                Not(V[i][j][k+1]),
                                updateV(k, i+1, j),                     
                                )
                            ]           
                    valfinal[k][2*dim*(i+1) + 2*j + 1] = V[i+1][j][k+1] == V[i+1][j][k]
                    valfinal[k][2*dim*i + 2*j + 1] = V[i][j][k+1] == V[i][j][k]
                
    s.add(Or(temp))
    
condcheck = []
for k in range(k1):
    condcheck += [H[rx][dim-2][k]]

s.add(Or(condcheck))

result = s.check()

model = s.model()

for i in range(dim):
        for j in range(dim):
            if((H[i][j][0] == False) and is_true(model[H[i][j][1]])):
                if(H[i][j+1][0] == False):
                    print(i,",",j, sep="")
                else:
                    print(i,",",j+1, sep="")
            elif((V[i][j][0] == False) and is_true(model[V[i][j][1]])):
                if(V[i+1][j][0] == False):
                    print(i,",",j, sep="")
                else:
                    print(i+1,",",j, sep="")


for k in range(2,k1):
    for i in range(dim):
        for j in range(dim):
            if(is_false(model[H[i][j][k-1]]) and is_true(model[H[i][j][k]])):
                if(is_false(model[H[i][j+1][k-1]])):
                    print(i,",",j, sep="")
                else:
                    print(i,",",j+1, sep="")
            elif(is_false(model[V[i][j][k-1]]) and is_true(model[V[i][j][k]])):
                if(is_false(model[V[i+1][j][k-1]])):
                    print(i,",",j, sep="")
                else:
                    print(i+1,",",j, sep="")
