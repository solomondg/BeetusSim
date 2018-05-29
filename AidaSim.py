#!/usr/bin/env python3

# import numpy as np
# import time


class AIDASim:
    def __init__(self):
        self.ke = 5.4      # l/hr
        self.k1 = 0.025    # /hr
        self.k2 = 1.25     # /hr
        self.Ibasal = 10   # mU/l
        self.Km = 10       # mmol/l
        self.GI = 0.54     # mmol/hr/kg
        self.GX = 5.3      # mmol/l
        self.c = 0.015     # mmol/hr/kg/mU*l
        self.kgabs = 1     # /hr
        self.Vmaxge = 120  # mmol/hr
        self.VI = 0.142    # l/kg
        self.Vg = 0.22     # l/kg

        self.a = 0  # TODO: Get params
        self.b = 0  # TODO: Get params
        self.s = 0  # TODO: Get params

        self.D = 0         # Dose
        self.t = 0         # Time elapsed from insulin injection

        self.time = 0     # Simulator ticks (time)

        self.I = 0         # Plasma insulin concentration
        self.Ia = 0        # Active insulin pool

    def T50(self):
        """calculates time when 50% of dose will be absorbed"""
        return (self.a * self.D) + self.b

    def Iabs(self, t):
        """calculates current insulin absorbtion rate"""
        top = self.s * self.t * self.T50(self.t) * self.D
        bottom = self.t * (self.T50(self.t) + self.t)**2
        return top/bottom

    def di_dT(self, old, dt, t):
        """Change in plasma insulin concentration. Old is the current insulin
        concentration, dt is the change in time, and """
        term1 = self.Iabs(t)/self.VI
        term2 = self.ke * self.I
        return old + dt*(term1 - term2)  # Shitty version of euler's method

    def dia_dt(self, old, dt):
        term1 = (self.k1 * self.I)
        term2 = (self.k2 * self.Ia)
        return old + dt*(term1 - term2)

    def Iss(self):
        return self.I


