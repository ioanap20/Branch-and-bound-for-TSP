# -*- coding: utf-8 -*-

import random
import math

class UF:
    def __init__(self,S):
        self.id={}
        for x in S:
            self.id[x]=x
        self.rank ={}
        for x in S:
            self.rank[x]=1  
        
    def union(self, p, q):
        r1 = self.find(p)
        r2 = self.find(q)
        
        if r1 == r2:
            return
                    
        if self.rank[r2] > self.rank[r1]:
            self.id[r1] = r2
        else:
            self.id[r2] = r1
            
        if self.rank[r2] == self.rank[r1]:
            self.rank[r1] += 1
        
    def find(self, p):
        if self.id[p] == p:
            return p
        # path compression
        self.id[p] = self.find(self.id[p])
        return self.id[p]

class WG:
    def __init__(self, L): # L is the list of edges
        L.sort(key= lambda e: e[2])
        self.edges=L
        self.adj={}
        for x in L:
            if x[0] not in self.adj:
                self.adj[x[0]]={x[1]:x[2]}
            else:
                self.adj[x[0]][x[1]]=x[2]
            if x[1] not in self.adj:
                self.adj[x[1]]={x[0]:x[2]}
            else:
                self.adj[x[1]][x[0]]=x[2]

    # QUESTION 1
    def min_cycle_aux(self,w,L,S):
        # TODO
        if S == set():
            if L[0] in self.adj[L[-1]]:
                return w + self.adj[L[-1]][L[0]], L + [L[0]]
            else:
                return math.inf, []
        
        best_cost = math.inf
        best_cycle = []
        
        for v in S:
            if v in self.adj[L[-1]]:
                new_w = w + self.adj[L[-1]][v]
                new_L = L + [v]
                new_S = S - {v}
                new_cost, new_cycle = self.min_cycle_aux(new_w, new_L, new_S)
                
                if new_cost < best_cost:
                    best_cost = new_cost
                    best_cycle = new_cycle
        
        
        return best_cost, best_cycle
    
    
    def get_vertices(self):
        return set(self.adj.keys())
     

    # QUESTION 2
    def min_cycle(self):
        # TODO
        vertex_set = self.get_vertices()
        best_cost = math.inf
        best_cycle = []
        for v in vertex_set:
            cost, cycle = self.min_cycle_aux(0, [v], vertex_set - {v})
            if cost < best_cost:
                best_cost = cost
                best_cycle = cycle
        return best_cost, best_cycle
        

    '''
    Question 3
    Put your answer here
    
    w_start is the cost to connect the first vertex in L to the vertices in S, w_end is the cost to connect the last vertex in L to the vertices in S. The lower bound is the sum of the cost of the current cycle, the cost to connect the first vertex in L to the vertices in S, the cost to connect the last vertex in L to the vertices in S, and the minimum cost to connect the vertices in S.
    and S is the cost to span S
    '''

    # QUESTION 4
    def lower_bound(self,w,L,S): # returns low(L), with w the cost of L, and S the set of vertices not in L
        # TODO
        w_start = math.inf
        w_end = math.inf
        for v in S:
            if v in self.adj[L[0]]:
                w_start = min(w_start, self.adj[L[0]][v])
            if v in self.adj[L[-1]]:
                w_end = min(w_end, self.adj[L[-1]][v])
        
        if w_start == math.inf or w_end == math.inf:
            return math.inf
        
        lower_bound = w + w_start + w_end + self.weight_min_tree(S)
        return lower_bound
        

    # QUESTION 5
    def min_cycle_aux_using_bound(self,bestsofar,w,L,S):
        # TODO
        
        if len(S) == 0:
            if L[0] in self.adj[L[-1]]:
                total_weight = w + self.adj[L[-1]][L[0]]
                if total_weight < bestsofar:
                    return total_weight, L + [L[0]]
            return math.inf, []
        
        if self.lower_bound(w, L, S) >= bestsofar:
            return math.inf, []
        
        min_cost = math.inf
        best_cycle = []
        
        for v in S:
            if v in self.adj[L[-1]]:
                new_w = w + self.adj[L[-1]][v]
                new_L = L + [v]
                S.remove(v)
                
                if self.lower_bound(new_w, new_L, S) < bestsofar or len(S) == 0:
                    new_cost, new_cycle = self.min_cycle_aux_using_bound(bestsofar, new_w, new_L, S)
                
                    if new_cost < bestsofar:
                        bestsofar = new_cost
                        best_cycle = new_cycle
                        min_cost = new_cost
                S.add(v)
                    
        
        return min_cost, best_cycle
        

    def min_cycle_using_bound(self):
        # TODO
        vertex_set = self.get_vertices()
        v = vertex_set.pop()
        return self.min_cycle_aux_using_bound(math.inf, 0, [v], vertex_set - {v})
#################################################################
## Auxiliary methods
#################################################################

    def weight_min_tree(self,S): # mincost among all trees whose spanned vertices are those in S
        if len(S)==1: return 0
        if len(S)==2:
            L=list(S)
            if L[0] in self.adj[L[1]]: return self.adj[L[0]][L[1]]
            else: return math.inf
        uf=UF(S)
        nr_components=len(S)
        weight=0
        for e in self.edges:
            if e[0] in S and e[1] in S:
                if uf.find(e[0])!=uf.find(e[1]):
                    weight=weight+e[2]
                    uf.union(e[0],e[1])
                    nr_components=nr_components-1
                    if nr_components==1:
                        return weight
        return math.inf

    def induce_by_subset(self,S): # reduces self.adj to keep only the edges with both ends in S
        new_adj={}
        for x in self.adj:
            for y in self.adj[x]:
                if x in S and y in S:
                    if x not in new_adj:
                        new_adj[x]={y:self.adj[x][y]}
                    else:
                        new_adj[x][y]=self.adj[x][y]
                    if y not in new_adj:
                        new_adj[y]={x:self.adj[y][x]}
                    else:
                        new_adj[y][x]=self.adj[y][x]
        self.adj=new_adj

    def display(self):
        print("Graph has "+str(len(self.adj))+" vertices")
        print()
        for x,y in self.adj.items():
            print("Neighbours of "+str(x)+":")
            for t,u in y.items():
                print(str(t)+" with weight "+str(u))
            print()
