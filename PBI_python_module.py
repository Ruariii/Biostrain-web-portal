import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import time


####################################################################################################

def getPlayerDict(playerTestData):
    # get dataArray - all tests
    data = []
    for i in playerTestData:
        data.append((i.id, i.Org, i.User, i.Timestamp, i.Protocol, i.TZ,
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
        sessions[f'{protocol}: {date}']['Front leg force at 150ms'] = []
        sessions[f'{protocol}: {date}']['Front leg peak force'] = []
        sessions[f'{protocol}: {date}']['Back leg force at 150ms'] = []
        sessions[f'{protocol}: {date}']['Back leg peak force'] = []
        sessions[f'{protocol}: {date}']['Crush factor at 150ms'] = []
        sessions[f'{protocol}: {date}']['Peak crush factor'] = []
        i += 1

    i = 0
    for row in data:
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

        j = i + 1
        if j == len(data):
            sessions[f'{protocol}: {date}']['index'].append(index)
            sessions[f'{protocol}: {date}']['TZ'].append(tz)
            sessions[f'{protocol}: {date}']['Front leg force at 150ms'].append(fl150)
            sessions[f'{protocol}: {date}']['Front leg peak force'].append(flpeak)
            sessions[f'{protocol}: {date}']['Back leg force at 150ms'].append(bl150)
            sessions[f'{protocol}: {date}']['Back leg peak force'].append(blpeak)
            sessions[f'{protocol}: {date}']['Crush factor at 150ms'].append(cr150)
            sessions[f'{protocol}: {date}']['Peak crush factor'].append(crpeak)
            break

        else:
            sessions[f'{protocol}: {date}']['index'].append(index)
            sessions[f'{protocol}: {date}']['TZ'].append(tz)
            sessions[f'{protocol}: {date}']['Front leg force at 150ms'].append(fl150)
            sessions[f'{protocol}: {date}']['Front leg peak force'].append(flpeak)
            sessions[f'{protocol}: {date}']['Back leg force at 150ms'].append(bl150)
            sessions[f'{protocol}: {date}']['Back leg peak force'].append(blpeak)
            sessions[f'{protocol}: {date}']['Crush factor at 150ms'].append(cr150)
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

    dates, numTests = [], []
    for sessionName, tests in sessions.items():
        date = datetime.strptime(sessionName.split(': ')[1], '%Y/%m/%d')
        dates.append(date)
        numTests.append(len(tests['index']))

    try:
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
    except:
        allTests, allDates = [], []

    try:
        last30dates = allDates[len(allDates)-31: len(allDates)-1]
        last30tests = allTests[len(allTests) - 31: len(allTests) - 1]
    except:
        last30dates = allDates
        last30tests = allTests

    return sessions, lastBaseline, baselineList, lastFatigue, fatigueList, last30dates, last30tests


def getPlayerTzDict(sessions, lastBaseline):
    data = sessions[lastBaseline]

    # Pull out traces
    tzs = data['TZ']
    fl150 = data['Front leg force at 150ms']
    flpeak = data['Front leg peak force']
    bl150 = data['Back leg force at 150ms']
    blpeak = data['Back leg peak force']
    cr150 = data['Crush factor at 150ms']
    crpeak = data['Peak crush factor']

    # Separate transition zones
    indexL, indexR = [], []
    fl150L, fl150R = [], []
    flpeakL, flpeakR = [], []
    bl150L, bl150R = [], []
    blpeakL, blpeakR = [], []
    cr150L, cr150R = [], []
    crpeakL, crpeakR = [], []
    li, ri = 0, 0
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
    fl150Lmax = [max(fl150L, default=0)]
    bl150Lmax = [max(bl150L, default=0)]
    cr150Lmax = [max(cr150L, default=0)]
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
            'Front leg force at 150ms': fl150L,
            'Front leg peak force': flpeakL,
            'Back leg force at 150ms': bl150L,
            'Back leg peak force': blpeakL,
            'Crush factor at 150ms': cr150L,
            'Peak crush factor': crpeakL
        },
        'max': {
            'index': [1],
            'Front leg force at 150ms': fl150Lmax,
            'Front leg peak force': flpeakLmax,
            'Back leg force at 150ms': bl150Lmax,
            'Back leg peak force': blpeakLmax,
            'Crush factor at 150ms': cr150Lmax,
            'Peak crush factor': crpeakLmax
        },
        'avg': {
            'index': [1],
            'Front leg force at 150ms': fl150Lavg,
            'Front leg peak force': flpeakLavg,
            'Back leg force at 150ms': bl150Lavg,
            'Back leg peak force': blpeakLavg,
            'Crush factor at 150ms': cr150Lavg,
            'Peak crush factor': crpeakLavg
        }
    }

    RHTZ_data = {
        'session': {
            'index': indexR,
            'Front leg force at 150ms': fl150R,
            'Front leg peak force': flpeakR,
            'Back leg force at 150ms': bl150R,
            'Back leg peak force': blpeakR,
            'Crush factor at 150ms': cr150R,
            'Peak crush factor': crpeakR
        },
        'max': {
            'index': [2],
            'Front leg force at 150ms': fl150Rmax,
            'Front leg peak force': flpeakRmax,
            'Back leg force at 150ms': bl150Rmax,
            'Back leg peak force': blpeakRmax,
            'Crush factor at 150ms': cr150Rmax,
            'Peak crush factor': crpeakRmax
        },
        'avg': {
            'index': [2],
            'Front leg force at 150ms': fl150Ravg,
            'Front leg peak force': flpeakRavg,
            'Back leg force at 150ms': bl150Ravg,
            'Back leg peak force': blpeakRavg,
            'Crush factor at 150ms': cr150Ravg,
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


def getSquadDict(squadTestData, protocol):
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
    for i in range(len(timestamps)):
        timeadj.append(round(timestamps[i] + (minute * j)))
        j += 1
    i = 0
    squadSessions = {}
    for row in squadData:
        user = row[2]
        date = datetime.fromtimestamp(timeadj[i]).strftime("%Y/%m/%d")
        protocol = row[4]
        index = row[0]

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

    selectedProtocol = f': {protocol} :'
    # Filter the squadSessions dictionary to find all keys containing 'Baseline'
    proSessions = {k: v for k, v in squadSessions.items() if selectedProtocol in k}

    keys = [key for key, data in proSessions.items()]
    filteredKeys = []
    names = []
    for key in keys[::]:
        name = key.split(' : ')[0]
        if name in names:
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

    return squadProData, squadProDateData, allTests, allDates, reversed(list(np.unique(np.array(testDates))))


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

