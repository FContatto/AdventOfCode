words2 = '''jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr'''


from collections import defaultdict, deque
def build_graph(words):
    rows = words.split('\n')
    graph = defaultdict(list)
    for r in rows:
        v, edges = r.split(': ')
        edges = edges.split()
        graph[v].extend(edges)
        for e in edges:
            graph[e].append(v)
    return graph


def get_edges(graph):
    edges = set()
    for k, v_ls in graph.items():
        for v in v_ls:
            if (v, k) not in edges:
                edges.add((k,v))
    return list(edges)

def calculate_connected_component(graph, start, end):
    seen = set()
    to_visit = deque([start])
    while len(to_visit) > 0:
        next_v = to_visit.pop()
        if start == end:
            return None
        if next_v in seen:
            continue
        seen.add(next_v)
        for next_v_2 in graph[next_v]:
            if next_v_2 not in seen:
                to_visit.appendleft(next_v_2)
    return len(seen)

def shortest_path_bfs(graph, start_v, end_v):
    seen = dict()
    to_visit = deque([(start_v, None, 0)])
    while len(to_visit) > 0:
        furthest_v, prev_v, longest_dist = to_visit.pop()
        if furthest_v in seen:
            continue
        seen[furthest_v] = prev_v
        if furthest_v == end_v:
            shortest_path = [end_v]
            end = end_v
            while start_v != end:
                end = seen[end]
                shortest_path.append(end)
            shortest_path = shortest_path[::-1]
            return [(shortest_path[i], shortest_path[i+1]) for i in range(len(shortest_path)-1)]
        for next_v_2 in graph[furthest_v]:
            if next_v_2 not in seen:
                to_visit.appendleft((next_v_2, furthest_v, longest_dist + 1))
    return None

def calculate_components(words):
    graph = build_graph(words)
    edges = get_edges(graph)
    n = len(graph)
    for i in range(len(edges)-2):
        v1, v2 = edges[i]
        graph[v1].remove(v2)
        graph[v2].remove(v1)
        shortest_path_1 = shortest_path_bfs(graph, v1, v2)
        if shortest_path_1 is None:
            continue
        for edge_2 in shortest_path_1:
            v3, v4 = edge_2
            graph[v3].remove(v4)
            graph[v4].remove(v3)
            shortest_path_1_another = shortest_path_bfs(graph, v1, v2)
            if shortest_path_1_another is None:
                continue
            shortest_path_2 = shortest_path_bfs(graph, v3, v4)
            if shortest_path_2 is None:
                continue
            shortest_path_2 = set(shortest_path_2)
            #the third edge to remove must be in the intersection of these paths
            third_edge_candidate = []
            for e in shortest_path_1_another:
                e_v1, e_v2 = e
                if (e in shortest_path_2) or ((e_v2,e_v1) in shortest_path_2):
                    third_edge_candidate.append(e)
            for edge_3 in third_edge_candidate:
                v5, v6 = edge_3
                graph[v5].remove(v6)
                graph[v6].remove(v5)
                conn_comp_len = calculate_connected_component(graph, v5, v6)
                if conn_comp_len is not None:
                    conn_comp_len_2 = calculate_connected_component(graph, v6, v5)
                    #check there are only 2 connected components
                    if n == conn_comp_len + conn_comp_len_2:
                        return conn_comp_len*conn_comp_len_2
                graph[v5].append(v6)
                graph[v6].append(v5)
            graph[v3].append(v4)
            graph[v4].append(v3)
        graph[v1].append(v2)
        graph[v2].append(v1)

    return 1

print(calculate_components(words))