include "alldifferent.mzn";

array[1..5] of var 1..5: path;

constraint alldifferent(path);

solve satisfy;

output ["Path: " ++ show(path)];
