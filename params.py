from blist import sorteddict
from numpy.random import normal

# in carbs absorbed per unit administered
# this operates directly off of the stomach pool of carbs
# as such, it's more effective to "intercept" eaten carbs
# this is completely independant from carb-bgl sensitivity and insulin-bgl sensitivity
insulinToCarb = sorteddict(
    {
        0 * 60: 11,  # Midnight
        6 * 60: 7,  # 6 AM
        9 * 60: 5, # 9 AM
        12 * 60: 8, # Noon
        (3 + 12) * 60: 7, # 3 PM
        (7 * 12) * 60: 11, # 7 PM
    }
)

# TODO: Consider making this add to the stomach carb pool (or it's own?)
# in mg/dl per hour, how much the bgl rises without any intervention (fuck you too, liver)
liverGlycogenRisePerHour = sorteddict(
    {
        0 * 60: 20,  # Midnight
        4 * 60: 50,  # 4 AM - dawn effect lmao fuck
        7 * 60: 30, # 7 AM
        12 * 60: 20, # Noon
        (3 + 12) * 30: 7, # 3 PM
        (7 * 12) * 30: 11, # 7 PM
    }
)

# in mg/dl per unit
# how much one unit of insulin lowers blood sugar
insulinSensitivityFactor = sorteddict(
    {
        0 * 60: 20,  # Midnight
        6 * 60: 25,  # 6 AM
        9 * 60: 20, # 9 AM
        12 * 60: 25, # Noon
        (3 + 12) * 20: 7, # 3 PM
        (7 * 12) * 30: 11, # 7 PM
    }
)

insulinDoseBaseSensitivityMultiplier = 1.0  # in case we want to reduce and simulate pump being retard
# all insulin doses will be added with a fuzzing factor proportional to the dose size
insulinDoseFuzzPercentage = 0.1  # scale
insulinDoseFuzzBiasFactorPercentage = -0.1  # +/- bias

insulinInfluxDefaultBaseTime = 15.0  # so insulinEndBaseTime is adaptable
insulinInfluxBaseTime = insulinInfluxDefaultBaseTime  # in case we want to increase and simulate scar tissue or something
# all insulin influx times will be added with a fuzzing factor
insulinInfluxFuzzPercentage = 0.1  # scale
insulinInfluxFuzzBiasFactorPercentage = 0.1  # +/- bias

insulinDefaultEndBaseTime = 240.0
insulinDefaultPeakBaseTime = 90.0
insulinEndBaseTime = (insulinDefaultEndBaseTime-insulinInfluxDefaultBaseTime) # adapts to insulin influx time
insulinPeakBaseTime = (insulinDefaultPeakBaseTime-insulinInfluxDefaultBaseTime) # adapts to insulin influx time

insulinStartTolerance = 0.05
insulinEndTolerance = 0.05



glycogenDoseBaseSensitivityMultiplier = 1.0  # in case we want to reduce and simulate pump being retard
# all glycogen doses will be added with a fuzzing factor proportional to the dose size
glycogenDoseFuzzPercentage = 0.3  # livers are fuckin retarded lmao
glycogenDoseFuzzBiasFactorPercentage = -0.0  # +/- bias

glycogenInfluxDefaultBaseTime = 1.0  # so glycogenEndBaseTime is adaptable
glycogenInfluxBaseTime = glycogenInfluxDefaultBaseTime  # in case we want to increase and simulate scar tissue or something
# all glycogen influx times will be added with a fuzzing factor
glycogenInfluxFuzzPercentage = 0.1  # scale
glycogenInfluxFuzzBiasFactorPercentage = 0.0  # +/- bias

glycogenDefaultEndBaseTime = 30.0
glycogenDefaultPeakBaseTime = 15.0
glycogenEndBaseTime = (glycogenDefaultEndBaseTime-glycogenInfluxDefaultBaseTime) # adapts to glycogen influx time
glycogenPeakBaseTime = (glycogenDefaultPeakBaseTime-glycogenInfluxDefaultBaseTime) # adapts to glycogen influx time

glycogenStartTolerance = 0.05
glycogenEndTolerance = 0.05

simTickMinutes = 5
