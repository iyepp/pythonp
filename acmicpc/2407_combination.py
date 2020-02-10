

def calNumerator(n1, n2):
    temp = 1
    for x in range(0,n2,1):
        x = n1-x
        temp = temp*x 
    return temp

def calDenominator(n2):
    temp =1
    for x in range(n2, 1, -1):
        temp = temp*x
    return temp

nu, de  =map( int, input("").split() )

numernator = calNumerator(nu, de )

denominator = calDenominator( de )

print( numernator//denominator )

"""
n, m = map(int, input().split())
answer = 1
k = n - m

while n > k:
    answer *= n
    n -= 1
while m > 1:
    answer = answer // m
    m -= 1

print(answer)
"""
