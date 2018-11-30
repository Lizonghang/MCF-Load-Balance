// load data
int NumNodes = ...;
int NumLinks = ...;
int NumPaths = ...;
int NumPairs = NumNodes*(NumNodes-1);
range Links = 1..NumLinks;
range Paths = 1..NumPaths;
range Pairs = 1..NumPairs;
int Capacity[Links] = ...;
int Demands[Pairs] = ...;
int Delta[Pairs][Links][Paths] = ...;

// decision variables
dvar float+ z;
dvar boolean x[Pairs][Paths];

minimize z;

subject to {
  forall( k in Pairs )
    ctDemand:
      sum( p in Paths )
        x[k][p] * Demands[k] == Demands[k];

  forall( l in Links )
    ctUtilizeRate:
      sum( k in Pairs )
        sum ( p in Paths )
          Delta[k][l][p] * x[k][p] * Demands[k] <= z * Capacity[l];
}
