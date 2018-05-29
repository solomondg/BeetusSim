from utils.ShittyLogisticAbsorbtion import ShittyLogisticAbsorbtion

from utils.calc import *
from utils.util import *


class MainSim:
    activeInsulinDoses: [ShittyLogisticAbsorbtion] = []
    activeGlycogenDoses: [ShittyLogisticAbsorbtion] = []
    activeCarbDoses: [ShittyLogisticAbsorbtion] = []

    time = 0  # in minutes, 0 to 1440
    bgl = 120
    carbPool = 0

    insulinHistory = []
    glycogenHistory = []
    carbHistory = []

    def __init__(self):
        pass

    def doseInsulin(self, *, dose):
        adjDose = getAdjustedInsulinDose(dose)
        adjInflux = getAdjustedInsulinInflux(insulinInfluxBaseTime)
        adjEnd = getAdjustedInsulinEndTime(adjInflux)
        adjPeak = getAdjustedInsulinPeakTime(adjInflux)
        self.activeInsulinDoses.append(
            ShittyLogisticAbsorbtion(
                dose=adjDose,
                influxTime=adjInflux,
                totalTime=adjEnd,
                peakTime=adjPeak,
                startTime=self.time,
                startTolerance=insulinStartTolerance,
                endTolerance=insulinEndTolerance
            )

        )

    def doseGlycogen(self, *, dose):
        adjDose = getAdjustedGlycogenDose(dose)
        print("Dosing glycogen", adjDose)
        adjInflux = getAdjustedGlycogenInflux(glycogenInfluxBaseTime)
        adjEnd = getAdjustedGlycogenEndTime(adjInflux)
        adjPeak = getAdjustedGlycogenPeakTime(adjInflux)
        self.activeGlycogenDoses.append(
            ShittyLogisticAbsorbtion(
                dose=adjDose,
                influxTime=adjInflux,
                totalTime=adjEnd,
                peakTime=adjPeak,
                startTime=self.time,
                startTolerance=insulinStartTolerance,
                endTolerance=insulinEndTolerance
            )

        )

    def doseCarb(self, *, dose, glycemicIndex):  # TODO
        pass

    def removeAbsorbed(self):
        for n in [self.activeInsulinDoses, self.activeGlycogenDoses, self.activeCarbDoses]:
            toPop = []
            for i in range(len(n)):
                if n[i].isAbsorbed(time=self.time):
                    toPop += [i]
            print(toPop)
            for i in toPop:
                n.pop(i)

    def tick(self):
        basalGlycogen = True

        # dose basal glycogen
        if basalGlycogen:
            self.doseGlycogen(
                dose=getValueOfClosestKey(
                    key=self.time,
                    dict=liverGlycogenRisePerHour
                ) / (60 / simTickMinutes)
            )

        totalInsulinPool = 0.0
        for profile in self.activeInsulinDoses:  # TODO: First apply to carb pool?
            totalInsulinPool += profile.getRemaining(time=self.time)
            absorbedInsulin = profile.getAbsorbtion(startTime=self.time, endTime=self.time + simTickMinutes)
            insulinSens = getValueOfClosestKey(key=self.time, dict=insulinSensitivityFactor)
            self.bgl -= absorbedInsulin * insulinSens
            self.insulinHistory.append([self.time, totalInsulinPool, absorbedInsulin])

        totalGlycogenPool = 0.0
        for profile in self.activeGlycogenDoses:
            totalGlycogenPool += profile.getRemaining(time=self.time)
            absorbedGlycogen = profile.getAbsorbtion(startTime=self.time, endTime=self.time + simTickMinutes)
            self.bgl -= absorbedGlycogen * 1  # Glycogen sensitivity is one cause the dose is defined in terms of mg/dl
            self.glycogenHistory.append([self.time, totalGlycogenPool, absorbedGlycogen])

        self.removeAbsorbed()  # remove doses that have run their course

        self.time += simTickMinutes

        print(self.time, self.bgl, totalGlycogenPool)
