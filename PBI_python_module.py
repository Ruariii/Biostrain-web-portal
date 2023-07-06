import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import time


####################################################################################################

def getPlayerDict(playerTestData):
    # get dataArray - all tests
    data = []
    for i in playerTestData:
        data.append((i.id, i.Org, i.User, i.Timestamp, i.Protocol,
                     i.Matchday, i.Strategy, i.Phase, i.TZ,
                     i.Left0ms, i.Left50ms, i.Left100ms,
                     i.Left150ms, i.Left200ms, i.Left250ms,
                     i.Left300ms, i.Leftpeak, i.Right0ms,
                     i.Right50ms, i.Right100ms, i.Right150ms,
                     i.Right200ms, i.Right250ms, i.Right300ms,
                     i.Rightpeak))

    timestamps = [row[3] for row in data]
    minute = 60
    timeadj = []
    j = 0
    for i in range(len(timestamps)):
        timeadj.append(round(timestamps[i] + (minute * j)))
        j += 1

    sessions = {}
    i = 0
    for row in data:
        date = datetime.fromtimestamp(timeadj[i]).strftime("%Y/%m/%d")
        protocol = row[4]
        sessions[f'{protocol}: {date}'] = {}
        sessions[f'{protocol}: {date}']['index'] = []
        sessions[f'{protocol}: {date}']['TZ'] = []
        sessions[f'{protocol}: {date}']['Protocol'] = []
        sessions[f'{protocol}: {date}']['Strategy'] = []
        sessions[f'{protocol}: {date}']['Matchday'] = []
        sessions[f'{protocol}: {date}']['Phase'] = []
        sessions[f'{protocol}: {date}']['Front leg force at 150ms'] = []
        sessions[f'{protocol}: {date}']['Front leg RFD 50-150ms'] = []
        sessions[f'{protocol}: {date}']['Front leg peak force'] = []
        sessions[f'{protocol}: {date}']['Back leg force at 150ms'] = []
        sessions[f'{protocol}: {date}']['Back leg RFD 50-150ms'] = []
        sessions[f'{protocol}: {date}']['Back leg peak force'] = []
        sessions[f'{protocol}: {date}']['Crush factor at 150ms'] = []
        sessions[f'{protocol}: {date}']['Combined RFD 50-150ms'] = []
        sessions[f'{protocol}: {date}']['Peak crush factor'] = []
        i += 1

    i = 0
    for row in data:
        date = datetime.fromtimestamp(timeadj[i]).strftime("%Y/%m/%d")
        protocol = row[4]
        index = row[0]
        tz = row[8]
        matchday = row[5]
        strategy = row[6]
        phase = row[7]
        if tz == 'LHTZ':
            flRFD = round((row[12]-row[10])*10, 1)
            fl150 = round(row[12], 1)
            flpeak = round(row[16], 1)
            blRFD = round((row[20]-row[18])*10, 1)
            bl150 = round(row[20], 1)
            blpeak = round(row[24], 1)
        else:
            blRFD = round((row[12]-row[10])*10, 1)
            bl150 = round(row[12], 1)
            blpeak = round(row[16], 1)
            flRFD = round((row[20]-row[18])*10, 1)
            fl150 = round(row[20], 1)
            flpeak = round(row[24], 1)

        crRFD = round((flRFD + blRFD), 1)
        cr150 = round((fl150 + bl150), 1)
        crpeak = round((flpeak + blpeak), 1)

        j = i + 1
        if j == len(data):
            sessions[f'{protocol}: {date}']['index'].append(index)
            sessions[f'{protocol}: {date}']['TZ'].append(tz)
            sessions[f'{protocol}: {date}']['Protocol'].append(protocol)
            sessions[f'{protocol}: {date}']['Strategy'].append(strategy)
            sessions[f'{protocol}: {date}']['Matchday'].append(matchday)
            sessions[f'{protocol}: {date}']['Phase'].append(phase)
            sessions[f'{protocol}: {date}']['Front leg force at 150ms'].append(fl150)
            sessions[f'{protocol}: {date}']['Front leg RFD 50-150ms'].append(flRFD)
            sessions[f'{protocol}: {date}']['Front leg peak force'].append(flpeak)
            sessions[f'{protocol}: {date}']['Back leg force at 150ms'].append(bl150)
            sessions[f'{protocol}: {date}']['Back leg RFD 50-150ms'].append(blRFD)
            sessions[f'{protocol}: {date}']['Back leg peak force'].append(blpeak)
            sessions[f'{protocol}: {date}']['Crush factor at 150ms'].append(cr150)
            sessions[f'{protocol}: {date}']['Combined RFD 50-150ms'].append(crRFD)
            sessions[f'{protocol}: {date}']['Peak crush factor'].append(crpeak)
            break

        else:
            sessions[f'{protocol}: {date}']['index'].append(index)
            sessions[f'{protocol}: {date}']['TZ'].append(tz)
            sessions[f'{protocol}: {date}']['Protocol'].append(protocol)
            sessions[f'{protocol}: {date}']['Strategy'].append(strategy)
            sessions[f'{protocol}: {date}']['Matchday'].append(matchday)
            sessions[f'{protocol}: {date}']['Phase'].append(phase)
            sessions[f'{protocol}: {date}']['Front leg force at 150ms'].append(fl150)
            sessions[f'{protocol}: {date}']['Front leg RFD 50-150ms'].append(flRFD)
            sessions[f'{protocol}: {date}']['Front leg peak force'].append(flpeak)
            sessions[f'{protocol}: {date}']['Back leg force at 150ms'].append(bl150)
            sessions[f'{protocol}: {date}']['Back leg RFD 50-150ms'].append(blRFD)
            sessions[f'{protocol}: {date}']['Back leg peak force'].append(blpeak)
            sessions[f'{protocol}: {date}']['Crush factor at 150ms'].append(cr150)
            sessions[f'{protocol}: {date}']['Combined RFD 50-150ms'].append(crRFD)
            sessions[f'{protocol}: {date}']['Peak crush factor'].append(crpeak)
            i += 1
            continue

    sessionList = []
    fatigueList, baselineList = [], []
    for key in sessions:
        sessionList.append(key)
    lastFatigue = ''
    lastBaseline = ''
    for session in reversed(sessionList):
        if 'fatigue' in session or 'sprint' in session:
            fatigueList.append(session)
            if lastFatigue == '':
                lastFatigue = session
        else:
            baselineList.append(session)
            if lastBaseline == '':
                lastBaseline = session

    fatigueProtocolList = []
    for session in fatigueList:
        sessionStr = str(session)
        protocolStr = sessionStr[0:len(sessionStr)-12]
        if protocolStr in fatigueProtocolList:
            continue
        else:
            fatigueProtocolList.append(protocolStr)

    baselineProtocolList = []
    for session in baselineList:
        sessionStr = str(session)
        protocolStr = sessionStr[0:len(sessionStr) - 12]
        if protocolStr in baselineProtocolList:
            continue
        else:
            baselineProtocolList.append(protocolStr)



    dates, numTests = [], []
    for sessionName, tests in sessions.items():
        date = str(datetime.strptime(sessionName.split(': ')[1], '%Y/%m/%d'))
        dates.append(date[0:len(date)-9])
        numTests.append(len(tests['index']))

    totalTests = sum(numTests)
    lastTest = dates[len(dates)-1]


    return sessions, lastBaseline, baselineList, baselineProtocolList, lastFatigue, fatigueList, fatigueProtocolList, dates, numTests


def getPlayerTzDict(sessions, lastBaseline):
    data = sessions[lastBaseline]

    # Pull out traces
    tzs = data['TZ']
    pros = data['Protocol']
    strat = data['Strategy']
    match = data['Matchday']
    phase = data['Phase']
    fl150 = data['Front leg force at 150ms']
    flrfd = data['Front leg RFD 50-150ms']
    flpeak = data['Front leg peak force']
    bl150 = data['Back leg force at 150ms']
    blrfd = data['Back leg RFD 50-150ms']
    blpeak = data['Back leg peak force']
    cr150 = data['Crush factor at 150ms']
    crrfd = data['Combined RFD 50-150ms']
    crpeak = data['Peak crush factor']

    # Separate transition zones
    indexL, indexR = [], []
    fl150L, fl150R = [], []
    flRFDL, flRFDR = [], []
    flpeakL, flpeakR = [], []
    bl150L, bl150R = [], []
    blRFDL, blRFDR = [], []
    blpeakL, blpeakR = [], []
    cr150L, cr150R = [], []
    crRFDL, crRFDR = [], []
    crpeakL, crpeakR = [], []
    li, ri = 0, 0
    for i in range(len(tzs)):
        if tzs[i] == 'LHTZ':
            li += 1
            indexL.append(li)
            fl150L.append(fl150[i])
            flRFDL.append(flrfd[i])
            flpeakL.append(flpeak[i])
            bl150L.append(bl150[i])
            blRFDL.append(blrfd[i])
            blpeakL.append(blpeak[i])
            cr150L.append(cr150[i])
            crRFDL.append(crrfd[i])
            crpeakL.append(crpeak[i])
        else:
            ri += 1
            indexR.append(ri)
            fl150R.append(fl150[i])
            flRFDR.append(flrfd[i])
            flpeakR.append(flpeak[i])
            bl150R.append(bl150[i])
            blRFDR.append(blrfd[i])
            blpeakR.append(blpeak[i])
            cr150R.append(cr150[i])
            crRFDR.append(crrfd[i])
            crpeakR.append(crpeak[i])

    # Get max and avg for each metric
    flRFDLmax = [max(flRFDL, default=0)]
    blRFDLmax = [max(blRFDL, default=0)]
    crRFDLmax = [max(crRFDL, default=0)]
    fl150Lmax = [max(fl150L, default=0)]
    bl150Lmax = [max(bl150L, default=0)]
    cr150Lmax = [max(cr150L, default=0)]
    flRFDRmax = [max(flRFDR, default=0)]
    blRFDRmax = [max(blRFDR, default=0)]
    crRFDRmax = [max(crRFDR, default=0)]
    fl150Rmax = [max(fl150R, default=0)]
    bl150Rmax = [max(bl150R, default=0)]
    cr150Rmax = [max(cr150R, default=0)]
    flpeakLmax = [max(flpeakL, default=0)]
    blpeakLmax = [max(blpeakL, default=0)]
    crpeakLmax = [max(crpeakL, default=0)]
    flpeakRmax = [max(flpeakR, default=0)]
    blpeakRmax = [max(blpeakR, default=0)]
    crpeakRmax = [max(crpeakR, default=0)]
    try:
        flRFDLavg = [round(sum(flRFDL) / len(flRFDL), 1)]
    except:
        flRFDLavg = [0]
    try:
        blRFDLavg = [round(sum(blRFDL) / len(blRFDL), 1)]
    except:
        blRFDLavg = [0]
    try:
        crRFDLavg = [round(sum(crRFDL) / len(crRFDL), 1)]
    except:
        crRFDLavg = [0]
    try:
        flRFDRavg = [round(sum(flRFDR) / len(flRFDR), 1)]
    except:
        flRFDRavg = [0]
    try:
        blRFDRavg = [round(sum(blRFDR) / len(blRFDR), 1)]
    except:
        blRFDRavg = [0]
    try:
        crRFDRavg = [round(sum(crRFDR) / len(crRFDR), 1)]
    except:
        crRFDRavg = [0]
    try:
        fl150Lavg = [round(sum(fl150L) / len(fl150L), 1)]
    except:
        fl150Lavg = [0]
    try:
        bl150Lavg = [round(sum(bl150L) / len(bl150L), 1)]
    except:
        bl150Lavg = [0]
    try:
        cr150Lavg = [round(sum(cr150L) / len(cr150L), 1)]
    except:
        cr150Lavg = [0]
    try:
        fl150Ravg = [round(sum(fl150R) / len(fl150R), 1)]
    except:
        fl150Ravg = [0]
    try:
        bl150Ravg = [round(sum(bl150R) / len(bl150R), 1)]
    except:
        bl150Ravg = [0]
    try:
        cr150Ravg = [round(sum(cr150R) / len(cr150R), 1)]
    except:
        cr150Ravg = [0]
    try:
        flpeakLavg = [round(sum(flpeakL) / len(flpeakL), 1)]
    except:
        flpeakLavg = [0]
    try:
        blpeakLavg = [round(sum(blpeakL) / len(blpeakL), 1)]
    except:
        blpeakLavg = [0]
    try:
        crpeakLavg = [round(sum(crpeakL) / len(crpeakL), 1)]
    except:
        crpeakLavg = [0]
    try:
        flpeakRavg = [round(sum(flpeakR) / len(flpeakR), 1)]
    except:
        flpeakRavg = [0]
    try:
        blpeakRavg = [round(sum(blpeakR) / len(blpeakR), 1)]
    except:
        blpeakRavg = [0]
    try:
        crpeakRavg = [round(sum(crpeakR) / len(crpeakR), 1)]
    except:
        crpeakRavg = [0]

    # Create RHTZ and LHTZ dicts
    LHTZ_data = {
        'session': {
            'index': indexL,
            'Front leg RFD 50-150ms': flRFDL,
            'Front leg force at 150ms': fl150L,
            'Front leg peak force': flpeakL,
            'Back leg force at 150ms': bl150L,
            'Back leg RFD 50-150ms': blRFDL,
            'Back leg peak force': blpeakL,
            'Crush factor at 150ms': cr150L,
            'Combined RFD 50-150ms': crRFDL,
            'Peak crush factor': crpeakL
        },
        'max': {
            'index': [1],
            'Front leg force at 150ms': fl150Lmax,
            'Front leg RFD 50-150ms': flRFDLmax,
            'Front leg peak force': flpeakLmax,
            'Back leg force at 150ms': bl150Lmax,
            'Back leg RFD 50-150ms': blRFDLmax,
            'Back leg peak force': blpeakLmax,
            'Crush factor at 150ms': cr150Lmax,
            'Combined RFD 50-150ms': crRFDLmax,
            'Peak crush factor': crpeakLmax
        },
        'avg': {
            'index': [1],
            'Front leg force at 150ms': fl150Lavg,
            'Front leg RFD 50-150ms': flRFDLavg,
            'Front leg peak force': flpeakLavg,
            'Back leg force at 150ms': bl150Lavg,
            'Back leg RFD 50-150ms': blRFDLavg,
            'Back leg peak force': blpeakLavg,
            'Crush factor at 150ms': cr150Lavg,
            'Combined RFD 50-150ms': crRFDLavg,
            'Peak crush factor': crpeakLavg
        }
    }

    RHTZ_data = {
        'session': {
            'index': indexR,
            'Front leg RFD 50-150ms': flRFDR,
            'Front leg force at 150ms': fl150R,
            'Front leg peak force': flpeakR,
            'Back leg force at 150ms': bl150R,
            'Back leg RFD 50-150ms': blRFDR,
            'Back leg peak force': blpeakR,
            'Crush factor at 150ms': cr150R,
            'Combined RFD 50-150ms': crRFDR,
            'Peak crush factor': crpeakR
        },
        'max': {
            'index': [1],
            'Front leg force at 150ms': fl150Rmax,
            'Front leg RFD 50-150ms': flRFDRmax,
            'Front leg peak force': flpeakRmax,
            'Back leg force at 150ms': bl150Rmax,
            'Back leg RFD 50-150ms': blRFDRmax,
            'Back leg peak force': blpeakRmax,
            'Crush factor at 150ms': cr150Rmax,
            'Combined RFD 50-150ms': crRFDRmax,
            'Peak crush factor': crpeakRmax
        },
        'avg': {
            'index': [1],
            'Front leg force at 150ms': fl150Ravg,
            'Front leg RFD 50-150ms': flRFDRavg,
            'Front leg peak force': flpeakRavg,
            'Back leg force at 150ms': bl150Ravg,
            'Back leg RFD 50-150ms': blRFDRavg,
            'Back leg peak force': blpeakRavg,
            'Crush factor at 150ms': cr150Ravg,
            'Combined RFD 50-150ms': crRFDRavg,
            'Peak crush factor': crpeakRavg
        }
    }

    return LHTZ_data, RHTZ_data


def getHistoricalDict(sessions, baselineList):
    baselineData = {}
    li, ri = 0, 0
    for key in reversed(baselineList):
        baselineData[key] = {}
        # Pull out traces
        tzs = sessions[key]['TZ']
        fl150 = sessions[key]['Front leg force at 150ms']
        flpeak = sessions[key]['Front leg peak force']
        bl150 = sessions[key]['Back leg force at 150ms']
        blpeak = sessions[key]['Back leg peak force']
        cr150 = sessions[key]['Crush factor at 150ms']
        crpeak = sessions[key]['Peak crush factor']

        # Separate transition zones
        indexL, indexR = [], []
        fl150L, fl150R = [], []
        flpeakL, flpeakR = [], []
        bl150L, bl150R = [], []
        blpeakL, blpeakR = [], []
        cr150L, cr150R = [], []
        crpeakL, crpeakR = [], []
        for i in range(len(tzs)):
            if tzs[i] == 'LHTZ':
                li += 1
                indexL.append(li)
                fl150L.append(fl150[i])
                flpeakL.append(flpeak[i])
                bl150L.append(bl150[i])
                blpeakL.append(blpeak[i])
                cr150L.append(cr150[i])
                crpeakL.append(crpeak[i])
            else:
                ri += 1
                indexR.append(ri)
                fl150R.append(fl150[i])
                flpeakR.append(flpeak[i])
                bl150R.append(bl150[i])
                blpeakR.append(blpeak[i])
                cr150R.append(cr150[i])
                crpeakR.append(crpeak[i])

        # Get max and avg for each metric
        fl150Lmax = [round(max(fl150L, default=0), 1)]
        bl150Lmax = [round(max(bl150L, default=0), 1)]
        cr150Lmax = [round(max(cr150L, default=0), 1)]
        fl150Rmax = [round(max(fl150R, default=0), 1)]
        bl150Rmax = [round(max(bl150R, default=0), 1)]
        cr150Rmax = [round(max(cr150R, default=0), 1)]
        flpeakLmax = [round(max(flpeakL, default=0), 1)]
        blpeakLmax = [round(max(blpeakL, default=0), 1)]
        crpeakLmax = [round(max(crpeakL, default=0), 1)]
        flpeakRmax = [round(max(flpeakR, default=0), 1)]
        blpeakRmax = [round(max(blpeakR, default=0), 1)]
        crpeakRmax = [round(max(crpeakR, default=0), 1)]
        try:
            fl150Lavg = [round(sum(fl150L) / len(fl150L), 1)]
        except:
            fl150Lavg = [0]
        try:
            bl150Lavg = [round(sum(bl150L) / len(bl150L), 1)]
        except:
            bl150Lavg = [0]
        try:
            cr150Lavg = [round(sum(cr150L) / len(cr150L), 1)]
        except:
            cr150Lavg = [0]
        try:
            fl150Ravg = [round(sum(fl150R) / len(fl150R), 1)]
        except:
            fl150Ravg = [0]
        try:
            bl150Ravg = [round(sum(bl150R) / len(bl150R), 1)]
        except:
            bl150Ravg = [0]
        try:
            cr150Ravg = [round(sum(cr150R) / len(cr150R), 1)]
        except:
            cr150Ravg = [0]
        try:
            flpeakLavg = [round(sum(flpeakL) / len(flpeakL), 1)]
        except:
            flpeakLavg = [0]
        try:
            blpeakLavg = [round(sum(blpeakL) / len(blpeakL), 1)]
        except:
            blpeakLavg = [0]
        try:
            crpeakLavg = [round(sum(crpeakL) / len(crpeakL), 1)]
        except:
            crpeakLavg = [0]
        try:
            flpeakRavg = [round(sum(flpeakR) / len(flpeakR), 1)]
        except:
            flpeakRavg = [0]
        try:
            blpeakRavg = [round(sum(blpeakR) / len(blpeakR), 1)]
        except:
            blpeakRavg = [0]
        try:
            crpeakRavg = [round(sum(crpeakR) / len(crpeakR), 1)]
        except:
            crpeakRavg = [0]

        LHTZ_data = {
            'max': {
                'index': indexL,
                'Front leg force at 150ms': fl150Lmax,
                'Front leg peak force': flpeakLmax,
                'Back leg force at 150ms': bl150Lmax,
                'Back leg peak force': blpeakLmax,
                'Crush factor at 150ms': cr150Lmax,
                'Peak crush factor': crpeakLmax
            },
            'avg': {
                'index': indexL,
                'Front leg force at 150ms': fl150Lavg,
                'Front leg peak force': flpeakLavg,
                'Back leg force at 150ms': bl150Lavg,
                'Back leg peak force': blpeakLavg,
                'Crush factor at 150ms': cr150Lavg,
                'Peak crush factor': crpeakLavg
            }
        }

        RHTZ_data = {
            'max': {
                'index': indexR,
                'Front leg force at 150ms': fl150Rmax,
                'Front leg peak force': flpeakRmax,
                'Back leg force at 150ms': bl150Rmax,
                'Back leg peak force': blpeakRmax,
                'Crush factor at 150ms': cr150Rmax,
                'Peak crush factor': crpeakRmax
            },
            'avg': {
                'index': indexR,
                'Front leg force at 150ms': fl150Ravg,
                'Front leg peak force': flpeakRavg,
                'Back leg force at 150ms': bl150Ravg,
                'Back leg peak force': blpeakRavg,
                'Crush factor at 150ms': cr150Ravg,
                'Peak crush factor': crpeakRavg
            }
        }

        baselineData[key]['LHTZ'] = LHTZ_data
        baselineData[key]['RHTZ'] = RHTZ_data

    return baselineData


def getSquadDict(squadTestData, Protocol):
    squadData = []
    for i in squadTestData:
        squadData.append((i.id, i.Org, i.User, i.Timestamp, i.Protocol, i.TZ,
                          i.Left0ms, i.Left50ms, i.Left100ms,
                          i.Left150ms, i.Left200ms, i.Left250ms,
                          i.Left300ms, i.Leftpeak, i.Right0ms,
                          i.Right50ms, i.Right100ms, i.Right150ms,
                          i.Right200ms, i.Right250ms, i.Right300ms,
                          i.Rightpeak))

    timestamps = [row[3] for row in squadData]
    minute = 60
    timeadj = []
    j = 0
    for t in range(len(timestamps)):
        timeadj.append(round(timestamps[t] + (minute * j)))
        j += 1
    i = 0
    squadSessions = {}
    for row in squadData:
        user = row[2]
        date = datetime.fromtimestamp(timeadj[i]).strftime("%Y/%m/%d")
        protocol = row[4]

        squadSessions[f'{user} : {protocol} : {date}'] = {}
        squadSessions[f'{user} : {protocol} : {date}']['index'] = []
        squadSessions[f'{user} : {protocol} : {date}']['TZ'] = []
        squadSessions[f'{user} : {protocol} : {date}']['Front leg force at 150ms'] = []
        squadSessions[f'{user} : {protocol} : {date}']['Front leg peak force'] = []
        squadSessions[f'{user} : {protocol} : {date}']['Back leg force at 150ms'] = []
        squadSessions[f'{user} : {protocol} : {date}']['Back leg peak force'] = []
        squadSessions[f'{user} : {protocol} : {date}']['Crush factor at 150ms'] = []
        squadSessions[f'{user} : {protocol} : {date}']['Peak crush factor'] = []
        i += 1
    i = 0
    for row in squadData:
        user = row[2]
        date = datetime.fromtimestamp(timeadj[i]).strftime("%Y/%m/%d")
        protocol = row[4]
        index = row[0]
        tz = row[5]
        if tz == 'LHTZ':
            fl150 = round(row[9], 1)
            flpeak = round(row[13], 1)
            bl150 = round(row[17], 1)
            blpeak = round(row[21], 1)
        else:
            bl150 = round(row[9], 1)
            blpeak = round(row[13], 1)
            fl150 = round(row[17], 1)
            flpeak = round(row[21], 1)

        cr150 = round((fl150 + bl150), 1)
        crpeak = round((flpeak + blpeak), 1)

        squadSessions[f'{user} : {protocol} : {date}']['index'].append(index)
        squadSessions[f'{user} : {protocol} : {date}']['TZ'].append(tz)
        squadSessions[f'{user} : {protocol} : {date}']['Front leg force at 150ms'].append(fl150)
        squadSessions[f'{user} : {protocol} : {date}']['Front leg peak force'].append(flpeak)
        squadSessions[f'{user} : {protocol} : {date}']['Back leg force at 150ms'].append(bl150)
        squadSessions[f'{user} : {protocol} : {date}']['Back leg peak force'].append(blpeak)
        squadSessions[f'{user} : {protocol} : {date}']['Crush factor at 150ms'].append(cr150)
        squadSessions[f'{user} : {protocol} : {date}']['Peak crush factor'].append(crpeak)
        i += 1

    selectedProtocol = f': {Protocol} :'
    # Filter the squadSessions dictionary to find all keys containing 'Baseline'
    proSessions = {k: v for k, v in squadSessions.items() if selectedProtocol in k}

    keys = [key for key, data in proSessions.items()]
    filteredKeys = []
    names = []
    for key in keys[::]:
        name = key.split(' : ')[0]
        date = key.split(' : ')[2]
        if f'{name} : {date}' in keys:
            continue
        else:
            filteredKeys.append(key)
        names.append(name)

    filteredSessions = {k: v for k, v in proSessions.items() if k in filteredKeys}
    squadProData = {}
    squadProDateData = {}
    testDates = []
    li, ri = 0, 0
    for key in filteredKeys:
        user = key.split(' : ')[0]
        date = key.split(' : ')[2]
        testDates.append(date)
        squadProData[user] = {}
        squadProDateData[date] = {}
    for key in filteredKeys:
        user = key.split(' : ')[0]
        date = key.split(' : ')[2]
        squadProDateData[date][user] = {}
        # Pull out traces
        tzs = filteredSessions[key]['TZ']
        fl150 = filteredSessions[key]['Front leg force at 150ms']
        flpeak = filteredSessions[key]['Front leg peak force']
        bl150 = filteredSessions[key]['Back leg force at 150ms']
        blpeak = filteredSessions[key]['Back leg peak force']
        cr150 = filteredSessions[key]['Crush factor at 150ms']
        crpeak = filteredSessions[key]['Peak crush factor']

        # Separate transition zones
        indexL, indexR = [], []
        fl150L, fl150R = [], []
        flpeakL, flpeakR = [], []
        bl150L, bl150R = [], []
        blpeakL, blpeakR = [], []
        cr150L, cr150R = [], []
        crpeakL, crpeakR = [], []
        for i in range(len(tzs)):
            if tzs[i] == 'LHTZ':
                li += 1
                indexL.append(li)
                fl150L.append(fl150[i])
                flpeakL.append(flpeak[i])
                bl150L.append(bl150[i])
                blpeakL.append(blpeak[i])
                cr150L.append(cr150[i])
                crpeakL.append(crpeak[i])
            else:
                ri += 1
                indexR.append(ri)
                fl150R.append(fl150[i])
                flpeakR.append(flpeak[i])
                bl150R.append(bl150[i])
                blpeakR.append(blpeak[i])
                cr150R.append(cr150[i])
                crpeakR.append(crpeak[i])

        # Get max and avg for each metric
        fl150Lmax = [round(max(fl150L, default=0), 1)]
        bl150Lmax = [round(max(bl150L, default=0), 1)]
        cr150Lmax = [round(max(cr150L, default=0), 1)]
        fl150Rmax = [round(max(fl150R, default=0), 1)]
        bl150Rmax = [round(max(bl150R, default=0), 1)]
        cr150Rmax = [round(max(cr150R, default=0), 1)]
        flpeakLmax = [round(max(flpeakL, default=0), 1)]
        blpeakLmax = [round(max(blpeakL, default=0), 1)]
        crpeakLmax = [round(max(crpeakL, default=0), 1)]
        flpeakRmax = [round(max(flpeakR, default=0), 1)]
        blpeakRmax = [round(max(blpeakR, default=0), 1)]
        crpeakRmax = [round(max(crpeakR, default=0), 1)]
        try:
            fl150Lavg = [round(sum(fl150L) / len(fl150L), 1)]
        except:
            fl150Lavg = [0]
        try:
            bl150Lavg = [round(sum(bl150L) / len(bl150L), 1)]
        except:
            bl150Lavg = [0]
        try:
            cr150Lavg = [round(sum(cr150L) / len(cr150L), 1)]
        except:
            cr150Lavg = [0]
        try:
            fl150Ravg = [round(sum(fl150R) / len(fl150R), 1)]
        except:
            fl150Ravg = [0]
        try:
            bl150Ravg = [round(sum(bl150R) / len(bl150R), 1)]
        except:
            bl150Ravg = [0]
        try:
            cr150Ravg = [round(sum(cr150R) / len(cr150R), 1)]
        except:
            cr150Ravg = [0]
        try:
            flpeakLavg = [round(sum(flpeakL) / len(flpeakL), 1)]
        except:
            flpeakLavg = [0]
        try:
            blpeakLavg = [round(sum(blpeakL) / len(blpeakL), 1)]
        except:
            blpeakLavg = [0]
        try:
            crpeakLavg = [round(sum(crpeakL) / len(crpeakL), 1)]
        except:
            crpeakLavg = [0]
        try:
            flpeakRavg = [round(sum(flpeakR) / len(flpeakR), 1)]
        except:
            flpeakRavg = [0]
        try:
            blpeakRavg = [round(sum(blpeakR) / len(blpeakR), 1)]
        except:
            blpeakRavg = [0]
        try:
            crpeakRavg = [round(sum(crpeakR) / len(crpeakR), 1)]
        except:
            crpeakRavg = [0]

        LHTZ_data = {
            'max': {
                'index': indexL,
                'Peak crush factor': crpeakLmax,
                'Front leg peak force': flpeakLmax,
                'Back leg peak force': blpeakLmax,
                'Crush factor at 150ms': cr150Lmax,
                'Front leg force at 150ms': fl150Lmax,
                'Back leg force at 150ms': bl150Lmax,

            },
            'avg': {
                'index': indexL,
                'Peak crush factor': crpeakLavg,
                'Front leg peak force': flpeakLavg,
                'Back leg peak force': blpeakLavg,
                'Crush factor at 150ms': cr150Lavg,
                'Front leg force at 150ms': fl150Lavg,
                'Back leg force at 150ms': bl150Lavg,

            }
        }

        RHTZ_data = {
            'max': {
                'index': indexR,
                'Peak crush factor': crpeakRmax,
                'Front leg peak force': flpeakRmax,
                'Back leg peak force': blpeakRmax,
                'Crush factor at 150ms': cr150Rmax,
                'Front leg force at 150ms': fl150Rmax,
                'Back leg force at 150ms': bl150Rmax,

            },
            'avg': {
                'index': indexR,
                'Peak crush factor': crpeakRavg,
                'Front leg peak force': flpeakRavg,
                'Back leg peak force': blpeakRavg,
                'Crush factor at 150ms': cr150Ravg,
                'Front leg force at 150ms': fl150Ravg,
                'Back leg force at 150ms': bl150Ravg,

            }
        }

        squadProData[user]['LHTZ'] = LHTZ_data
        squadProData[user]['RHTZ'] = RHTZ_data

        squadProDateData[date][user]['LHTZ'] = LHTZ_data
        squadProDateData[date][user]['RHTZ'] = RHTZ_data

    test_dates = list(set(testDates))

    dates, numTests = [], []
    for sessionName, tests in filteredSessions.items():
        date = datetime.strptime(sessionName.split(': ')[2], '%Y/%m/%d')
        dates.append(date)
        numTests.append(len(tests['index']))

    minDate = dates[0]
    maxDate = datetime.now()
    allDates = [datetime.strftime(minDate + timedelta(days=d), '%Y/%m/%d') for d in range((maxDate - minDate).days + 1)]
    allTests = []
    for day in allDates:
        dayobj = datetime.strptime(day, '%Y/%m/%d')
        if dayobj in dates:
            allTests.append(numTests[dates.index(dayobj)])
        else:
            allTests.append(0)

    return squadProData, squadProDateData, allTests, allDates, test_dates, filteredKeys


from statistics import mean


def get_scores(rows):
    # create a dictionary to store the scores for each protocol
    scores = {}

    # iterate through the rows of data
    for row in rows:
        # get the protocol name and score
        protocol = row.Protocol
        tz = row.TZ
        leftScore = row.Leftpeak
        rightScore = row.Rightpeak

        # if the protocol is not in the dictionary, add it and create a new list for the scores
        if protocol not in scores:
            scores[protocol] = {}
        if tz not in scores[protocol]:
            scores[protocol][tz] = {}
            scores[protocol][tz]['Left leg'] = []
            scores[protocol][tz]['Right leg'] = []

            # add the score to the list for the protocol
        scores[protocol][tz]['Left leg'].append(leftScore)
        scores[protocol][tz]['Right leg'].append(rightScore)
    # create a new dictionary to store the best, worst, and average scores for each protocol
    results = {}

    for protocol, tzs in scores.items():
        if protocol not in results:
            results[protocol] = {}

        for tz, legs in tzs.items():
            results[protocol][tz] = {}
            for leg, score_list in legs.items():
                # Calculate best, worst, and average scores for the protocol tz and leg
                best = max(score_list)
                worst = min(score_list)
                average = mean(score_list)
                # Add the results to the dictionary
                results[protocol][tz][leg] = (best, worst, average)

    # return the results
    return results


def generate_report(results):
    # create the table header
    report = """
  <table class="table table-hover">
    <tr class="table-secondary">
      <th>Protocol</th>
      <th>Transition zone</th>
      <th>Leg</th>
      <th>Best Score (kg)</th>
      <th>Worst Score (kg)</th>
      <th>Average Score (kg)</th>
    </tr>
  """

    # create a string to hold the final report
    final_report = report

    # iterate through the results and add a row for each protocol and time zone
    for protocol, tzs in results.items():
        for tz, legs in tzs.items():
            for leg, tup in legs.items():
                # create a row for the protocol and time zone
                row = """
            <tr>
              <td>{protocol}</td>
              <td>{tz}</td>
              <td>{leg}</td>
              <td>{best}</td>
              <td>{worst}</td>
              <td>{average}</td>
            </tr>
            """
                final_report += row.format(protocol=protocol, tz=tz, leg=leg, best=round(tup[0], 1),
                                           worst=round(tup[1], 1), average=round(tup[2], 1))

    # close the table
    final_report += "</table>"

    # return the final report
    return final_report


def getSessions(sessions):
    playerSessions = {}
    for key in sessions:
        data = sessions[key]
        playerSessions[key] = {}

        # Pull out traces
        tzs = data['TZ']
        pros = data['Protocol']
        strat = data['Strategy']
        match = data['Matchday']
        phase = data['Phase']
        fl150 = data['Front leg force at 150ms']
        flrfd = data['Front leg RFD 50-150ms']
        flpeak = data['Front leg peak force']
        bl150 = data['Back leg force at 150ms']
        blrfd = data['Back leg RFD 50-150ms']
        blpeak = data['Back leg peak force']
        cr150 = data['Crush factor at 150ms']
        crrfd = data['Combined RFD 50-150ms']
        crpeak = data['Peak crush factor']

        # Separate transition zones
        indexL, indexR = [], []
        stratL, stratR = [], []
        proL, proR = [], []
        matchL, matchR = [], []
        phaseL, phaseR = [], []
        fl150L, fl150R = [], []
        flRFDL, flRFDR = [], []
        flpeakL, flpeakR = [], []
        bl150L, bl150R = [], []
        blRFDL, blRFDR = [], []
        blpeakL, blpeakR = [], []
        cr150L, cr150R = [], []
        crRFDL, crRFDR = [], []
        crpeakL, crpeakR = [], []
        li, ri = 0, 0
        for i in range(len(tzs)):
            if tzs[i] == 'LHTZ':
                li += 1
                stratL.append(strat[i])
                proL.append(pros[i])
                matchL.append(match[i])
                phaseL.append(phase[i])
                indexL.append(li)
                fl150L.append(fl150[i])
                flRFDL.append(flrfd[i])
                flpeakL.append(flpeak[i])
                bl150L.append(bl150[i])
                blRFDL.append(blrfd[i])
                blpeakL.append(blpeak[i])
                cr150L.append(cr150[i])
                crRFDL.append(crrfd[i])
                crpeakL.append(crpeak[i])
            else:
                ri += 1
                stratR.append(strat[i])
                proR.append(pros[i])
                matchR.append(match[i])
                phaseR.append(phase[i])
                indexR.append(ri)
                fl150R.append(fl150[i])
                flRFDR.append(flrfd[i])
                flpeakR.append(flpeak[i])
                bl150R.append(bl150[i])
                blRFDR.append(blrfd[i])
                blpeakR.append(blpeak[i])
                cr150R.append(cr150[i])
                crRFDR.append(crrfd[i])
                crpeakR.append(crpeak[i])

        # Get max and avg for each metric
        flRFDLmax = [max(flRFDL, default=0)]
        blRFDLmax = [max(blRFDL, default=0)]
        crRFDLmax = [max(crRFDL, default=0)]
        fl150Lmax = [max(fl150L, default=0)]
        bl150Lmax = [max(bl150L, default=0)]
        cr150Lmax = [max(cr150L, default=0)]
        flRFDRmax = [max(flRFDR, default=0)]
        blRFDRmax = [max(blRFDR, default=0)]
        crRFDRmax = [max(crRFDR, default=0)]
        fl150Rmax = [max(fl150R, default=0)]
        bl150Rmax = [max(bl150R, default=0)]
        cr150Rmax = [max(cr150R, default=0)]
        flpeakLmax = [max(flpeakL, default=0)]
        blpeakLmax = [max(blpeakL, default=0)]
        crpeakLmax = [max(crpeakL, default=0)]
        flpeakRmax = [max(flpeakR, default=0)]
        blpeakRmax = [max(blpeakR, default=0)]
        crpeakRmax = [max(crpeakR, default=0)]
        try:
            flRFDLavg = [round(sum(flRFDL) / len(flRFDL), 1)]
        except:
            flRFDLavg = [0]
        try:
            blRFDLavg = [round(sum(blRFDL) / len(blRFDL), 1)]
        except:
            blRFDLavg = [0]
        try:
            crRFDLavg = [round(sum(crRFDL) / len(crRFDL), 1)]
        except:
            crRFDLavg = [0]
        try:
            flRFDRavg = [round(sum(flRFDR) / len(flRFDR), 1)]
        except:
            flRFDRavg = [0]
        try:
            blRFDRavg = [round(sum(blRFDR) / len(blRFDR), 1)]
        except:
            blRFDRavg = [0]
        try:
            crRFDRavg = [round(sum(crRFDR) / len(crRFDR), 1)]
        except:
            crRFDRavg = [0]
        try:
            fl150Lavg = [round(sum(fl150L) / len(fl150L), 1)]
        except:
            fl150Lavg = [0]
        try:
            bl150Lavg = [round(sum(bl150L) / len(bl150L), 1)]
        except:
            bl150Lavg = [0]
        try:
            cr150Lavg = [round(sum(cr150L) / len(cr150L), 1)]
        except:
            cr150Lavg = [0]
        try:
            fl150Ravg = [round(sum(fl150R) / len(fl150R), 1)]
        except:
            fl150Ravg = [0]
        try:
            bl150Ravg = [round(sum(bl150R) / len(bl150R), 1)]
        except:
            bl150Ravg = [0]
        try:
            cr150Ravg = [round(sum(cr150R) / len(cr150R), 1)]
        except:
            cr150Ravg = [0]
        try:
            flpeakLavg = [round(sum(flpeakL) / len(flpeakL), 1)]
        except:
            flpeakLavg = [0]
        try:
            blpeakLavg = [round(sum(blpeakL) / len(blpeakL), 1)]
        except:
            blpeakLavg = [0]
        try:
            crpeakLavg = [round(sum(crpeakL) / len(crpeakL), 1)]
        except:
            crpeakLavg = [0]
        try:
            flpeakRavg = [round(sum(flpeakR) / len(flpeakR), 1)]
        except:
            flpeakRavg = [0]
        try:
            blpeakRavg = [round(sum(blpeakR) / len(blpeakR), 1)]
        except:
            blpeakRavg = [0]
        try:
            crpeakRavg = [round(sum(crpeakR) / len(crpeakR), 1)]
        except:
            crpeakRavg = [0]

        # Create RHTZ and LHTZ dicts
        LHTZ_data = {
            'session': {
                'index': indexL,
                'Protocol': proL,
                'Strategy': stratL,
                'Matchday': matchL,
                'Phase': phaseL,
                'Front leg RFD 50-150ms': flRFDL,
                'Front leg force at 150ms': fl150L,
                'Front leg peak force': flpeakL,
                'Back leg force at 150ms': bl150L,
                'Back leg RFD 50-150ms': blRFDL,
                'Back leg peak force': blpeakL,
                'Crush factor at 150ms': cr150L,
                'Combined RFD 50-150ms': crRFDL,
                'Peak crush factor': crpeakL
            },
            'max': {
                'index': [1],
                'Front leg force at 150ms': fl150Lmax,
                'Front leg RFD 50-150ms': flRFDLmax,
                'Front leg peak force': flpeakLmax,
                'Back leg force at 150ms': bl150Lmax,
                'Back leg RFD 50-150ms': blRFDLmax,
                'Back leg peak force': blpeakLmax,
                'Crush factor at 150ms': cr150Lmax,
                'Combined RFD 50-150ms': crRFDLmax,
                'Peak crush factor': crpeakLmax
            },
            'avg': {
                'index': [1],
                'Front leg force at 150ms': fl150Lavg,
                'Front leg RFD 50-150ms': flRFDLavg,
                'Front leg peak force': flpeakLavg,
                'Back leg force at 150ms': bl150Lavg,
                'Back leg RFD 50-150ms': blRFDLavg,
                'Back leg peak force': blpeakLavg,
                'Crush factor at 150ms': cr150Lavg,
                'Combined RFD 50-150ms': crRFDLavg,
                'Peak crush factor': crpeakLavg
            }
        }

        RHTZ_data = {
            'session': {
                'index': indexR,
                'Protocol': proR,
                'Strategy': stratR,
                'Matchday': matchR,
                'Phase': phaseR,
                'Front leg RFD 50-150ms': flRFDR,
                'Front leg force at 150ms': fl150R,
                'Front leg peak force': flpeakR,
                'Back leg force at 150ms': bl150R,
                'Back leg RFD 50-150ms': blRFDR,
                'Back leg peak force': blpeakR,
                'Crush factor at 150ms': cr150R,
                'Combined RFD 50-150ms': crRFDR,
                'Peak crush factor': crpeakR
            },
            'max': {
                'index': [1],
                'Front leg force at 150ms': fl150Rmax,
                'Front leg RFD 50-150ms': flRFDRmax,
                'Front leg peak force': flpeakRmax,
                'Back leg force at 150ms': bl150Rmax,
                'Back leg RFD 50-150ms': blRFDRmax,
                'Back leg peak force': blpeakRmax,
                'Crush factor at 150ms': cr150Rmax,
                'Combined RFD 50-150ms': crRFDRmax,
                'Peak crush factor': crpeakRmax
            },
            'avg': {
                'index': [1],
                'Front leg force at 150ms': fl150Ravg,
                'Front leg RFD 50-150ms': flRFDRavg,
                'Front leg peak force': flpeakRavg,
                'Back leg force at 150ms': bl150Ravg,
                'Back leg RFD 50-150ms': blRFDRavg,
                'Back leg peak force': blpeakRavg,
                'Crush factor at 150ms': cr150Ravg,
                'Combined RFD 50-150ms': crRFDRavg,
                'Peak crush factor': crpeakRavg
            }
        }

        playerSessions[key]['LHTZ'] = LHTZ_data
        playerSessions[key]['RHTZ'] = RHTZ_data

    # Calculate asymmetry for each key in playerSessions
    for key, value in playerSessions.items():
        lhtz_data = value['LHTZ']['session']
        rhtz_data = value['RHTZ']['session']
        asymmetry = {
            "avg": {},
            "max": {},
            "session": {}
        }
        for metric in lhtz_data.keys():
            if metric != 'index' and metric != 'Protocol' and metric != 'Strategy' and metric != 'Matchday' and metric != 'Phase':
                lhtz_values = lhtz_data[metric]
                rhtz_values = rhtz_data[metric]
                asymmetry_values = []
                for lhtz_val, rhtz_val in zip(lhtz_values, rhtz_values):
                    try:
                        asymmetry_val = round(((rhtz_val - lhtz_val) / rhtz_val) * 100, 2)
                    except:
                        asymmetry_val = 100
                    asymmetry_values.append(asymmetry_val)
                try:
                    asymmetry["avg"][metric] = [round(sum(asymmetry_values) / len(asymmetry_values), 2)]
                except:
                    asymmetry["avg"][metric] = 0
                asymmetry["max"][metric] = [max(asymmetry_values, default=0)]
                asymmetry["session"][metric] = asymmetry_values
        playerSessions[key]['Asymmetry'] = asymmetry

    return playerSessions



def getSessionTable(playerSessions):
    tableList = []
    for session in playerSessions:

        lhtzSession = playerSessions[session]['LHTZ']['session'];
        rhtzSession = playerSessions[session]['RHTZ']['session'];
        asymmetrySession = playerSessions[session]['Asymmetry']['session'];

        report = '''
            <table class="table table-hover" >
              <tr class="table-secondary">
                <td colspan="4" style="font-size: 0.75rem">Test conditions</td>
                <td colspan="9" style="font-size: 0.75rem">LHTZ</td>
                <td colspan="9" style="font-size: 0.75rem">RHTZ</td>
                <td colspan="9" style="font-size: 0.75rem">Asymmetry</td>
              </tr>
              <tr>
                <td>Index</td>
                <td>Matchday</td>
                <td>Strategy</td>
                <td>Phase</td>
                <td>FL peak force (kg)</td>
                <td>BL peak force (kg)</td>
                <td>Peak crush factor (kg)</td>
                <td>FL force at 150ms (kg)</td>
                <td>BL force at 150ms (kg)</td>
                <td>Crush factor at 150ms (kg)</td>
                <td>FL RFD (kg/s)</td>
                <td>BL RFD (kg/s)</td>
                <td>Combined RFD 50-150ms (kg/s)</td>
                <td>FL peak force (kg)</td>
                <td>BL peak force (kg)</td>
                <td>Peak crush factor (kg)</td>
                <td>FL force at 150ms (kg)</td>
                <td>BL force at 150ms (kg)</td>
                <td>Crush factor at 150ms (kg)</td>
                <td>FL (kg/s)</td>
                <td>BL RFD (kg/s)</td>
                <td>Combined RFD (kg/s)</td>
                <td>FL peak force (%)</td>
                <td>BL peak force (%)</td>
                <td>Peak crush factor (%)</td>
                <td>FL force at 150ms (%)</td>
                <td>BL force at 150ms (%)</td>
                <td>Crush factor at 150ms (%)</td>
                <td>FL RFD (%)</td>
                <td>BL RFD (%)</td>
                <td>Combined RFD (%)</td>
              </tr>
        '''

        final_report = report
        for test in range(len(playerSessions[session]['LHTZ']['session']['index'])):

            row = """
            <tr>
                <td>{index}</td>
                <td>{strategy}</td>
                <td>{matchday}</td>
                <td>{phase}</td>
                <td>{LFP}</td>
                <td>{LBP}</td>
                <td>{LCP}</td>
                <td>{LF150}</td>
                <td>{LB150}</td>
                <td>{LC150}</td>
                <td>{LFrfd}</td>
                <td>{LBrfd}</td>
                <td>{LCrfd}</td>
                <td>{RFP}</td>
                <td>{RBP}</td>
                <td>{RCP}</td>
                <td>{RF150}</td>
                <td>{RB150}</td>
                <td>{RC150}</td>
                <td>{RFrfd}</td>
                <td>{RBrfd}</td>
                <td>{RCrfd}</td>
                <td>{AFP}</td>
                <td>{ABP}</td>
                <td>{ACP}</td>
                <td>{AF150}</td>
                <td>{AB150}</td>
                <td>{AC150}</td>
                <td>{AFrfd}</td>
                <td>{ABrfd}</td>
                <td>{ACrfd}</td>
            </tr>
            """

            final_report += row.format(index=lhtzSession['index'][test],
                                       strategy=lhtzSession['Strategy'][test],
                                       matchday=lhtzSession['Matchday'][test],
                                       phase=lhtzSession['Phase'][test],
                                       LFP=lhtzSession['Front leg peak force'][test],
                                       LBP=lhtzSession['Back leg peak force'][test],
                                       LCP=lhtzSession['Peak crush factor'][test],
                                       LF150=lhtzSession['Front leg force at 150ms'][test],
                                       LB150=lhtzSession['Back leg force at 150ms'][test],
                                       LC150=lhtzSession['Crush factor at 150ms'][test],
                                       LFrfd=lhtzSession['Front leg RFD 50-150ms'][test],
                                       LBrfd=lhtzSession['Back leg RFD 50-150ms'][test],
                                       LCrfd=lhtzSession['Combined RFD 50-150ms'][test],
                                       RFP=rhtzSession['Front leg peak force'][test],
                                       RBP=rhtzSession['Back leg peak force'][test],
                                       RCP=rhtzSession['Peak crush factor'][test],
                                       RF150=rhtzSession['Front leg force at 150ms'][test],
                                       RB150=rhtzSession['Back leg force at 150ms'][test],
                                       RC150=rhtzSession['Crush factor at 150ms'][test],
                                       RFrfd=rhtzSession['Front leg RFD 50-150ms'][test],
                                       RBrfd=rhtzSession['Back leg RFD 50-150ms'][test],
                                       RCrfd=rhtzSession['Combined RFD 50-150ms'][test],
                                       AFP=asymmetrySession['Front leg peak force'][test],
                                       ABP=asymmetrySession['Back leg peak force'][test],
                                       ACP=asymmetrySession['Peak crush factor'][test],
                                       AF150=asymmetrySession['Front leg force at 150ms'][test],
                                       AB150=asymmetrySession['Back leg force at 150ms'][test],
                                       AC150=asymmetrySession['Crush factor at 150ms'][test],
                                       AFrfd=asymmetrySession['Front leg RFD 50-150ms'][test],
                                       ABrfd=asymmetrySession['Back leg RFD 50-150ms'][test],
                                       ACrfd=asymmetrySession['Combined RFD 50-150ms'][test],
                                       )
        final_report+= "</table>"

        tableList.append(final_report)

    return tableList

def getPlayerTags(playerSessions):

    proList = []
    dayList = []
    stratList = []
    phaseList = []

    for session in playerSessions:
        for i in range(len(playerSessions[session]['LHTZ']['session']['Protocol'])):
            pro = playerSessions[session]['LHTZ']['session']['Protocol'][i]
            if pro not in proList:
                proList.append(pro)
            day = playerSessions[session]['LHTZ']['session']['Matchday'][i]
            if day not in dayList:
                dayList.append(day)
            strat = playerSessions[session]['LHTZ']['session']['Strategy'][i]
            if strat not in stratList:
                stratList.append(strat)
            phase = playerSessions[session]['LHTZ']['session']['Phase'][i]
            if phase not in phaseList:
                phaseList.append(phase)

    playerTags = {
        'Protocol': proList,
        'Strategy': stratList,
        'Matchday': dayList,
        'Phase': phaseList
    }

    return playerTags
