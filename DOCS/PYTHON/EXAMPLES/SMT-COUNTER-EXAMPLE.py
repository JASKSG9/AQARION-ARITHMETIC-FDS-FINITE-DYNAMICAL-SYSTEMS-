from z3 import *
# Define integer variables for T(x) for x in 0..n-1
# Define constraints for P
# Ask Z3: "Find me a T where D=0 AND C != 0"
# If Z3 returns SAT, you have a counterexample certificate for huge n.
