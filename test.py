# -*- coding: utf-8 -*-

import random
import time

from WG import *

grading_mode = False

def error(msg):
    print(msg)
    assert not grading_mode, msg
    return False

L_tutorial=[['A','B',2],['B','C',1],['C','D',1],['D','E',2],['E','F',1],['F','G',2],['G','H',1],['H','A',1],['A','F',1],['B','E',1],['D','G',1],['C','H',5]]

def check_cycle(wg, cyc, prefix=None, weight=None): # check a cycle is valid, if w is not None, compare weight
    if cyc is None or len(cyc) != len(wg.adj)+1:
        return error("path {} does not have the expected number of vertices".format(cyc))
    if cyc[0] != cyc[-1]:
        return error("path {} is not a cycle".format(cyc))
    w = 0
    for i in range(len(cyc)-1):
        if cyc[i+1] not in wg.adj[cyc[i]]:
            return error("path {} is invalid: edge {}-{} does not exist".format(cyc. cyc[i], cyc[i+1]))
        w += wg.adj[cyc[i]][cyc[i+1]]
    if prefix is not None and cyc[0:len(prefix)] != prefix:
        return error("path {} is valid but but does not start with prefix {}".format(cyc, prefix))
    if weight is not None and w != weight:
        return error("path {} is valid but not optimal: is has weight {} but expected {}".format(cyc, w, weight))
    return True

def test1():
    print("testing min_cycle_aux")
    global L_tutorial
    wg=WG(L_tutorial)
    print("Tests on the graph of Figure 1")
    print()

    for prefix, wopt, solution in [(['A','F','G'], 14, ['A', 'F', 'G', 'D', 'E', 'B', 'C', 'H', 'A']),
                                   (['H','C'], 14, ['H', 'C', 'D', 'G', 'F', 'E', 'B', 'A', 'H']),
                                   (['G'], 8, ['G', 'H', 'A', 'F', 'E', 'B', 'C', 'D', 'G']),
                                   (['A','B','C','D','E','F','G','H'], 11, ['A','B','C','D','E','F','G','H','A'])]:
        print("Test with input L=", prefix)
        res=wg.min_cycle_aux(0,prefix.copy(),set(['A','B','C','D','E','F','G','H'])-set(prefix))
        if res is None:
            return error("skipping min_cycle_aux (unimplemented)")
        # sanity check the reference solution
        if not check_cycle(wg, solution, prefix, wopt): return
        print("reference solution is {}".format(solution))
        if not check_cycle(wg, res[1], prefix, wopt): return
    print("Success!")

def equal_cycles(L1,L2):
    if len(L1)!=len(L2): return False
    if len(L1)==1: return L1[0]==L2[0]
    L1.pop(); L2.pop()
    if not L1[0] in L2: return False
    i=L2.index(L1[0])
    if L1==L2[i:]+L2[:i]: return True
    L2.reverse()
    i=L2.index(L1[0])
    if L1==L2[i:]+L2[:i]: return True
    return False

def test2():
    global L_tutorial
    print("\ntesting min_cycle")
    wg=WG(L_tutorial)
    print("Test on the graph of Figure 1")
    res=wg.min_cycle()
    if res is None:
        return error("skipping min_cycle (unimplemented)")
    expected=['G', 'H', 'A', 'F', 'E', 'B', 'C', 'D', 'G']
    if res[0]==8 and equal_cycles(res[1],expected):
        print("Success!")
    else:
        print("Error, expected")
        print((8,expected))
        print("but output is")
        print(res)
        error("min_cycle failed")

def test4():
    global L_tutorial
    print("\ntesting lower_bound")
    wg=WG(L_tutorial)
    print("Test on the graph of Figure 1")
    print("Test with input L=['F']")
    res=wg.lower_bound(0,['F'],set(['A', 'B', 'C', 'D', 'E', 'G', 'H']))
    if res is None:
        return error("skipping lower_bound (unimplemented)")
    if res!=8: return error("Error, expected 8, but output is "+str(res))
    print("Test with input L=['D','E']")
    res=wg.lower_bound(2,['D','E'],set(['A', 'B', 'C', 'F', 'G', 'H']))
    if res!=10: return error("Error, expected 10, but output is "+str(res))
    print("Test with input L=['A','B','E','F']")
    res=wg.lower_bound(4,['A','B','E','F'],set(['C', 'D', 'G', 'H']))
    if res!=10: return error("Error, expected 10, but output is "+str(res))
    print("Test with input L=['A','B','E','D']")
    res=wg.lower_bound(5,['A','B','E','D'],set(['C', 'F', 'G', 'H']))
    if res!=15: return error("Error, expected 15, but output is "+str(res))
    print("Success!")

def random_graph(n):
    L=[]
    for i in range(n):
        for j in range(i+1,n):
            L.append([i,j,random.random()])
    return WG(L)

def test_random_graph(n):
    print("\ntesting random graphs")
    wg=random_graph(n)
    start = time.time()
    res1 = wg.min_cycle()
    if res1 is None:
        return error("skipping random graphs (min_cycle not implemented)")
    check_cycle(wg, res1[1])
    elapsed = (time.time() - start)
    print("min_cycle took time "+str(elapsed))
    start = time.time()
    res2 = wg.min_cycle_using_bound()
    if res2 is None:
        return error("skipping random graphs (min_cycle not implemented)")
    check_cycle(wg, res2[1])
    elapsed = (time.time() - start)
    print("min_cycle_using_bound took time "+str(elapsed))
    if abs(res1[0]-res2[0])>=0.001:
        return error("min_cycle and min_cycle_using_bound did not return paths of the same length")
    print("Success!")

def read_cities():
    cities=["Barcelona","Belgrade","Berlin","Brussels","Bucharest","Budapest","Copenhagen","Dublin",
            "Hamburg","Istanbul","Kiev","London","Madrid","Milan","Moscow","Munich","Paris","Prague",
            "Rome","Saint Petersburg", "Sofia", "Stockholm", "Vienna", "Warsaw"]
    distances=[]
    with open("cities.txt") as f:
        content = f.readlines()
        distances = [x.strip().split() for x in content]
        #print(content)
    list_edges=[]
    for j in range(1,len(cities)):
        for i in range(j):
            list_edges.append([cities[i],cities[j],int(distances[i][j])])
    return WG(list_edges)

def display_min_tour_cities(cities_in_tour, wopt):
    wg=read_cities()
    wg.induce_by_subset(cities_in_tour)
    #wg.display()
    print(str(len(cities_in_tour))+" cities in the tour")
    res = wg.min_cycle_using_bound()
    if res is None:
        return error("skipping min_cycle_using_bound (unimplemented)")
    print(res)
    if not check_cycle(wg, res[1], [], wopt): return False
    return True

def test_trip():
    print("\ntesting with cities")
    cities_in_tour1=set(["Belgrade","Berlin","Budapest","Copenhagen","Brussels", "Stockholm", "Vienna"])
    if not display_min_tour_cities(cities_in_tour1, 4505): return
    cities_in_tour2=set(["Barcelona","Belgrade","Berlin","Brussels","Hamburg","Paris","Istanbul","Kiev","London","Moscow","Prague","Rome","Saint Petersburg", "Sofia", "Stockholm", "Vienna"])
    if not display_min_tour_cities(cities_in_tour2, 9518): return
    print("Success!")


''' CALLS TO TEST FUNCTIONS '''

test1()
test2()
test4()
n=9; test_random_graph(n)
test_trip()



