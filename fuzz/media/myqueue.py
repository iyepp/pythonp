
class CQueue:
    _r = 0
    _f = 0
    _size = 0
    def __init__(self, size):
        self._list= ['']*(size+1)
        self._size = size+1
        self._r = 0
        self._f = 0

    def empty(self):
        #return True if len(self._list) == 0 else False
        return True if self._r == self._f else False

    def deQ(self):
        #if len(self._list) == 0 :
        if self._r == self._f :
            print(f"deQ {self._f} : {self._r} ERROR -1\t", end="")
            return -1
        else:
            print(f"deQ {self._f} : {self._r} \t", end="")
            #ret = self._list.remove(self._f)
            #ret = self._list.pop(self._f)
            ret = self._list[self._f]
            print( ">>" , ret )
            self._f = (self._f+1)%self._size
            return ret

    def enQ(self, value):
        if (self._r+1)%self._size == self._f:
            print(f"enQ {self._f} : {self._r} Error -1 \t", end="")
            return -1
        else:
            #rear를 증가해서 뒤에 넣는다
            print(f"enQ {self._f} : {self._r} \t", end="")
            self._list[self._r] = value
            self._r = (self._r + 1) % self._size
            return value

    def peekQ(self):
        print(f"peek {self._f} : {self._r} \t", end="")
        print( self._list[self._f] )
        return self._list[self._f]
    
    def checkfr(self):
        print(f"\t\t{self._f} : {self._r} \t", end="")

q = CQueue(10000)

q.checkfr()
print( q.enQ(1) ) 
q.checkfr()
print( q.enQ(2) )
q.checkfr()
print( q.enQ(3) )
q.checkfr()
print( q.enQ(4) )


print( q.peekQ() )
q.checkfr()
print( q.deQ() )
q.checkfr()
print( q.deQ() )
q.checkfr()
print( q.deQ() )
q.checkfr()
print( q.deQ() )
q.checkfr()

print("==========")

print( q.enQ(5) )
q.checkfr()
print( q.enQ(6) )
q.checkfr()
print( q.enQ(7) )
q.checkfr()
print( q.enQ(8) )
q.checkfr()

print( q.peekQ() )
q.checkfr()

ret = q.deQ()
print(":::", ret)
print( q.deQ() )
print( q.deQ() )
print( q.deQ() )
print( q.deQ() )

