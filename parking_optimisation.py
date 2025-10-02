
import copy
t=10
import random
import copy
random.randrange
from math import*
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial import Polynomial
import time

def regret(L,P,v,C,pref_car, coorplace):
    #inversed mappingcar->place
    car_to_place = create_inverse_mappings(C)
    
    # Get the spot of car v in O(1)
    p = car_to_place.get(v, 0)

    # Get the preferences of car v in O(1) with dict
    pref_car_dict = {u[0]: u[1] for u in pref_car}
    l = pref_car_dict.get(v, [])
    
    # Calculate the regret
    for i, place_pref in enumerate(l):
        if coorplace[place_pref] == p:
            return len(P) - i
    return 0
def regretplace(L,p,V,p0,C,pref_place):
    v=C[p0]
    l=[]
    j=0
    for e in pref_place:
        if e[0]==p:
            l=e[1]
        for i in range(len(l)):
            if l[i]==v:
                j=len(l)-i
    return j





def regretsum(L,P,V,C,pref_car, coorplace):
    a=0
    for v in V:
        a=a+regret(L,P,v,C,pref_car, coorplace)/len(V)
    return a

def regretsumplace(L,P,V,C,pref_place, coorplace):
    a=0
    for p in range(len(P)):
        a=a+regretplace(L,p,V,coorplace[p],C,pref_place)
    return a

def regrettot(L,P,P0,V,N,C,pref_car, coorplace):
    a=len(P0)*len(V)
    b=regretsum(L,P,N,C,pref_car, coorplace)
    return (a+b)

# global Cache of the distances to avoid recomputations
class DistanceCache:
    def __init__(self, L):
        self.cache = {}
        self._precompute_all_distances(L)
    
    def _precompute_all_distances(self, L):
        for i in range(len(L)):
            distances = djikstra(L, i)
            for j in range(len(L)):
                self.cache[(i,j)] = distances[j]
    
    def get_distance(self, i, j):
        return self.cache.get((i,j), float('inf'))

# global instance of the cache
distance_cache = None

def init_distance_cache(L):
    """Initialize the distance cache."""
    global distance_cache
    if distance_cache is None:
        distance_cache = DistanceCache(L)
    return distance_cache
    
def create_inverse_mappings(C):
    car_to_place = {}  # O(1) lookup
    for place, car in C.items():
        if car != 0:
            car_to_place[car] = place
    return car_to_place
def actualisation(match, time, P0):
    new_time = {k: v-10 for k, v in time.items() if v > 10}
    
    P = []
    coorplace = {}
    d = {}
    
    if not time:
        return {}, {}, P0, {i: i for i in range(len(P0))}
    
    for place in match:
        if match[place] != 0:
            idcar = match[place]
            if idcar not in new_time:  
                d[place] = 0
                coorplace[len(P)] = place
                P.append(P0[place])
            else:
                d[place] = idcar
        else:
            coorplace[len(P)] = place
            P.append(P0[place])
    
    return d, new_time, P, coorplace
import numpy as np

def regretsum_vectorized(distances, preferences):
    return np.mean(distances * preferences)



class OptimizedParking:
    def __init__(self, L):
        self.distance_cache = DistanceCache(L)
        self.car_to_place = {}
        self.place_to_car = defaultdict(int)
        
    def update_mappings(self, C):
        self.car_to_place.clear()
        self.place_to_car.clear()
        for place, car in C.items():
            if car != 0:
                self.car_to_place[car] = place
                self.place_to_car[place] = car

def complete_algo(L):
    P0=places(L)[0]
    P=copy.deepcopy(P0)
    P2=copy.deepcopy(P0)
    #continu=True
    C={}
    V=[]
    t=0
    time={}
    i=0
    l1=[]
    l3=[]
    l4=[]
    l5=[]
    C2={}
    V2=[]
    time2={}
    l12=[]
    l32=[]
    l42=[]
    ln=[]
    ln2=[]
    while i<10:
        t=t+10
        A=actualisation(C,time,P0)
        C=A[0]
        time=A[1]
        P=A[2]
        coordplace=A[3]
        A2=actualisation(C2,time2,P0)
        C2=A2[0]
        time2=A2[1]
        P2=A2[2]
        coordplace2=A2[3]
        N=cars(L,43,t)
        result=new_round(V+N,P,t,C,time,coordplace)
        resultbis=new_round_naive(V2+N,P2,t,C2,time2,coordplace2)
        C=result[1]
        V=result[2]
        time=result[3]
        pref_car=result[4]
        idchoice=result[0]
        pref_place=result[5]
        C2=resultbis[1]
        V2=resultbis[2]
        time2=resultbis[3]
        pref_car2=resultbis[4]
        idchoice2=resultbis[0]
        pref_place2=resultbis[5]
        i=i+1
        if len(P)==0:
            l1=l1+[0]
            l3=l3+[len(P0)*len(V)]
        else:
            l1=l1+[regretsum(L,P,idchoice,C,pref_car, coordplace)]#regret
            l3=l3+[regrettot(L,P,P0,V,idchoice,C,pref_car, coordplace)]
        if len(P2)==0:
            l12=l12+[0]
            l32=l32+[len(P0)*len(V)]
        else:
            l12=l12+[regretsum(L,P2,idchoice2,C2,pref_car2, coordplace2)]#regret
            l32=l32+[regrettot(L,P2,P0,V2,idchoice2,C2,pref_car2, coordplace2)]
        l42=l42+[regretsumplace(L,P2,idchoice2,C2,pref_place2, coordplace2)]
        l4=l4+[regretsumplace(L,P,idchoice,C,pref_place, coordplace)]
        ln.append(len(V))
        ln2.append(len(V2))
        print(i)
        #print (l4[len(l4)-1],l42[len(l42)-1])
    return (l1,l12,l3,l32,l4,l42,ln,ln2)

def distance(g,i,j):
    """Version optimisée utilisant le cache"""
    global distance_cache
    if distance_cache is None:
        distance_cache = DistanceCache(g)
    return distance_cache.get_distance(i, j)

def distance_places_to_go(L,P,i):
    """Version optimisée avec append()"""
    l = []
    for j in range(len(places_to_go)):
        l.append(distance_car(L,P,places_to_go,i,j))
    return l


def distance_car(L,P,V,i,j):
    lp=P[i]
    lv=V[j]#j est le num de la voit, i de la place
    pA=lp[0]
    pB=lp[2]
    vA=lv[0]
    vB=lv[2]
    if (pA,pB)!=(vA,vB) and (pA,pB)!=(vB,vA):
        dAA=distance(L,pA,vA)+lp[1]+lv[1]
        dAB=distance(L,pA,vB)+lp[1]+lv[3]
        dBA=distance(L,pB,vA)+lp[3]+lv[1]
        dBB=distance(L,pB,vB)+lp[3]+lv[3]
        l=[dAA,dBB,dBA,dAB]
        d=min(l)
    else:
        if pA==vA:
            d=abs(lp[1]-lv[1])
        elif pA==vB:
            d=abs(lp[1]-lv[3])
    return d

def djikstra(g,i):
    a_traiter ={i:0}
    distance=[0]*len(g)
    while len(a_traiter)!=0:
        (s,d)=withdraw__min(a_traiter)
        di=distance[s]
        for j in range (len(g)):
            if g[s][j]!=0:
                nd=di+g[s][j]
                if (distance[j]==0 or distance[j]>nd) and (j not in a_traiter or (a_traiter[j]>nd)):
                    a_traiter[j]=nd
                    if j!=i:
                        distance[j]=nd
    return distance
def places_to_go_factor(L,P,i):
    x=0
    l=distance_places_to_go(L,P,i)
    for e in l :
        a=1/(e+0.1)
        x+=a
    return x
def time_factor(L,V,v,t):
    if V[v][4]==1:
        return fonction1(t)
    if V[v][4]==2:
        return fonction2(t)
    if V[v][4]==3:
        return fonction3(t)
def flux(t,P):
    return(floor(fonction4(t))+len(P)+len(P0)//10)
def fonction1(t):#résidents
    if t<780:
        return 0
    if t>1080:
        return 10
    if 780<=t<=1080:
        return ((10/300)*(t-13*60))

def fonction2(t):#pendulaire
    if t<480:
        return 10
    if t>780:
        return 0
    if 480<=t<=780:
        return ((10/300)*(13*60-t))

def fonction3(t):#touriste
    if t<480 or t>1080:
        return 0
    if 480<=t<780:
        return ((10/300)*(t-8*60))
    if 780<=t<=1080:
        return ((10/300)*(18*60-t))
def fonction4(t):#touriste
    if t<480 or t>1080:
        return 1
    if 480<=t<780:
        return ((10/300)*(t-8*60))
    if 780<=t<=1080:
        return ((10/300)*(18*60-t))
def listpref(L,P,V,p,t):
    return order(pref_general(L,P,V,p,t))
def list_pref_car(L,P,V,t):
    """Version optimisée avec append()"""
    l = []
    for v in range(len(V)):
        l.append(prefcar(L,P,V,v))
    l.sort(key=lambda tup:(tup[0][0],tup[0][1]))
    return l
def listtodico(M):
    d={} #la cle est le numero de la place et la valeur est sa list de pref
    for i in range (len(M)):
        d[M[i][0]]=M[i][1]
    return d

def marriage(V0,P0,coordplace):
    C={} #la clef est la place et la valeur est la car
    V=copy.deepcopy(V0)
    P=copy.deepcopy(P0)
    P1=listtodico(P)
    V1=listtodico(V)
    man_not_married_yet=[V0[i][0] for i in range(len(V0))]
    while man_not_married_yet!=[]:
        trouve=False
        while trouve==False:
            voit=man_not_married_yet.pop()
            one=V1[voit].pop()
            placepref=coordplace[one]
            if placepref not in C:
                C[placepref]=voit
                trouve=True
            else:
                actuel=C[placepref]
                i=0
                while i<len(P):
                    if P1[one][i]==actuel:
                        man_not_married_yet.append(actuel)
                        C[placepref]=voit
                        trouve=True
                        i=len(P)+1 
                    elif P1[one][i]==voit:
                         man_not_married_yet.append(voit)
                         i=len(P)+1
                    i+=1
    return C

def min(l):
    a=l[0]
    for e in l :
        if e <a:
            a=e
    return a
def less_polluting(V,n,prvoit): #c is a list of tuples id and dicos (supporiginals); n is the number of cars we can add
    J=[]
    for i in range(len(V)):
        J.append((V[i][5],V[i],prvoit[i][1])) #on ordonne les borderline en critère de pollution croissant crit'air, id, time
    J.sort()
    wait_list=[J.pop()[1] for k in range(len(V)-n)]
    choicesupp=[(J[i][1][7],J[i][2],J[i][1][6]) for i in range(len(J))]
    return(choicesupp, wait_list)

def newpref_places(choice,prplaces):
    T=[choice[i][0] for i in range(len(choice))]
    newpref=[]
    for i in range(len(prplaces)):
        M=[]
        for j in range(len(prplaces[i][1])):
            if prplaces[i][1][j] in T:
                M.append(prplaces[i][1][j])
        newpref=newpref+[(prplaces[i][0],M)]
    return newpref

def new_round(V,P,t,C,time,coordplace): #nouvelle list de lists de cars et de places
    timeprov={}
    te=copy.deepcopy(time)
    for e in V:
        timeprov[e[7]]=e[6]
    #print(len(P))
    if len(P)==0:
        return ([], C,V,te,[],[])
    pref_car=list_pref_car(L,P,V,t)
    pref_places=prefplaces(L,P,V,t)
    choiceprov=[]
    n=len(P)
    tr=pref_car[0][0][0] #rang min de slice
    H=slice(pref_car,tr)
    wait_list=[]
    while pref_car!=[] and n-len(H)>=0:
        choiceprov=choiceprov+H
        pref_car=pref_car[len(H):]
        V=V[len(H):]
        n=n-len(H)
        tr+=1
        H=slice(pref_car,tr)
    if len(choiceprov)<len(P) and pref_car!=[]:
        supp=slice(pref_car,tr)
        voitsupp=[V[i] for i in range(len(supp))]
        V=V[len(supp):]
        ajout=less_polluting(voitsupp,n,supp)[0]
        choice=choiceprov+ajout
        wait_list=less_polluting(voitsupp,n,supp)[1]
        wait_list=wait_list[:]+V[:]
    else:
        choice=choiceprov
        wait_list=V[:]
    idchoice=[choice[i][0] for i in range(len(choice))]
    newprefplaces=newpref_places(choice,pref_places)
    perf=perfectmarriage(newprefplaces,choice, C, coordplace)
    C=perf[1]
    for car in idchoice:
        te[car]=timeprov[car]
    V.sort(key=lambda tup:(tup[7]))
    return (idchoice, C, wait_list,te,choice, pref_places)



def new_round_naive(V,P,t,C,time,coordplace):
    if len(P)==0:
        return([], C, V, time,[],[])
    pref_car=list_pref_car(L,P,V,t)
    pref_place=prefplaces(L,P,V,t)
    idchoice=[]
    choice=[]
    Vlibre=V[:]
    voitdist={}
    timeprov={}
    te=copy.deepcopy(time)
    for e in V:
        timeprov[e[7]]=e[6]
    for j in range (len(P)):
        dists=[]
        for v in Vlibre:
            i=Vlibre.index(v)
            e=distance_car(L,P,Vlibre,j,i)
            voitdist[e]=v
            dists.append(e)
        distmin=min(dists)
        voitpref=voitdist[distmin]
        Vlibre.pop(Vlibre.index(voitpref))
        C[coordplace[j]]=voitpref[7]
        choice.append(voitpref)
        idchoice.append(voitpref[7])
    for idcar in idchoice:
        te[idcar]=timeprov[idcar]
    return(idchoice, C, Vlibre, te, pref_car, pref_place)


def occurences(L):
    l=len(L[0])
    a=L[0][l-1]
    k=0
    for A in L:
        if A[l-1]==a:
            k+=1
    return k
def order(l):
    a=[]
    L=copy.deepcopy(l)
    while len(L)!=0:
        a=[withdraw_max(L)[1]]+a
    return a

def perfectmarriage(pref_places,choice,C, coordplace): #lists
    p=len(pref_places)
    D=marriage(choice,pref_places,coordplace)
    for i in range(len(C)):
        if i not in D:
            D[i]=C[i]
    return (choice, D)
def places(L): #43 places
    l=[]
    n=0
    for i in range (len(L)):
        for j in range (len(L)):
            if L[i][j]!=0 and i<j:
                a=L[i][j]
                b=int(a/0.5)
                for k in range (1,b-1):
                    l=l+[[i,k*0.5,j,a-(k*0.5)]]
                    n=n+1
    return l, n

def pref_general(L,P,V,p,t):
    l=[]
    for v in range(len(V)):
        pref=prefpollution(L,P,V,p,v)+preftype(L,P,V,p,v,t)
        prefbis=1/(prefpollution(L,P,V,p,v)+1)
        rang=V[v][7]
        l=l+[[pref,rang]]
    return l

def prefplaces(L,P,V,t):
    l=[]
    for p in range(len(P)):
        l=l+[(p,listpref(L,P,V,p,t))]
    return l

def prefpollution(L,P,V,p,v):
    a=V[v][5]+0.5
    c=distance_car(L,P,V,p,v)
    return a*c #pour le moment juste "crit'air" x distance, loi sur laquelle on peut jouer

def preftype(L,P,V,p,v,t):
    a=V[v][4]
    c=places_to_go_factor(L,P,p)
    d=time_factor(L,V,v,t)
    return a*c*d

def prefcar(L,P,V,v):
    tour1=V[v][7]
    a=random.randrange(len(P))
    l=[]
    for p in range(len(P)):
        l=l+[[distance_car(L,P,P,a,p),p]]
    lbis=order(l)
    return (tour1,lbis,V[v][6])
def withdraw_min(l):
    m=100
    k=0
    for i in range(len(l)):
        if l[i][0]<m:
            m=l[i][0]
            k=i
    p=l.pop(k)
    return p

def withdraw__min(d):
    m=100
    k=0
    for e in d :
        if d[e]<m:
            m=d[e]
            k=e
    p=d.pop(k)
    return (k,p)




def slice(pref_car,tr):
    j=0
    H=[]
    while j<len(pref_car) and pref_car[j][0][0]==tr:
        H.append(pref_car[j])
        j=j+1
    return H



def neighbor(L,a):
    """Version optimisée avec append()"""
    l = []
    for i in range(len(L)):
        if L[i][a] != 0:
            l.append(i)
    return l




def cars(L,n,t):
    """Version optimisée avec append()"""
    l = []
    tour = round(t/10)
    for i in range(n):
        t_voit = []
        a = random.randrange(19)
        b = random.choice(neighbor(L,a))
        d = L[a][b]
        dA = round(random.uniform(0,d),1)
        dB = round(d-dA,2)
        g = random.randrange(1,4)#type entre 1 et 3 (touriste/résident...)
        h = random.randrange(6)#crit'air(entre 0 et 5)
        if g==1:#résident
            e = random.randrange(30,50,10)
        if g==2:#pendulaire
            e = random.randrange(30,50,10)
        if g==3:#touriste
            e = random.randrange(10,30,10)
        t_voit = [a,dA,b,dB,g,h,e,(tour,i)]
        l.append(t_voit)
    return l
L=[[0, 4, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [4, 0, 1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 2.5, 0, 1.5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 2.5, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 2, 0, 0, 0, 1, 0, 0, 0, 0.5, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1.5, 0, 1, 0, 2, 0, 0, 0, 0.5, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 2, 0, 3, 0, 0, 0, 0.5, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0], [2, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 2, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0.5, 0, 0, 0, 3, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0.5, 0, 0, 0, 1, 0, 2, 0, 0, 0, 2, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0.5, 0, 0, 0, 2, 0, 0.5, 0, 0, 0, 2, 0, 0], [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0.5, 0, 0, 0, 0, 0, 2, 2], [0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2.5, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2.5, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1, 0, 0.5, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0.5, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 1, 0]]
places_to_go = [[3,0.5,6,0.5,3],[6,1.5,7,1.5,2],[12,1,18,1,1],[13,2,14,1.5,3],[0,1,8,1,5]] #théatre:3,place:2,poste:1,chateau:3,leclerc:5
Pa=[(1,[(3,5),(3,4),(4,0),(4,1)]),(3,[(4,1),(3,4),(4,0),(3,5)]),(5,[(3,4),(4,1),(4,0),(3,5)])] #pref des places
Va=[((3,5),[1,3,5],20),((3,4),[3,5,1],30)] #pref des voit
Supp=[((4,0),[3,1,5],40),((4,1),[1,3,5],10)]
newsupp=[((4,0),[3,1,5])]
choicex=[((3,5),[1,3,5]),((3,4),[3,5,1]),((4,1),[1,3,5])]
Supporiginals=[((4,0),{"pollution":13,"localisation":(3,4), "type":"touristo"},[3,1,5]),((4,1),{"pollution":5,"localisation":(9,4), type:"touristo"},[1,3,5])]
def empty_dico(n): #dico vide des places de 0 a n-1 inclu
    D={}
    for i in range(n):
        D[i]=(0,0)
    return D
C=empty_dico(9)

def withdraw_max(l):#il faut remplacer la fonction qui s'appelle withdraw_min par celle-là (je crois même qu'il y en a 2 qui s'appellent withdraw_min lol enlève les 2)
    m=-inf
    k=0
    for i in range(len(l)):
        if l[i][0]>m:
            m=l[i][0]
            k=i
    p=l.pop(k)
    return p


def benchmark_performance():
    #mesure performance
    print("preformance benchmarking")
    
    # Initialiser le cache de distances
    init_distance_cache(L)
    
    # Test 1: Mesurer le time de calcul de distances
    start_time = time.time()
    for i in range(10):
        for j in range(10):
            distance(L, i, j)
    cache_time = time.time() - start_time
    print(f" time with cache: {cache_time:.4f}s")
    
    # Test 2: Mesurer l'algo complet
    start_time = time.time()
    result = complete_algo(L)
    total_time = time.time() - start_time
    print(f" time complete algorithm : {total_time:.4f}s")
    
    return result, cache_time, total_time


    
def tipe():
    result, cache_time, total_time = benchmark_performance()
    t = [10*i for i in range(10)]
    l = result
    
    # Graphique 1: Regret simple
    plt.figure(figsize=(10, 6))
    y1 = l[0]
    plt.plot(t, y1, marker='.', color='red', label='Optimised')
    y12 = l[1]
    plt.plot(t, y12, marker='.', color='blue', label='Naive')
    plt.title('Regret over time')
    plt.xlabel('time (minutes)')
    plt.ylabel('Regret')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()
    
    # Graphique 2: Courbes de tendance du regret
    plt.figure(figsize=(10, 6))
    p1 = Polynomial.fit(t, y1, 3)
    yr1 = [p1(e) for e in t]
    p12 = Polynomial.fit(t, y12, 3)
    yr12 = [p12(e) for e in t]
    plt.plot(t, yr1, color='red', label='optimised tendency')
    plt.plot(t, yr12, color='blue', label='naive tendency')
    plt.title('regret tendency')
    plt.xlabel('time (minutes)')
    plt.ylabel('Regret (tendency)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()
    
    # Graphique 3: Regret total
    plt.figure(figsize=(10, 6))
    y3 = l[2]
    plt.plot(t, y3, marker='.', color='red', label='Optimised')
    y32 = l[3]
    plt.plot(t, y32, marker='.', color='blue', label='Naive')
    plt.title('Total regret over time')
    plt.xlabel('time (minutes)')
    plt.ylabel('Total regret')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()
    
    print(f" Optimised performance: {total_time:.4f}s")
    return None
if 'L' in globals():
    init_distance_cache(L)
    print(" distance cache initialized.")


tipe()  