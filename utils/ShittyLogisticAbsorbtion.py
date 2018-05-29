import numpy
import scipy
import scipy.optimize as opt
import numpy as np
from numpy import exp
from collections import namedtuple

# This is the worlds most ghetto insulin/food absorbtion
# class ShittyLogisticAbsorbtion:
#     def __init__(self, *, dose, totalTime, tolerance=0.05):
#         self.dose = dose
#         self.totalTime = totalTime
#         self.tolerance = tolerance
#
#     def calcAtPoint(self, time):  # t=0 is when this function started
#         if self.ret < self.dose * self.tolerance:
#             return 0

# 1/1+e^x

# Note: insulin absorption onset: 15 min
# Peak: 1.5h
# Total duration: 4h

# We need the absolute min of (-e^x/(e^x +1)^2) to be when x = 90
# We need dose/(1+e^-k*(x-x0)) to equal 5% of dose when x = 240
# We need dose/(1+e^-k*(x-x0)) to equal 95% of dose when x = 15

# Say dose = 1
# 1/(1+e^(-k*(240-90))) = 0.05 * 1
# 1/(1+e^(-k*(15-90))) = 0.95 * 1

# Wolfram alpha: 1/(1+e^(-k*(240-90))) + z = 0.1 and 1/(1+e^(-k*(15-90))) + z = 0.9, solve for k, z

INSULIN_TOTALTIME = 300
INSULIN_PEAKTIME = 90
INSULIN_STARTTOLERANCE = 0.05
INSULIN_FINISHTOLERANCE = 1 - 0.05

# shitty notes to self
# bgl affect factor: negative for insulin, positive for sugar/glucagon/whatever
# -25 for insulin
# +40 for food

# food:
# juice:
#   influx: 5
#   peak: 10
#   total: 15

# pizza:
#   influx: 30
#   peak: 60
#   total: 180

LogisticCurveTimePoints = namedtuple("LogisticCurveTimePoints", ['start', 'peak', 'end'])
LogisticCurveTolerances = namedtuple("LogisticCurveTolerances", ['start', 'end'])


class ShittyLogisticAbsorbtion:
    def __init__(self, *, dose,
                 influxTime=15, peakTime=90, totalTime=240, startTime=0, startTolerance=0.05, endTolerance=0.05):
        self.dose = dose
        self.timePoints = LogisticCurveTimePoints(start=influxTime, peak=peakTime, end=totalTime)
        self.tolerances = LogisticCurveTolerances(start=1 - startTolerance, end=endTolerance)
        self.startTime = startTime

        # Logistic function is of the form
        #      1
        #  --------           + z
        #   1 + e^(-k*(x-peak))
        #
        #
        # We need to find the equation for the function where
        # T=startTime -> latent=dose*(1-tolerance)
        # T=totalTime -> latent=dose*tolerance

        # Find:
        # - k
        # - L

        def tempSig(vars):
            k, z = vars
            firstEq = dose / (1 + exp(-k * (self.timePoints.end - 90))) + z - self.tolerances.end * dose
            secondEq = dose / (1 + exp(-k * (self.timePoints.start - 90))) + z - self.tolerances.start * dose
            return firstEq, secondEq

        self.k, self.z = opt.fsolve(tempSig, (0.0, 0.0))

    def logisticEquation(self, *, time):
        return self.dose / (1 + exp(-self.k * (time - self.timePoints.peak))) + self.z

    def getAbsorbtion(self, *, startTime, endTime):
        return self.logisticEquation(time=endTime-self.startTime) - self.logisticEquation(time=startTime-self.startTime)

    def getRemaining(self, *, time):
        return -self.getAbsorbtion(startTime=time-self.startTime, endTime=self.timePoints.end-self.startTime)

    def isAbsorbed(self, *, time):
        return time > self.startTime + self.timePoints.end + self.timePoints.start
