list=['(a,b)','(c,d)','(e,f)']
x=len(list)
#pengennya ambil list[0],[-1] dan list[1],[-2] make x=2
k=0
while k<x:
    print()
    y=list[x-k]
    k=k+1
print(x-k)
query="insert into v values" + "%s;"%list[x-k]
print(query)
