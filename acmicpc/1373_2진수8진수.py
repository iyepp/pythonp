
l1 = []
l2 = []
l1 =  input()

l1 =list(l1)
length = len(l1)

if length %3 != 0:
    while length % 3 != 0:
        l1.insert(0, 0)
        length = len(l1)

for x in range(0, length, 3):
    a = int( l1[x] )
    b = int( l1[x+1] )
    c = int( l1[x+2] )
    l2.append(a*4+b*2+c)
    
for x in range(len(l2)):
    l2[x] = str(l2[x])

l2 = "".join(l2)
print( l2 )   
