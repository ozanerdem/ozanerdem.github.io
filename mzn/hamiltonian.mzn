include "alldifferent.mzn";

array[1..5] of var 1..5: path;

array[1..6] of 1..5: source = [1, 1, 2, 3, 3, 4];
array[1..6] of 1..5: target = [3, 5, 5, 4, 5, 2];

predicate edge(int: u, int: v) =
    exists(e in 1..6)(source[e] == u /\ target[e] == v);

predicate precedes(int: u, int: v) = exists(i in 1..4)(path[i] == u /\ path[i + 1] == v);

constraint alldifferent(path);

constraint forall(v1, v2 in 1..5)(not edge(v1, v2) -> not precedes(v1, v2));

solve satisfy;

output ["Path: " ++ show(path)];
