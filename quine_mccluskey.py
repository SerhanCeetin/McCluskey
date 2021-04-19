import string
from difflib import ndiff

class Minterm():
    def __init__(self, dec_str):
        self.dec=int(dec_str)
        self.binary=format(self.dec, "b")

    def binary_format(self, size):
        self.binary = (size-len(self.binary))*"0"+self.binary

    def __lt__(self, other):
        return self.dec < other
    def __le__(self, other):
        return self.dec <= other
    def __gt__(self, other):
        return self.dec > other
    def __ge__(self, other):
        return self.dec >= other
    def __ne__(self, other):
        return self.dec != other
    def __eq__(self, other):
        return self.dec == other
    def __str__(self):
        return "m"+str(self.dec)

    def comp(self, other):
        count = 0
        pos = 0

        res=list(self.binary)
        for i in range(len(self.binary)):
            if self.binary[i] != other.binary[i]:
                count += 1
                pos = i
        if count == 1:
            res[pos]="-"
            return "".join(res)
        else:
            return False

    def __repr__(self):
        return str(self.binary)

    # def __hash__(self):
    #     return id(self)



class Implicant():
    def __init__(self, minterms:tuple, implicant:str, implicants=None):
        self.minterms=minterms
        self.implicant=implicant
        self.implicants=implicants
        self.isused=False

    def __str__(self):
        return f"m({','.join([str(m.dec) for m in self.minterms])})"

    def __repr__(self):
        used="*"
        if(self.isused):
            used=""
        return self.implicant+used

    def comp(self, other):
        count = 0
        pos = 0

        res=list(self.implicant)
        for i in range(len(self.implicant)):
            if self.implicant[i] != other.implicant[i]:
                count += 1
                pos = i
        if count == 1:
            res[pos]="-"
            return "".join(res)
        else:
            return False

    def __eq__(self, other):
        return other.implicant==self.implicant
    def __ne__(self, other):
        return other.implicant!=self.implicant
    #
    # def __hash__(self):
    #     return id(self)

u_input=['4', '8', '9', '10', "12", "11", "14", "15"]
minterms = list(map(Minterm, u_input))

l=len(max(minterms).binary)

col1=dict()
for m in minterms:
    m.binary_format(l)
    col1.setdefault(m.binary.count("1"), []).append(m)


col2=dict()
for g in col1.keys():
    if(g+1 in col1.keys()):
        for m1 in col1[g]:
            for m2 in col1[g+1]:
                res=m1.comp(m2)
                if(res!=False):
                    col2.setdefault(res.count("1"), []).append(Implicant(minterms=tuple([m1,m2]), implicant=res))

col3=dict()
for g in col2.keys():
    if(g+1 in col2.keys()):
        for i1 in col2[g]:
            for i2 in col2[g+1]:
                res=i1.comp(i2)
                if(res!=False):
                    i1.isused=True
                    i2.isused=True
                    col3.setdefault(res.count("1"), []).append(Implicant(minterms=tuple(list(i1.minterms)+list(i2.minterms)), implicant=res, implicants=tuple([i1,i2])))

for k,v in col3.items():
    res=[]
    for i in v:
        if(i not in res):
            res.append(i)
    col3[k]=res
print(col1)
print(col2)
print(col3)
