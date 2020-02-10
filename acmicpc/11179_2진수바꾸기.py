
mystr=""
mylist=[]
res = 0
def revdevbi(n):
    if n==0 :
        return
    m=int(n/2)
    
    revdevbi(m)
    
    #mystr.append(str(n%2))
    mylist.append(n%2)

def revbidev(mlist):
    base = 0
    for x in range(len(mlist)):
        base = base + mlist.pop() * pow(2,x)
    
    # final result
    print(base)

num = int(input(""))

revdevbi(num)
#print(mylist)

mylist.reverse()
#print(mylist)

revbidev(mylist)


