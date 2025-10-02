from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import copy
import random
import json
from math import *
from collections import defaultdict
import numpy as np
import time

app = Flask(__name__)
CORS(app)

# -------------------------------
# Code d'optimisation de parking adapté
# -------------------------------

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

# Cache global des distances
distance_cache = None

def init_distance_cache(L):
    global distance_cache
    if distance_cache is None:
        distance_cache = DistanceCache(L)
    return distance_cache

def create_inverse_mappings(C):
    car_to_place = {}
    for place, car in C.items():
        if car != 0:
            car_to_place[car] = place
    return car_to_place

def regret(L,P,v,C,pref_car, coorplace):
    car_to_place = create_inverse_mappings(C)
    p = car_to_place.get(v, 0)
    pref_car_dict = {u[0]: u[1] for u in pref_car}
    l = pref_car_dict.get(v, [])
    
    for i, place_pref in enumerate(l):
        if coorplace[place_pref] == p:
            return len(P) - i
    return 0

def regretsum(L,P,V,C,pref_car, coorplace):
    if len(V) == 0:
        return 0
    a = 0
    for v in V:
        a = a + regret(L,P,v,C,pref_car, coorplace)/len(V)
    return a

def regrettot(L,P,P0,V,N,C,pref_car, coorplace):
    a = len(P0)*len(V) if V else 0
    b = regretsum(L,P,N,C,pref_car, coorplace)
    return (a+b)

def distance(g,i,j):
    global distance_cache
    if distance_cache is None:
        distance_cache = DistanceCache(g)
    return distance_cache.get_distance(i, j)

def djikstra(g,i):
    a_traiter = {i:0}
    distance_arr = [0]*len(g)
    while len(a_traiter) != 0:
        (s,d) = withdraw__min(a_traiter)
        di = distance_arr[s]
        for j in range(len(g)):
            if g[s][j] != 0:
                nd = di + g[s][j]
                if (distance_arr[j] == 0 or distance_arr[j] > nd) and (j not in a_traiter or (a_traiter[j] > nd)):
                    a_traiter[j] = nd
                    if j != i:
                        distance_arr[j] = nd
    return distance_arr

def withdraw__min(d):
    m = float('inf')
    k = None
    for e in d:
        if d[e] < m:
            m = d[e]
            k = e
    if k is not None:
        p = d.pop(k)
        return (k,p)
    return (None, None)

def distance_car(L,P,V,i,j):
    if i >= len(P) or j >= len(V):
        return float('inf')
    
    lp = P[i]
    lv = V[j]
    pA = lp[0]
    pB = lp[2]
    vA = lv[0]
    vB = lv[2]
    
    if (pA,pB) != (vA,vB) and (pA,pB) != (vB,vA):
        dAA = distance(L,pA,vA) + lp[1] + lv[1]
        dAB = distance(L,pA,vB) + lp[1] + lv[3]
        dBA = distance(L,pB,vA) + lp[3] + lv[1]
        dBB = distance(L,pB,vB) + lp[3] + lv[3]
        l = [dAA,dBB,dBA,dAB]
        d = min(l)
    else:
        if pA == vA:
            d = abs(lp[1] - lv[1])
        elif pA == vB:
            d = abs(lp[1] - lv[3])
        else:
            d = 0
    return d

def places(L):
    l = []
    n = 0
    for i in range(len(L)):
        for j in range(len(L)):
            if L[i][j] != 0 and i < j:
                a = L[i][j]
                b = int(a/0.5)
                for k in range(1, b-1):
                    l = l + [[i, k*0.5, j, a-(k*0.5)]]
                    n = n + 1
    return l, n

def neighbor(L,a):
    l = []
    for i in range(len(L)):
        if L[i][a] != 0:
            l.append(i)
    return l

def cars(L,n,t):
    l = []
    tour = round(t/10)
    for i in range(n):
        a = random.randrange(19)
        neighbors = neighbor(L,a)
        if not neighbors:
            continue
        b = random.choice(neighbors)
        d = L[a][b]
        dA = round(random.uniform(0,d),1)
        dB = round(d-dA,2)
        g = random.randrange(1,4)
        h = random.randrange(6)
        if g == 1:
            e = random.randrange(30,50,10)
        elif g == 2:
            e = random.randrange(30,50,10)
        else:
            e = random.randrange(10,30,10)
        t_voit = [a,dA,b,dB,g,h,e,(tour,i)]
        l.append(t_voit)
    return l

def actualisation(match, time_dict, P0):
    new_time = {k: v-10 for k, v in time_dict.items() if v > 10}
    
    P = []
    coorplace = {}
    d = {}
    
    if not time_dict:
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

def new_round_naive(V,P,t,C,time_dict,coordplace):
    if len(P) == 0:
        return([], C, V, time_dict, [], [])
    
    idchoice = []
    choice = []
    Vlibre = V[:]
    voitdist = {}
    timeprov = {}
    te = copy.deepcopy(time_dict)
    
    for e in V:
        timeprov[e[7]] = e[6]
    
    for j in range(len(P)):
        if not Vlibre:
            break
        dists = []
        for v in Vlibre:
            i = Vlibre.index(v)
            e = distance_car(L,P,Vlibre,j,i)
            voitdist[e] = v
            dists.append(e)
        
        if dists:
            distmin = min(dists)
            voitpref = voitdist[distmin]
            Vlibre.remove(voitpref)
            C[coordplace[j]] = voitpref[7]
            choice.append(voitpref)
            idchoice.append(voitpref[7])
    
    for idcar in idchoice:
        te[idcar] = timeprov[idcar]
    
    return(idchoice, C, Vlibre, te, [], [])

def simple_algo(L, iterations=10):
    """Version simplifiée de l'algorithme pour l'interface web"""
    P0 = places(L)[0]
    P = copy.deepcopy(P0)
    C = {}
    V = []
    t = 0
    time_dict = {}
    
    results = {
        'times': [],
        'regret_naive': [],
        'cars_count': [],
        'performance_time': 0
    }
    
    start_time = time.time()
    
    for i in range(iterations):
        t = t + 10
        A = actualisation(C, time_dict, P0)
        C = A[0]
        time_dict = A[1]
        P = A[2]
        coordplace = A[3]
        
        N = cars(L, 20, t)  # Réduire le nombre de voitures pour la démo
        result = new_round_naive(V + N, P, t, C, time_dict, coordplace)
        
        C = result[1]
        V = result[2]
        time_dict = result[3]
        idchoice = result[0]
        
        results['times'].append(t)
        results['cars_count'].append(len(V))
        
        if len(P) == 0:
            results['regret_naive'].append(0)
        else:
            # Calcul simplifié du regret
            regret_val = len(V) * 0.1 if V else 0
            results['regret_naive'].append(regret_val)
    
    results['performance_time'] = time.time() - start_time
    return results

# Graphe de la ville (matrice d'adjacence)
L = [[0, 4, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
     [4, 0, 1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
     [0, 1, 0, 2.5, 0, 1.5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
     [0, 0, 2.5, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
     [0, 2, 0, 0, 0, 1, 0, 0, 0, 0.5, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
     [0, 0, 1.5, 0, 1, 0, 2, 0, 0, 0, 0.5, 0, 0, 0, 0, 0, 0, 0, 0], 
     [0, 0, 0, 1, 0, 2, 0, 3, 0, 0, 0, 0.5, 0, 0, 0, 0, 0, 0, 0], 
     [0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0], 
     [2, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 2, 0, 0, 0, 0, 0], 
     [0, 0, 0, 0, 0.5, 0, 0, 0, 3, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0], 
     [0, 0, 0, 0, 0, 0.5, 0, 0, 0, 1, 0, 2, 0, 0, 0, 2, 0, 0, 0], 
     [0, 0, 0, 0, 0, 0, 0.5, 0, 0, 0, 2, 0, 0.5, 0, 0, 0, 2, 0, 0], 
     [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0.5, 0, 0, 0, 0, 0, 2, 2], 
     [0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2.5, 0, 0, 0, 0], 
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2.5, 0, 1, 0, 0, 0], 
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1, 0, 1, 0, 0], 
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1, 0, 0.5, 0], 
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0.5, 0, 1], 
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 1, 0]]

# Initialiser le cache
init_distance_cache(L)

# -------------------------------
# Routes Flask
# -------------------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/run_simulation', methods=['POST'])
def run_simulation():
    try:
        data = request.get_json()
        iterations = data.get('iterations', 10)
        iterations = min(max(iterations, 1), 20)  # Limiter entre 1 et 20
        
        results = simple_algo(L, iterations)
        
        return jsonify({
            'success': True,
            'data': results
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/graph_info')
def graph_info():
    """Retourne des informations sur le graphe de la ville"""
    nodes = len(L)
    edges = sum(1 for i in range(nodes) for j in range(nodes) if L[i][j] > 0) // 2
    places_info = places(L)
    
    return jsonify({
        'nodes': nodes,
        'edges': edges,
        'parking_spots': places_info[1],
        'total_places': len(places_info[0])
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
