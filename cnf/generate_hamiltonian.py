import sys
import collections

PREFIX = "h"


class Edge:
    def __init__(self, source, target):
        self.source = source
        self.target = target


def calculate_num_nodes(edges):
    # Assume that the node ids that are references form a contiguous interval
    cur_min = sys.maxint
    cur_max = - sys.maxint - 1
    for e in edges:
        cur_min = min(cur_min, e.source)
        cur_min = min(cur_min, e.target)
        cur_max = max(cur_max, e.source)
        cur_max = max(cur_max, e.target)

    return cur_max - cur_min + 1


def generate_mapping(edges, num_nodes):
    # h_{11}, h_{12}, ... h_{16}
    # h_{21}, ...

    dimacs_map = collections.defaultdict(collections.defaultdict)
    assigned_id = 1
    for order_idx in range(1, num_nodes + 1):
        for node_idx in range(1, num_nodes + 1):
            dimacs_map[order_idx][node_idx] = assigned_id
            assigned_id += 1

    return dimacs_map


if __name__ == "__main__":
    edges = [Edge(1, 3), Edge(1, 5), Edge(2, 5),
             Edge(3, 4), Edge(3, 5), Edge(4, 2)]

    num_nodes = calculate_num_nodes(edges)

    dimacs_map = generate_mapping(edges, num_nodes)

    print "c At most one edge"
    for o in range(1, num_nodes + 1):
        for n1 in range(1, num_nodes + 1):
            for n2 in range(n1 + 1, num_nodes + 1):
                if n1 == n2:
                    continue
                print -dimacs_map[o][n1], -dimacs_map[o][n2], "0"

    print "c At least one edge"
    for o in range(1, num_nodes + 1):
        lits = []
        for e in range(1, num_nodes + 1):
            lits.append(dimacs_map[o][e])

        s = " ".join(map(lambda item: str(item), lits)) + " 0"
        print s

    print "c Each node appears in path"
    for u in range(1, num_nodes + 1):
        lits = []
        for o in range(1, num_nodes + 1):
            lits.append(dimacs_map[o][u])
        s = " ".join(map(lambda item: str(item), lits)) + " 0"
        print s

    print "c Each node appears at most once in path"
    for u in range(1, num_nodes + 1):
        for k in range(1, num_nodes + 1):
            for l in range(1, num_nodes + 1):
                if k == l:
                    continue
                print -dimacs_map[k][u], -dimacs_map[l][u], "0"

    print "c Prevent illegal steps"
    lits = []
    # Populate a list of all possible edges
    for u in range(1, num_nodes + 1):
        for v in range(1, num_nodes + 1):
            lits.append((u, v))

    # Remove the existing edges, so that you are left with the inexistent edges
    for edge in edges:
        if (edge.source, edge.target) in lits:
            lits.remove((edge.source, edge.target))

    for (src, tgt) in lits:
        for o in range(1, num_nodes):
            print -dimacs_map[o][src], -dimacs_map[o + 1][tgt], "0"

