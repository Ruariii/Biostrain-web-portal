import pandas as pd
import numpy as np
import statistics as st
import os
import datetime

####################################################################################################




def playerPlot(playerTestData, name):
    cols = ["Index", "Org", "User", "Timestamp", "Protocol", "TZ", "Left0ms", "Left50ms", "Left100ms", "Left150ms",
            "Left200ms", "Left250ms", "Left300ms", "Leftpeak", "Right0ms", "Right50ms", "Right100ms", "Right150ms",
            "Right200ms", "Right250ms", "Right300ms", "Rightpeak", "Combined0ms", "Combined50ms", "Combined100ms",
            "Combined150ms", "Combined200ms", "Combined250ms", "Combined300ms", "Combinedpeak"]

    # get dataArray - all tests
    dataArray = []
    infoArray = []
    for i in playerTestData:
        dataArray.append((i.Index, i.Org, i.User, i.Timestamp, i.Protocol, i.TZ,
                         i.Left0ms, i.Left50ms, i.Left100ms,
                         i.Left150ms, i.Left200ms, i.Left250ms,
                         i.Left300ms, i.Leftpeak, i.Right0ms,
                         i.Right50ms, i.Right100ms, i.Right150ms,
                         i.Right200ms, i.Right250ms, i.Right300ms,
                         i.Rightpeak, i.Combined0ms, i.Combined50ms,
                         i.Combined100ms, i.Combined150ms, i.Combined200ms,
                         i.Combined250ms, i.Combined300ms, i.Combinedpeak))

        infoArray.append((i.Org, i.User, i.Timestamp, i.Protocol, i.TZ,
                         i.Leftpeak, i.Rightpeak))

    # get last 5 tests
    end = len(dataArray) - 1
    if len(dataArray)>5:
        dataArrayHead = infoArray[end-5:end]
    else:
        dataArrayHead = infoArray[0:end]

    # split into baseline & fatigue tests based on protocol name
    baselineTests, fatigueTests = [], []
    # create dictionary objects
    baselineDict, fatigueDict = {}, {}
    for row in dataArray:
        if "sprint" in row[4] or "fatigue" in row[4] or "Sprint" in row[4] or "Fatigue" in row[4]:
            fatigueTests.append(row)
            fatigueDict[row[4]] = {}
            # add keys to dicts
            for col in cols:
                fatigueDict[row[4]][col] = []

        else:
            baselineTests.append(row)
            baselineDict[row[4]] = {}
            # add keys to dicts
            for col in cols:
                baselineDict[row[4]][col] = []
    # populate dicts
    for row in dataArray:
        if "sprint" in row[4] or "fatigue" in row[4] or "Sprint" in row[4] or "Fatigue" in row[4]:
            for i in range(len(cols)):
                fatigueDict[row[4]][cols[i]].append(row[i])
        else:
            for i in range(len(cols)):
                baselineDict[row[4]][cols[i]].append(row[i])

    # BASELINE - get best scores from each protocol
    baselineMax = []
    count = 1
    for protocol in baselineDict:
        for key in baselineDict[protocol]:
            if "150" in key or "peak" in key:
                maxval = max(baselineDict[protocol][key])
                maxidx = np.argmax(baselineDict[protocol][key])
                maxvaltz = baselineDict[protocol]['TZ'][maxidx]
                maxvaltime = baselineDict[protocol]['Timestamp'][maxidx]

                baselineMax.append((count, protocol, key, maxval, maxvaltz, maxvaltime))
            else:
                continue
        count += 1

    # FATIGUE - get best scores from each protocol (may be some other metrics from fatigue tests)
    fatigueMax = []
    count = 1
    for protocol in fatigueDict:
        for key in fatigueDict[protocol]:
            if "150" in key or "peak" in key:
                maxval = max(fatigueDict[protocol][key])
                maxidx = np.argmax(fatigueDict[protocol][key])
                maxvaltz = fatigueDict[protocol]['TZ'][maxidx]
                maxvaltime = fatigueDict[protocol]['Timestamp'][maxidx]

                fatigueMax.append((count, protocol, key, maxval, maxvaltz, maxvaltime))
            else:
                continue
        count += 1

    activityLog = {name: {}}
    for row in dataArray:
        activityLog[name][row[3]] = {}
        activityLog[name][row[3]]['protocol'] = []
        activityLog[name][row[3]]['count'] = []
    for key in activityLog[name]:
        counter = 0
        for row in dataArray:
            if row[3] == key:
                counter += 1
                pro = row[4]
            else:
                continue
        activityLog[name][key]['count']=counter
        activityLog[name][key]['protocol']=pro

    timeArray=[time for time in activityLog[name]]
    countArray, proArray = [], []
    for time in timeArray:
        countArray.append(activityLog[name][time]['count'])
        proArray.append(activityLog[name][time]['protocol'])

    a = datetime.datetime.today()

    timeExt = timeArray
    countExt = countArray
    strTime = timeExt[len(timeArray) - 1]
    timeObj = datetime.datetime.strptime(strTime, '%d/%m/%Y')
    x = 1
    while timeObj < a:
        timeObj = timeObj + datetime.timedelta(days=x)
        strTime = datetime.datetime.strftime(timeObj, '%d/%m/%Y')
        timeExt.append(strTime)
        countExt.append(0)
        x += 1



    LHTZdata, RHTZdata = [], []
    for row in baselineTests:
        if row[5] == 'LHTZ':
            LHTZdata.append(row)
        else:
            RHTZdata.append(row)
    front150L, frontPeakL, back150L, backPeakL, combined150L, combinedPeakL = 0, 0, 0, 0, 0, 0
    front150R, frontPeakR, back150R, backPeakR, combined150R, combinedPeakR = 0, 0, 0, 0, 0, 0
    radarLabels = ['Front force at 150ms', 'Front peak force', 'Back force at 150ms', 'Back peak force',
                   'Combined force at 150ms', 'Combined peak force']
    for row in LHTZdata:
        if row[9] > front150L:
            front150L = row[9]
        if row[13] > frontPeakL:
            frontPeakL = row[13]
        if row[17] > back150L:
            back150L = row[17]
        if row[21] > backPeakL:
            backPeakL = row[21]
        if row[25] > combined150L:
            combined150L = row[25]
        if row[29] > combinedPeakL:
            combinedPeakL = row[29]
    radarDataL = [front150L, frontPeakL, back150L, backPeakL, combined150L, combinedPeakL]
    for row in RHTZdata:
        if row[9] > back150R:
            back150R = row[9]
        if row[13] > backPeakR:
            backPeakR = row[13]
        if row[17] > front150R:
            front150R = row[17]
        if row[21] > frontPeakR:
            frontPeakR = row[21]
        if row[25] > combined150R:
            combined150R = row[25]
        if row[29] > combinedPeakR:
            combinedPeakR = row[29]
    radarDataR = [front150R, frontPeakR, back150R, backPeakR, combined150R, combinedPeakR]

    fatigueDict = {}
    fLabels = ['Force at 0ms', 'Force at 50ms', 'Force at 100ms', 'Force at 150ms',
                'Force at 200ms', 'Force at 250ms', 'Force at 300ms']
    for row in fatigueTests:
        fatigueDict[row[4]] = {}
        fatigueDict[row[4]]['LHTZ'] = {}
        fatigueDict[row[4]]['RHTZ'] = {}
        fatigueDict[row[4]]['LHTZ']['Fresh'] = {}
        fatigueDict[row[4]]['LHTZ']['Fatigued'] = {}
        fatigueDict[row[4]]['LHTZ']['Fresh']['Front leg'] = []
        fatigueDict[row[4]]['LHTZ']['Fatigued']['Back leg'] = []
        fatigueDict[row[4]]['RHTZ']['Fresh'] = {}
        fatigueDict[row[4]]['RHTZ']['Fatigued'] = {}
        fatigueDict[row[4]]['RHTZ']['Fresh']['Front leg'] = []
        fatigueDict[row[4]]['RHTZ']['Fatigued']['Back leg'] = []

    for key in fatigueDict:
        fa0LF, fa50LF, fa100LF, fa150LF, fa200LF, fa250LF, fa300LF, peakLF = [], [], [], [], [], [], [], []
        fa0LB, fa50LB, fa100LB, fa150LB, fa200LB, fa250LB, fa300LB, peakLB = [], [], [], [], [], [], [], []
        fa0RF, fa50RF, fa100RF, fa150RF, fa200RF, fa250RF, fa300RF, peakRF = [], [], [], [], [], [], [], []
        fa0RB, fa50RB, fa100RB, fa150RB, fa200RB, fa250RB, fa300RB, peakRB = [], [], [], [], [], [], [], []
        i = 0
        for i in range(len(fatigueTests)):
            if key == fatigueTests[i][4]:
                if fatigueTests[i][5] == 'LHTZ':
                    fa0LF.append(fatigueTests[i][6])
                    fa50LF.append(fatigueTests[i][7])
                    fa100LF.append(fatigueTests[i][8])
                    fa150LF.append(fatigueTests[i][9])
                    fa200LF.append(fatigueTests[i][10])
                    fa250LF.append(fatigueTests[i][11])
                    fa300LF.append(fatigueTests[i][12])
                    peakLF.append(fatigueTests[i][13])
                    fa0LB.append(fatigueTests[i][14])
                    fa50LB.append(fatigueTests[i][15])
                    fa100LB.append(fatigueTests[i][16])
                    fa150LB.append(fatigueTests[i][17])
                    fa200LB.append(fatigueTests[i][18])
                    fa250LB.append(fatigueTests[i][19])
                    fa300LB.append(fatigueTests[i][20])
                    peakLB.append(fatigueTests[i][21])
                else:
                    fa0RB.append(fatigueTests[i][6])
                    fa50RB.append(fatigueTests[i][7])
                    fa100RB.append(fatigueTests[i][8])
                    fa150RB.append(fatigueTests[i][9])
                    fa200RB.append(fatigueTests[i][10])
                    fa250RB.append(fatigueTests[i][11])
                    fa300RB.append(fatigueTests[i][12])
                    peakRB.append(fatigueTests[i][13])
                    fa0RF.append(fatigueTests[i][14])
                    fa50RF.append(fatigueTests[i][15])
                    fa100RF.append(fatigueTests[i][16])
                    fa150RF.append(fatigueTests[i][17])
                    fa200RF.append(fatigueTests[i][18])
                    fa250RF.append(fatigueTests[i][19])
                    fa300RF.append(fatigueTests[i][20])
                    peakRF.append(fatigueTests[i][21])

        fatigueDict[key]['LHTZ']['Fresh']['Front leg'] = (
        max(fa0LF, default=0), max(fa50LF, default=0), max(fa100LF, default=0), max(fa150LF, default=0),
        max(fa200LF, default=0), max(fa250LF, default=0), max(fa300LF, default=0), max(peakLF, default=0))
        fatigueDict[key]['LHTZ']['Fatigued']['Front leg'] = (
        min(fa0LF, default=0), min(fa50LF, default=0), min(fa100LF, default=0), min(fa150LF, default=0),
        min(fa200LF, default=0), min(fa250LF, default=0), min(fa300LF, default=0), min(peakLF, default=0))
        fatigueDict[key]['LHTZ']['Fresh']['Back leg'] = (
        max(fa0LB, default=0), max(fa50LB, default=0), max(fa100LB, default=0), max(fa150LB, default=0),
        max(fa200LB, default=0), max(fa250LB, default=0), max(fa300LB, default=0), max(peakLB, default=0))
        fatigueDict[key]['LHTZ']['Fatigued']['Back leg'] = (
        min(fa0LB, default=0), min(fa50LB, default=0), min(fa100LB, default=0), min(fa150LB, default=0),
        min(fa200LB, default=0), min(fa250LB, default=0), min(fa300LB, default=0), min(peakLB, default=0))

        fatigueDict[key]['RHTZ']['Fresh']['Front leg'] = (
        max(fa0RF, default=0), max(fa50RF, default=0), max(fa100RF, default=0), max(fa150RF, default=0),
        max(fa200RF, default=0), max(fa250RF, default=0), max(fa300RF, default=0), max(peakRF, default=0))
        fatigueDict[key]['RHTZ']['Fatigued']['Front leg'] = (
        min(fa0RF, default=0), min(fa50RF, default=0), min(fa100RF, default=0), min(fa150RF, default=0),
        min(fa200RF, default=0), min(fa250RF, default=0), min(fa300RF, default=0), min(peakRF, default=0))
        fatigueDict[key]['RHTZ']['Fresh']['Back leg'] = (
        max(fa0RB, default=0), max(fa50RB, default=0), max(fa100RB, default=0), max(fa150RB, default=0),
        max(fa200RB, default=0), max(fa250RB, default=0), max(fa300RB, default=0), max(peakRB, default=0))
        fatigueDict[key]['RHTZ']['Fatigued']['Back leg'] = (
        min(fa0RB, default=0), min(fa50RB, default=0), min(fa100RB, default=0), min(fa150RB, default=0),
        min(fa200RB, default=0), min(fa250RB, default=0), min(fa300RB, default=0), max(peakRB, default=0))

    i=0
    j=0
    fPlotDictL, fLabelDictL = {}, {}
    fPlotDictR, fLabelDictR = {}, {}
    for key in fatigueDict:
        for tz in fatigueDict[key]:
            for state in fatigueDict[key][tz]:
                for leg in fatigueDict[key][tz][state]:
                    if tz == 'LHTZ':
                        fPlotDictL[i] = list(fatigueDict[key][tz][state][leg])
                        fLabelDictL[i] = f'{key}: {leg}, {state}'
                        i+=1
                    else:
                        fPlotDictR[j] = list(fatigueDict[key][tz][state][leg])
                        fLabelDictR[j] = f'{key}: {leg}, {state}'
                        j+=1

    fAsymDict={}
    for key in fPlotDictR:
        fAsymDict[key]=[]
        for i in range(1, len(fPlotDictL[key])):
            try:
                fAsymDict[key].append(100*(fPlotDictR[key][i]-fPlotDictL[key][i])/max(fPlotDictR[key][i],fPlotDictL[key][i]))
            except:
                fAsymDict[key].append(0)


    flFatigue, blFatigue = [], []
    for key in fLabelDictL:
        if 'Front leg' in fLabelDictL[key]:
            flFatigue.append((fAsymDict[key]))
        else:
            blFatigue.append((fAsymDict[key]))

    flAsym, blAsym = [], []
    for i in range(len(flFatigue[0])):
        avgFL = []
        avgBL = []
        for row in range(len(flFatigue)):
            avgFL.append(flFatigue[row][i])
            avgBL.append(blFatigue[row][i])
        flAsym.append(sum(avgFL) / len(flFatigue))
        blAsym.append(sum(avgBL) / len(blFatigue))

    return baselineMax, timeArray, countArray, timeExt, \
           countExt, proArray, radarLabels, radarDataL, radarDataR, fPlotDictL,\
           fLabelDictL, fPlotDictR, fLabelDictR, fAsymDict, flAsym, blAsym, dataArrayHead


def squadPlot(squadTestData, squadPlayers, pro):
    cols = ["Index", "Org", "User", "Timestamp", "Protocol", "TZ", "Left0ms", "Left50ms", "Left100ms", "Left150ms",
            "Left200ms", "Left250ms", "Left300ms", "Leftpeak", "Right0ms", "Right50ms", "Right100ms", "Right150ms",
            "Right200ms", "Right250ms", "Right300ms", "Rightpeak", "Combined0ms", "Combined50ms", "Combined100ms",
            "Combined150ms", "Combined200ms", "Combined250ms", "Combined300ms", "Combinedpeak"]

    players=[]
    for i in squadPlayers:
        players.append(i.User)

    # get dataArray - all tests
    dataArray = []
    infoArray = []
    for i in squadTestData:
        dataArray.append((i.Index, i.Org, i.User, i.Timestamp, i.Protocol, i.TZ,
                         i.Left0ms, i.Left50ms, i.Left100ms,
                         i.Left150ms, i.Left200ms, i.Left250ms,
                         i.Left300ms, i.Leftpeak, i.Right0ms,
                         i.Right50ms, i.Right100ms, i.Right150ms,
                         i.Right200ms, i.Right250ms, i.Right300ms,
                         i.Rightpeak, i.Combined0ms, i.Combined50ms,
                         i.Combined100ms, i.Combined150ms, i.Combined200ms,
                         i.Combined250ms, i.Combined300ms, i.Combinedpeak))

        infoArray.append((i.Org, i.User, i.Timestamp, i.Protocol, i.TZ,
                         i.Leftpeak, i.Rightpeak))
    # get last 5 tests
    end = len(dataArray) - 1
    if len(dataArray)>5:
        dataArrayHead = infoArray[end-5:end]
    else:
        dataArrayHead = infoArray[0:end]


    # get activity
    activityLog = {}
    for row in dataArray:
        activityLog[row[3]] = 0

    a = datetime.datetime.today()
    activeDates = list(activityLog.keys())
    lastAct = activeDates[len(activeDates)-1]
    timeObj = datetime.datetime.strptime(lastAct, '%d/%m/%Y')
    x=0
    while timeObj < a:
        timeObj = timeObj + datetime.timedelta(days=x)
        strTime = datetime.datetime.strftime(timeObj, '%d/%m/%Y')
        activityLog[strTime] = 0
        x+=1
    for key in activityLog:
        count=0
        for row in dataArray:
            if row[3] == key:
                count+=1
        activityLog[key]=count

    activeDates = list(activityLog.keys())
    testsCompleted = [activityLog[key] for key in activeDates]

    # get best/worst scores from each protocol
    best150, bestPeak = [], []
    FLpeakAsym, BLpeakAsym, FL150Asym, BL150Asym = [], [], [], []
    for player in players:
        max150, maxPeak = [], []
        FLmax150L, FLmaxPeakL = [], []
        BLmax150L, BLmaxPeakL = [], []
        FLmax150R, FLmaxPeakR = [], []
        BLmax150R, BLmaxPeakR = [], []
        for row in dataArray:
            if row[2] == player:
                max150.append(row[25])
                maxPeak.append(row[29])
                if row[5] == 'LHTZ':
                    FLmax150L.append(row[9])
                    FLmaxPeakL.append(row[13])
                    BLmax150L.append(row[17])
                    BLmaxPeakL.append(row[21])
                elif row[5] == 'RHTZ':
                    BLmax150R.append(row[9])
                    BLmaxPeakR.append(row[13])
                    FLmax150R.append(row[17])
                    FLmaxPeakR.append(row[21])

        best150.append(max(max150, default=0))
        bestPeak.append(max(maxPeak, default=0))
        flpL = max(FLmaxPeakL, default=0)
        blpL = max(BLmaxPeakL, default=0)
        fl150L = max(FLmax150L, default=0)
        bl150L = max(BLmax150L, default=0)
        flpR = max(FLmaxPeakR, default=0)
        blpR = max(BLmaxPeakR, default=0)
        fl150R = max(FLmax150R, default=0)
        bl150R = max(BLmax150R, default=0)

        try:
            FLpeakAsym.append(100 * (flpR - flpL) / (max(flpL, flpR)))
            FL150Asym.append(100 * (fl150R - fl150L) / (max(fl150L, fl150R)))
            BLpeakAsym.append(100 * (blpR - blpL) / (max(blpL, blpR)))
            BL150Asym.append(100 * (bl150R - bl150L) / (max(bl150L, bl150R)))
        except:
            FLpeakAsym.append(0)
            FL150Asym.append(0)
            BLpeakAsym.append(0)
            BL150Asym.append(0)

    # get best worst asymmtery
    LHTZdata, RHTZdata = [], []
    for row in dataArray:
        if row[5] == 'LHTZ':
            LHTZdata.append(row)
        else:
            RHTZdata.append(row)

    return dataArray, dataArrayHead, activeDates, testsCompleted, players, bestPeak, best150, FLpeakAsym, BLpeakAsym, FL150Asym, BL150Asym