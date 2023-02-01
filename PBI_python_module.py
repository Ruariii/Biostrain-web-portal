import numpy as np
import pandas as pd
import datetime
import time

####################################################################################################

def getPlayerDict(playerTestData):
    cols = ["Index", "Org", "User", "Timestamp", "Protocol", "TZ", "Left0ms", "Left50ms", "Left100ms", "Left150ms",
            "Left200ms", "Left250ms", "Left300ms", "Leftpeak", "Right0ms", "Right50ms", "Right100ms", "Right150ms",
            "Right200ms", "Right250ms", "Right300ms", "Rightpeak", "Combined0ms", "Combined50ms", "Combined100ms",
            "Combined150ms", "Combined200ms", "Combined250ms", "Combined300ms", "Combinedpeak"]

    # get dataArray - all tests
    data = []
    for i in playerTestData:
        data.append((i.Index, i.Org, i.User, i.Timestamp, i.Protocol, i.TZ,
                          i.Left0ms, i.Left50ms, i.Left100ms,
                          i.Left150ms, i.Left200ms, i.Left250ms,
                          i.Left300ms, i.Leftpeak, i.Right0ms,
                          i.Right50ms, i.Right100ms, i.Right150ms,
                          i.Right200ms, i.Right250ms, i.Right300ms,
                          i.Rightpeak, i.Combined0ms, i.Combined50ms,
                          i.Combined100ms, i.Combined150ms, i.Combined200ms,
                          i.Combined250ms, i.Combined300ms, i.Combinedpeak))


    timestamps = [time.mktime(row[3].timetuple()) for row in data]
    minute = 60
    timeadj = []
    j = 0
    for i in range(len(timestamps)):
        timeadj.append(round(timestamps[i] + (minute * j)))
        j += 1

    sessions = {}
    i=0
    for row in data:
        date = datetime.datetime.fromtimestamp(timeadj[i]).strftime("%Y/%m/%d")
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
        i+=1

    i = 0
    for row in data:
        date = datetime.datetime.fromtimestamp(timeadj[i]).strftime("%Y/%m/%d")
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
            i+=1
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
        date = datetime.datetime.strptime(sessionName.split(': ')[1], '%Y/%m/%d')
        dates.append(date)
        numTests.append(len(tests['index']))

    minDate = dates[0]
    maxDate = datetime.datetime.now()
    allDates = [datetime.datetime.strftime(minDate + datetime.timedelta(days=d), '%Y/%m/%d') for d in range((maxDate - minDate).days + 1)]
    allTests = []
    for day in allDates:
        dayobj = datetime.datetime.strptime(day, '%Y/%m/%d')
        if dayobj in dates:
            allTests.append(numTests[dates.index(dayobj)])
        else:
            allTests.append(0)



    return sessions, lastBaseline, baselineList, lastFatigue, fatigueList, allDates, allTests

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
    fl150Lmax = [max(fl150L)]
    bl150Lmax = [max(bl150L)]
    cr150Lmax = [max(cr150L)]
    fl150Rmax = [max(fl150R)]
    bl150Rmax = [max(bl150R)]
    cr150Rmax = [max(cr150R)]
    flpeakLmax = [max(flpeakL)]
    blpeakLmax = [max(blpeakL)]
    crpeakLmax = [max(crpeakL)]
    flpeakRmax = [max(flpeakR)]
    blpeakRmax = [max(blpeakR)]
    crpeakRmax = [max(crpeakR)]
    fl150Lavg = [sum(fl150L) / len(fl150L)]
    bl150Lavg = [sum(bl150L) / len(bl150L)]
    cr150Lavg = [sum(cr150L) / len(cr150L)]
    fl150Ravg = [sum(fl150R) / len(fl150R)]
    bl150Ravg = [sum(bl150R) / len(bl150R)]
    cr150Ravg = [sum(cr150R) / len(cr150R)]
    flpeakLavg = [sum(flpeakL) / len(flpeakL)]
    blpeakLavg = [sum(blpeakL) / len(blpeakL)]
    crpeakLavg = [sum(crpeakL) / len(crpeakL)]
    flpeakRavg = [sum(flpeakR) / len(flpeakR)]
    blpeakRavg = [sum(blpeakR) / len(blpeakR)]
    crpeakRavg = [sum(crpeakR) / len(crpeakR)]

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
        fl150Lmax = [round(max(fl150L), 1)]
        bl150Lmax = [round(max(bl150L), 1)]
        cr150Lmax = [round(max(cr150L), 1)]
        fl150Rmax = [round(max(fl150R), 1)]
        bl150Rmax = [round(max(bl150R), 1)]
        cr150Rmax = [round(max(cr150R), 1)]
        flpeakLmax = [round(max(flpeakL), 1)]
        blpeakLmax = [round(max(blpeakL), 1)]
        crpeakLmax = [round(max(crpeakL), 1)]
        flpeakRmax = [round(max(flpeakR), 1)]
        blpeakRmax = [round(max(blpeakR), 1)]
        crpeakRmax = [round(max(crpeakR), 1)]
        fl150Lavg = [round(sum(fl150L) / len(fl150L), 1)]
        bl150Lavg = [round(sum(bl150L) / len(bl150L), 1)]
        cr150Lavg = [round(sum(cr150L) / len(cr150L), 1)]
        fl150Ravg = [round(sum(fl150R) / len(fl150R), 1)]
        bl150Ravg = [round(sum(bl150R) / len(bl150R), 1)]
        cr150Ravg = [round(sum(cr150R) / len(cr150R), 1)]
        flpeakLavg = [round(sum(flpeakL) / len(flpeakL), 1)]
        blpeakLavg = [round(sum(blpeakL) / len(blpeakL), 1)]
        crpeakLavg = [round(sum(crpeakL) / len(crpeakL), 1)]
        flpeakRavg = [round(sum(flpeakR) / len(flpeakR), 1)]
        blpeakRavg = [round(sum(blpeakR) / len(blpeakR), 1)]
        crpeakRavg = [round(sum(crpeakR) / len(crpeakR), 1)]

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
        squadData.append((i.Index, i.Org, i.User, i.Timestamp, i.Protocol, i.TZ,
                     i.Left0ms, i.Left50ms, i.Left100ms,
                     i.Left150ms, i.Left200ms, i.Left250ms,
                     i.Left300ms, i.Leftpeak, i.Right0ms,
                     i.Right50ms, i.Right100ms, i.Right150ms,
                     i.Right200ms, i.Right250ms, i.Right300ms,
                     i.Rightpeak, i.Combined0ms, i.Combined50ms,
                     i.Combined100ms, i.Combined150ms, i.Combined200ms,
                     i.Combined250ms, i.Combined300ms, i.Combinedpeak))

    timestamps = [time.mktime(row[3].timetuple()) for row in squadData]
    minute = 60
    timeadj = []
    j = 0
    for i in range(len(timestamps)):
        timeadj.append(round(timestamps[i] + (minute * j)))
        j += 1

    squadSessions = {}
    for row in squadData:
        user = row[2]
        date = datetime.datetime.fromtimestamp(timeadj[i]).strftime("%Y/%m/%d")
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

    for row in squadData:
        user = row[2]
        date = datetime.datetime.fromtimestamp(timeadj[i]).strftime("%Y/%m/%d")
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

    selectedProtocol = f': {protocol} :'

    # Filter the squadSessions dictionary to find all keys containing 'Baseline'
    proSessions = {k: v for k, v in squadSessions.items() if selectedProtocol in k}

    keys = [key for key, data in proSessions.items()]
    filteredKeys = []
    names = []
    for key in keys[::-1]:
        name = key.split(' : ')[0]
        if name in names:
            continue
        else:
            filteredKeys.append(key)
        names.append(name)

    filteredSessions = {k: v for k, v in proSessions.items() if k in filteredKeys}
    squadProData = {}
    li, ri = 0, 0
    for key in filteredKeys:
        user = key.split(' : ')[0]
        squadProData[user] = {}
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
        fl150Lmax = [round(max(fl150L), 1)]
        bl150Lmax = [round(max(bl150L), 1)]
        cr150Lmax = [round(max(cr150L), 1)]
        fl150Rmax = [round(max(fl150R), 1)]
        bl150Rmax = [round(max(bl150R), 1)]
        cr150Rmax = [round(max(cr150R), 1)]
        flpeakLmax = [round(max(flpeakL), 1)]
        blpeakLmax = [round(max(blpeakL), 1)]
        crpeakLmax = [round(max(crpeakL), 1)]
        flpeakRmax = [round(max(flpeakR), 1)]
        blpeakRmax = [round(max(blpeakR), 1)]
        crpeakRmax = [round(max(crpeakR), 1)]
        fl150Lavg = [round(sum(fl150L) / len(fl150L), 1)]
        bl150Lavg = [round(sum(bl150L) / len(bl150L), 1)]
        cr150Lavg = [round(sum(cr150L) / len(cr150L), 1)]
        fl150Ravg = [round(sum(fl150R) / len(fl150R), 1)]
        bl150Ravg = [round(sum(bl150R) / len(bl150R), 1)]
        cr150Ravg = [round(sum(cr150R) / len(cr150R), 1)]
        flpeakLavg = [round(sum(flpeakL) / len(flpeakL), 1)]
        blpeakLavg = [round(sum(blpeakL) / len(blpeakL), 1)]
        crpeakLavg = [round(sum(crpeakL) / len(crpeakL), 1)]
        flpeakRavg = [round(sum(flpeakR) / len(flpeakR), 1)]
        blpeakRavg = [round(sum(blpeakR) / len(blpeakR), 1)]
        crpeakRavg = [round(sum(crpeakR) / len(crpeakR), 1)]

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
    dates, numTests = [], []
    for sessionName, tests in filteredSessions.items():
        date = datetime.datetime.strptime(sessionName.split(': ')[2], '%Y/%m/%d')
        dates.append(date)
        numTests.append(len(tests['index']))

    minDate = dates[0]
    maxDate = datetime.datetime.now()
    allDates = [datetime.datetime.strftime(minDate + datetime.timedelta(days=d), '%Y/%m/%d') for d in range((maxDate - minDate).days + 1)]
    allTests = []
    for day in allDates:
        dayobj = datetime.datetime.strptime(day, '%Y/%m/%d')
        if dayobj in dates:
            allTests.append(numTests[dates.index(dayobj)])
        else:
            allTests.append(0)

    return squadProData, allTests, allDates



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
                maxidx = np.argmax((baselineDict[protocol][key]))
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
        date = row[3]
        activityLog[name][date] = {}
        activityLog[name][date]['protocol'] = []
        activityLog[name][date]['count'] = []
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

    a = datetime.date.today()

    timeExt = timeArray
    countExt = countArray
    timeObj = timeExt[len(timeArray) - 1]
    x = 1
    while timeObj < a:
        timeObj = timeObj + datetime.timedelta(days=x)
        timeExt.append(timeObj)
        countExt.append(0)
        x += 1
    timeStr = [time.strftime('%Y-%m-%d') for time in timeExt]





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

    return baselineMax, timeStr, countExt, proArray, radarLabels, radarDataL, radarDataR, fPlotDictL,\
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
    players2 = []
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
        players2.append(i.User)

        infoArray.append((i.Org, i.User, i.Timestamp, i.Protocol, i.TZ,
                         i.Leftpeak, i.Rightpeak))
    # get last 5 tests
    end = len(dataArray) - 1
    if len(dataArray)>5:
        dataArrayHead = infoArray[end-5:end]
    else:
        dataArrayHead = infoArray[0:end]

    activityLog = {pro: {}}
    for row in dataArray:
        date = row[3]
        activityLog[pro][date] = {}
        activityLog[pro][date]['protocol'] = []
        activityLog[pro][date]['count'] = []
    for key in activityLog[pro]:
        counter = 0
        for row in dataArray:
            if row[3] == key:
                counter += 1
                pro = row[4]
            else:
                continue
        activityLog[pro][key]['count'] = counter

    timeArray = [time for time in activityLog[pro]]
    countArray, proArray = [], []
    for time in timeArray:
        countArray.append(activityLog[pro][time]['count'])

    a = datetime.date.today()

    timeExt = timeArray
    countExt = countArray
    timeObj = timeExt[len(timeArray) - 1]
    x = 1
    while timeObj < a:
        timeObj = timeObj + datetime.timedelta(days=x)
        timeExt.append(timeObj)
        countExt.append(0)
        x += 1
    timeStr = [time.strftime('%Y-%m-%d') for time in timeExt]



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

    return dataArray, dataArrayHead, countExt, timeStr, players,\
           bestPeak, best150, FLpeakAsym, BLpeakAsym, FL150Asym, BL150Asym,

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
            final_report += row.format(protocol=protocol, tz=tz, leg=leg, best=round(tup[0],1), worst=round(tup[1],1), average=round(tup[2],1))

  # close the table
  final_report += "</table>"

  # return the final report
  return final_report


