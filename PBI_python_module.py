import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import statistics as st
import os
from datetime import datetime

####################################################################################################


def sorter(directory):
    fnames = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".csv"):
                fnames.append(os.path.join(root, file))

    datafiles, sessionfiles = [], []
    for name in fnames:
        if name[len(name) - 43] == '1':
            if 'sessionData' in name:
                datafiles.append(name)
            elif 'sessionStats' in name:
                sessionfiles.append(name)
            else:
                continue
        else:
            continue

    org = []
    datesUTC = []
    dates = []
    TZ = []
    pro = []
    mode = []
    comb = []
    user = []
    j = 0
    for f in sessionfiles:
        try:
            sf = pd.read_csv(f, header=0, nrows=7)
        except Exception as e:
            pass
        if np.shape(sf.values) == (7, 1):
            org.append(str(sf.values[0][0]))
            user.append(str(sf.values[1][0]))
            mode.append(str(sf.values[5][0]))
            pro.append(str(sf.values[6][0]))
        elif np.shape(sf.values) == (7, 2):
            org.append(str(sf.values[0][1]))
            user.append(str(sf.values[1][1]))
            mode.append(str(sf.values[5][1]))
            pro.append(str(sf.values[6][1]))
        datesUTC.append(f[len(f) - 43:len(f) - 33])
        dates.append(datetime.utcfromtimestamp(int(datesUTC[j])).strftime('%Y-%m-%d %H:%M:%S'))
        TZ.append(f[len(f) - 21:len(f) - 17])
        j += 1

    for d in range(len(datesUTC)):
        comb.append((org[d], user[d], dates[d], mode[d], pro[d], TZ[d]))

    df = pd.DataFrame(comb)
    org = df[:][0]
    user = df[:][1]
    sdt = df[:][2]
    mode = df[:][3]
    pro = df[:][4]
    tz = df[:][5]
    finfo = pd.DataFrame({'Organisation': org,
                         'User': user,
                         'Session timestamp': sdt,
                         'Mode': mode,
                         'Protocol': pro,
                         'Transformational_zone': tz})

    return finfo, sessionfiles, datafiles

####################################################################################################

def getStats(finfo, sessionfiles, org_val, user_val, pro_val, tz_val):

    idx = []
    s, sL, sR = [], [], []
    if tz_val == 'Both':
        search_params = {'Organisation': org_val,
                         'User': user_val,
                         'Protocol': pro_val}
        tzstr = "LHTZ & RHTZ"
    else:
        search_params = {'Organisation': org_val,
                         'User': user_val,
                         'Protocol': pro_val,
                         'Transformational_zone': tz_val}
        tzstr = str(tz_val)
    stats = {}
    for i in range(len(finfo)):
        test = 0
        for key in search_params:
            if search_params[key] == finfo[key][i]:
                test += 1
            else:
                continue
        if test == len(search_params):
            idx.append(i)
        else:
            continue

    for j in idx:

        sf = pd.read_csv(sessionfiles[j], header=15)

        namecol = sf.iloc[:, 0]
        forcecol = sf.iloc[:, 1]

        lp, l0, l50, l100, l150, l200, l250, l300 = [], [], [], [], [], [], [], []
        rp, r0, r50, r100, r150, r200, r250, r300 = [], [], [], [], [], [], [], []

        for i in range(len(namecol)):

            if namecol[i] == 'Left peak force':
                lp.append(forcecol[i])
                continue
            elif namecol[i] == 'Right peak force':
                rp.append(forcecol[i])
                continue

            if namecol[i] == 'Left force @ 0':
                l0.append(forcecol[i])
                continue
            elif namecol[i] == 'Right force @ 0':
                r0.append(forcecol[i])
                continue

            elif namecol[i] == 'Left force @ 50':
                l50.append(forcecol[i])
                continue
            elif namecol[i] == 'Right force @ 50':
                r50.append(forcecol[i])
                continue

            if namecol[i] == 'Left force @ 100':
                l100.append(forcecol[i])
                continue
            elif namecol[i] == 'Right force @ 100':
                r100.append(forcecol[i])
                continue

            elif namecol[i] == 'Left force @ 150':
                l150.append(forcecol[i])
                continue
            elif namecol[i] == 'Right force @ 150':
                r150.append(forcecol[i])
                continue

            if namecol[i] == 'Left force @ 200':
                l200.append(forcecol[i])
                continue
            elif namecol[i] == 'Right force @ 200':
                r200.append(forcecol[i])
                continue

            elif namecol[i] == 'Left force @ 250':
                l250.append(forcecol[i])
                continue
            elif namecol[i] == 'Right force @ 250':
                r250.append(forcecol[i])
                continue

            if namecol[i] == 'Left force @ 300':
                l300.append(forcecol[i])
                continue
            elif namecol[i] == 'Right force @ 300':
                r300.append(forcecol[i])
                continue

        org = finfo['Organisation'][j]
        user = finfo['User'][j]
        timestamp = sessionfiles[j][len(sessionfiles[j]) - 32:len(sessionfiles[j]) - 22]
        tz = finfo['Transformational_zone'][j]

        lpm, l0m, l50m, l100m, l150m, l200m, l250m, l300m = max(lp, default=0), max(l0, default=0), max(l50,
                                                                                                        default=0), max(
            l100, default=0), max(l150, default=0), max(l200, default=0), max(l250, default=0), max(l300, default=0)
        rpm, r0m, r50m, r100m, r150m, r200m, r250m, r300m = max(rp, default=0), max(r0, default=0), max(r50,
                                                                                                        default=0), max(
            r100, default=0), max(r150, default=0), max(r200, default=0), max(r250, default=0), max(r300, default=0)

        s.append((org, user, datetime.utcfromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S'), tz, lpm, l0m,
                  l50m, l100m, l150m, l200m, l250m, l300m, rpm, r0m, r50m, r100m,r150m, r200m, r250m, r300m))

        if tz == 'LHTZ':
            sL.append((org, user, datetime.utcfromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S'), tz, lpm, l0m,
                       l50m, l100m, l150m, l200m, l250m, l300m, rpm, r0m, r50m, r100m, r150m, r200m, r250m, r300m))
        else:
            sR.append((org, user, datetime.utcfromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S'), tz, lpm, l0m,
                       l50m, l100m, l150m, l200m, l250m, l300m, rpm, r0m, r50m, r100m, r150m, r200m, r250m, r300m))

    stats = pd.DataFrame(s,
                         columns=['Organisation', 'User',
                                  'Timestamp', 'Transformational zone',
                                  'Peak forceL', 'Force @ 0msL',
                                  'Force @ 50msL', 'Force @ 100msL',
                                  'Force @ 150msL', 'Force @ 200msL',
                                  'Force @ 250msL', 'Force @ 300msL',
                                  'Peak forceR', 'Force @ 0msR',
                                  'Force @ 50msR', 'Force @ 100msR',
                                  'Force @ 150msR', 'Force @ 200msR',
                                  'Force @ 250msR', 'Force @ 300msR'])

    LHTZstats = pd.DataFrame(sL,
                             columns=['Organisation', 'User',
                                      'Timestamp', 'Transformational zone',
                                      'Peak forceL', 'Force @ 0msL',
                                      'Force @ 50msL', 'Force @ 100msL',
                                      'Force @ 150msL', 'Force @ 200msL',
                                      'Force @ 250msL', 'Force @ 300msL',
                                      'Peak forceR', 'Force @ 0msR',
                                      'Force @ 50msR', 'Force @ 100msR',
                                      'Force @ 150msR', 'Force @ 200msR',
                                      'Force @ 250msR', 'Force @ 300msR'])

    RHTZstats = pd.DataFrame(sR,
                             columns=['Organisation', 'User',
                                      'Timestamp', 'Transformational zone',
                                      'Peak forceL', 'Force @ 0msL',
                                      'Force @ 50msL', 'Force @ 100msL',
                                      'Force @ 150msL', 'Force @ 200msL',
                                      'Force @ 250msL', 'Force @ 300msL',
                                      'Peak forceR', 'Force @ 0msR',
                                      'Force @ 50msR', 'Force @ 100msR',
                                      'Force @ 150msR', 'Force @ 200msR',
                                      'Force @ 250msR', 'Force @ 300msR'])


    return stats

####################################################################################################

def sessionPlotter(xplot, yplot, title):

    fig = go.Figure()

    for plot in yplot:
        fig.add_trace(go.Scatter(
            x=xplot,
            y=yplot[plot],
            name=plot))

    fig.update_layout(
        yaxis_title="Force (kg)",
        legend_title="Legend",
        plot_bgcolor="#4184C5",
        paper_bgcolor="rgb(15,37,55)",
        font=dict(
            size=12,
            color="white"
        ),
        title_text=title,
        title_yref="paper",
        title_xanchor="center",
        colorway=px.colors.qualitative.Light24,
        legend_orientation="h",
        legend_y=-0.25,
        height=500
    )
    fig.update_layout(hovermode="x unified",
                      hoverlabel=dict(
                          bgcolor="rgb(15,37,55)",
                          bordercolor="lightgrey",
                          namelength=-1
                      ))

    return fig


def dataPuller(directory):
    import os
    fnames = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".csv"):
                fnames.append(os.path.join(root, file))

    datafiles, sessionfiles = [], []
    for name in fnames:
        if name[len(name) - 43] == '1':
            if 'sessionData' in name:
                datafiles.append(name)
            elif 'sessionStats' in name:
                sessionfiles.append(name)
            else:
                continue
        else:
            continue

    comb = []
    for f in sessionfiles:

        datesUTC = (f[len(f) - 43:len(f) - 33])
        D = (datetime.utcfromtimestamp(int(datesUTC)).strftime('%Y-%m-%d %H:%M'))
        TZ = (f[len(f) - 21:len(f) - 17])
        try:
            df = pd.read_csv(f, header=None, names=[0, 1], index_col=False)
            info = df.iloc[0:9, :]
            O = (info.values[1][1])
            U = (info.values[2][1])
            P = (info.values[7][1])

            stats = df.iloc[13:len(df), :]
            namecol = stats.iloc[:, 0]
            forcecol = stats.iloc[:, 1]

            lp, l0, l50, l100, l150, l200, l250, l300 = [], [], [], [], [], [], [], []
            rp, r0, r50, r100, r150, r200, r250, r300 = [], [], [], [], [], [], [], []
            for i in range(13, len(df)):

                if namecol[i] == 'Left peak force':
                    lp.append(forcecol[i])
                    continue
                elif namecol[i] == 'Right peak force':
                    rp.append(forcecol[i])
                    continue

                if namecol[i] == 'Left force @ 0':
                    l0.append(forcecol[i])
                    continue
                elif namecol[i] == 'Right force @ 0':
                    r0.append(forcecol[i])
                    continue

                elif namecol[i] == 'Left force @ 50':
                    l50.append(forcecol[i])
                    continue
                elif namecol[i] == 'Right force @ 50':
                    r50.append(forcecol[i])
                    continue

                if namecol[i] == 'Left force @ 100':
                    l100.append(forcecol[i])
                    continue
                elif namecol[i] == 'Right force @ 100':
                    r100.append(forcecol[i])
                    continue

                elif namecol[i] == 'Left force @ 150':
                    l150.append(forcecol[i])
                    continue
                elif namecol[i] == 'Right force @ 150':
                    r150.append(forcecol[i])
                    continue

                if namecol[i] == 'Left force @ 200':
                    l200.append(forcecol[i])
                    continue
                elif namecol[i] == 'Right force @ 200':
                    r200.append(forcecol[i])
                    continue

                elif namecol[i] == 'Left force @ 250':
                    l250.append(forcecol[i])
                    continue
                elif namecol[i] == 'Right force @ 250':
                    r250.append(forcecol[i])
                    continue

                if namecol[i] == 'Left force @ 300':
                    l300.append(forcecol[i])
                    continue
                elif namecol[i] == 'Right force @ 300':
                    r300.append(forcecol[i])
                    continue

            lpm, l0m, l50m, l100m, l150m, l200m, l250m, l300m = max(lp, default=0), max(l0, default=0), max(l50,
                                                                                                            default=0), max(
                l100, default=0), max(l150, default=0), max(l200, default=0), max(l250, default=0), max(l300, default=0)
            rpm, r0m, r50m, r100m, r150m, r200m, r250m, r300m = max(rp, default=0), max(r0, default=0), max(r50,
                                                                                                            default=0), max(
                r100, default=0), max(r150, default=0), max(r200, default=0), max(r250, default=0), max(r300, default=0)

            comb.append((O, U, D, P, TZ, l0m, l50m, l100m, l150m, l200m, l250m, l300m, lpm, r0m, r50m, r100m, r150m,
                         r200m, r250m, r300m, rpm))


        except:
            continue

    headings = ['Org', 'User', 'Timestamp', 'Protocol', 'TZ',
                'Left force @ 0ms', 'Left force @ 50ms',
                'Left force @ 100ms', 'Left force @ 150ms',
                'Left force @ 200ms', 'Left force @ 250ms',
                'Left force @ 300ms', 'Left peak force',
                'Right force @ 0ms', 'Right force @ 50ms',
                'Right force @ 100ms', 'Right force @ 150ms',
                'Right force @ 200ms', 'Right force @ 250ms',
                'Right force @ 300ms', 'Right peak force']
    datafile = pd.DataFrame(comb, columns=headings)

    return datafile

def plotStyle(ptitle, x_val):

    plotcolors = ['#FD3216', '#00FE35', '#B68E00', '#0DF9FF',
                  '#FE00CE', '#479B55', '#F6F926', '#FED4C4',
                  '#FF9616', '#EEA6FB', '#DC587D', '#D626FF',
                  '#6E899C', '#00B5F7', '#6A76FC', '#C9FBE5',
                  '#FF0092', '#22FFA7', '#E3EE9E', '#86CE00',
                  '#BC7196', '#FC6955', '#E48F72']

    fig = go.Figure()
    fig.update_xaxes(showgrid=True, gridcolor='white',
                     showline=True, linewidth=2, linecolor='white', mirror=True)
    fig.update_yaxes(showgrid=True, gridcolor='white',
                     showline=True, linewidth=2, linecolor='white', mirror=True)
    fig.update_layout(
        autotypenumbers='convert types',
        xaxis_title=str(x_val),
        yaxis_title="Force (kg)",
        legend_title="Legend:",
        plot_bgcolor="#4184C5",
        paper_bgcolor="rgb(15,37,55)",
        colorway=plotcolors,
        font=dict(
            size=12,
            color="white"
        ),
        title_text=ptitle,
        title_font_size=20,
        title_xanchor="center",
        title_x=0.5,
        legend_orientation="h",
        legend_y=-0.125,
        legend_xanchor="center",
        legend_x=0.5,
        font_size=14,
        height=750
    )
    fig.update_layout(hovermode="x unified",
                      hoverlabel=dict(
                          bgcolor="rgb(15,37,55)",
                          bordercolor="lightgrey",
                          namelength=-1
                      ))
    return fig



def create_df(df, org, pro):

    if org == 'All':
        orgFilteredData=df
    else:
        orgFilteredData=df.query(f"Org == '{org}'")
    if pro == 'Any':
        proFilteredData=orgFilteredData
    else:
        proFilteredData=orgFilteredData.query(f"Protocol == '{pro}'")

    plotdf = proFilteredData.reset_index()

    return plotdf



def create_dict(df):
    #filter database
    count=0
    idx=['Org', 'User', 'Timestamp', 'Protocol', 'TZ',
           'Left force @ 0ms', 'Left force @ 50ms', 'Left force @ 100ms',
           'Left force @ 150ms', 'Left force @ 200ms', 'Left force @ 250ms',
           'Left force @ 300ms', 'Left peak force', 'Right force @ 0ms',
           'Right force @ 50ms', 'Right force @ 100ms', 'Right force @ 150ms',
           'Right force @ 200ms', 'Right force @ 250ms', 'Right force @ 300ms',
           'Right peak force']
    dataidx=['Left force @ 0ms', 'Left force @ 50ms', 'Left force @ 100ms',
           'Left force @ 150ms', 'Left force @ 200ms', 'Left force @ 250ms',
           'Left force @ 300ms', 'Left peak force', 'Right force @ 0ms',
           'Right force @ 50ms', 'Right force @ 100ms', 'Right force @ 150ms',
           'Right force @ 200ms', 'Right force @ 250ms', 'Right force @ 300ms',
           'Right peak force']

    fildf = df[idx]

    #initialise dict
    plotDict={}
    for user in fildf['User'].unique():
        plotDict[user]={}
    for user in plotDict:
        for i in range(len(fildf)):
            if fildf['User'][i] == user:
                plotDict[user][fildf['Protocol'][i]]={}

    for user in plotDict:
        for protocol in  plotDict[user]:
            for i in range(len(fildf)):
                if fildf['Protocol'][i] == protocol:
                    plotDict[user][protocol][fildf['TZ'][i]] = {}

    for user in plotDict:
        for protocol in  plotDict[user]:
            for tz in plotDict[user][protocol]:
                plotDict[user][protocol][tz]['Front leg']={}
                plotDict[user][protocol][tz]['Back leg']={}


    for user in plotDict:
        for protocol in  plotDict[user]:
            for tz in plotDict[user][protocol]:
                for leg in plotDict[user][protocol][tz]:
                    for i in dataidx:
                        plotDict[user][protocol][tz][leg][i]=[]
    #populate dict
    for user in plotDict:
        for protocol in  plotDict[user]:
            for tz in plotDict[user][protocol]:
                 for leg in plotDict[user][protocol][tz]:
                        for data in plotDict[user][protocol][tz][leg]:
                            for i in range(len(fildf)):
                                if tz == 'LHTZ' and leg == 'Front leg':
                                    if fildf['TZ'][i] == tz and fildf['Protocol'][i] == protocol and fildf['User'][i] == user:
                                        if 'Left' in data:
                                            plotDict[user][protocol][tz][leg][data].append(fildf[data][i])
                                elif tz == 'LHTZ' and leg == 'Back leg':
                                    if fildf['TZ'][i] == tz and fildf['Protocol'][i] == protocol and fildf['User'][i] == user:
                                        if 'Right' in data:
                                            plotDict[user][protocol][tz][leg][data].append(fildf[data][i])
                                elif tz == 'RHTZ' and leg == 'Front leg':
                                    if fildf['TZ'][i] == tz and fildf['Protocol'][i] == protocol and fildf['User'][i] == user:
                                        if 'Right' in data:
                                            plotDict[user][protocol][tz][leg][data].append(fildf[data][i])
                                else:
                                    if fildf['TZ'][i] == tz and fildf['Protocol'][i] == protocol and fildf['User'][i] == user:
                                        if 'Left' in data:
                                            plotDict[user][protocol][tz][leg][data].append(fildf[data][i])
    return plotDict
