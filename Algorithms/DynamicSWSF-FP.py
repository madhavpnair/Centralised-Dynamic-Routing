from heapdict import heapdict

INF = float('inf')

def DynamicSWSF_FP(N, E, U, d):
    min_heap = heapdict()
    rhs = [INF] * len(N)

    
    # lasr element is the sink
    sink = N[-1]
    rhs[sink] = 0
    
    # add inconsistent vertices to heap
    # sink can never be in U
    for u in U:
        rhs[u] = INF
        for (v, w) in E[u]:
            rhs[u] = min(rhs[u], d[v] + w)
        if rhs[u] != d[u]:
            min_heap[u] = min(rhs[u], d[u])
    
    # process heap
    while len(min_heap) > 0:
        u, dist_u = min_heap.popitem()
        if rhs[u] < d[u]:
            # u is over-consistent
            d[u] = rhs[u]
            for (v, w) in E[u]:
                rhs[v] = INF if v != sink else 0
                for (x, w_vx) in E[v]:
                    rhs[v] = min(rhs[v], d[x] + w_vx)
                if rhs[v] != d[v]:
                    min_heap[v] = min(rhs[v], d[v])
                else:
                    if v in min_heap:
                        del min_heap[v]
        
        else:
            # u is under-consistent
            d[u] = INF 
            for (v, w) in [(u, 0)] + E[u]:
                rhs[v] = INF if v != sink else 0
                for (x, w_vx) in E[v]:
                    rhs[v] = min(rhs[v], d[x] + w_vx)
                if rhs[v] != d[v]:
                    min_heap[v] = min(rhs[v], d[v])
                else:
                    if v in min_heap:
                        del min_heap[v]

    return d

# testing

N = [0, 1, 2]

E = {
    0: [(1, 2), (2, 20)],
    1: [(2, 3)],
    2: []
}

U = {0}

d = [13, 3, 0]

d_new = DynamicSWSF_FP(N, E, U, d)
print(d_new)


