from numpy.random import normal
from params import *


def getAdjustedInsulinDose(dose):
    return max(dose + normal(insulinDoseFuzzBiasFactorPercentage * dose, insulinDoseFuzzPercentage * dose), 0.0)


def getAdjustedInsulinInflux(influxTime):
    return max(influxTime + normal(insulinInfluxFuzzBiasFactorPercentage * influxTime,
                                   insulinInfluxFuzzBiasFactorPercentage * influxTime), 0.0)


def getAdjustedInsulinEndTime(influxTime):
    return insulinEndBaseTime + influxTime


def getAdjustedInsulinPeakTime(influxTime):
    return insulinPeakBaseTime + influxTime


def getAdjustedGlycogenDose(dose):
    return max(dose + normal(glycogenDoseFuzzBiasFactorPercentage * dose, glycogenDoseFuzzPercentage * dose), 0.0)


def getAdjustedGlycogenInflux(influxTime):
    return max(influxTime + normal(glycogenInfluxFuzzBiasFactorPercentage * influxTime,
                                   glycogenInfluxFuzzBiasFactorPercentage * influxTime), 0.0)


def getAdjustedGlycogenEndTime(influxTime):
    return glycogenEndBaseTime + influxTime


def getAdjustedGlycogenPeakTime(influxTime):
    return glycogenPeakBaseTime + influxTime
