
class CQueue:
    r = 0
    f = 0
    size = 0
    def __init__(self):
        self._list = []

    def empty(self):
        return True if len(self._list) == 0 else False

    def deQ(self):
        if len(self._list) == 0 :
            return 0
        else:
            return self._list.pop(-1)
    def enQ(self, value):
            return self._list.insert(0,value)

    def peekQ(self):
        if len(self._list) != 0:
            return self._list[-1]
        else :
            return 0
    
    def lenQ(self):
        return len(self._list)
        

q = CQueue()

q.enQ(1)
print( q.deQ() )

q.enQ(2)
q.enQ(3)
print( q.lenQ() )
print( q.peekQ() )
print( q.deQ() )
print( q.deQ() )

print("==========")
print( q.deQ() )
print( q.peekQ() )



