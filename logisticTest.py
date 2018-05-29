import scipy.optimize as opt
import numpy as np
from numpy import exp

START_FINISH = (0.05, 0.95)
dose = 5

def f(vars):
    k, z = vars
    firstEq = dose/(1+exp(-k*(240-90))) + z - START_FINISH[0]
    secondEq = dose/(1+exp(-k*(15-90))) + z - (dose-(1-START_FINISH[1]))
    return firstEq, secondEq

k, z= opt.fsolve(f, (0.0, 0.0))
print(k, z)
