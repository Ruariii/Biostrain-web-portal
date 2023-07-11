// SINGLE SESSION FILTER FUNCTION


function getSessionData(sessions, selectedSession) {
    const data = sessions[selectedSession];
    const tzs = data['TZ'];
    const fl150 = data['Front leg force at 150ms'];
    const flpeak = data['Front leg peak force'];
    const bl150 = data['Back leg force at 150ms'];
    const blpeak = data['Back leg peak force'];
    const cr150 = data['Crush factor at 150ms'];
    const crpeak = data['Peak crush factor'];

    const indexL = [];
    const indexR = [];
    const flRFDL = [];
    const flRFDR = [];
    const fl150L = [];
    const fl150R = [];
    const flpeakL = [];
    const flpeakR = [];
    const blRFDL = [];
    const blRFDR = [];
    const bl150L = [];
    const bl150R = [];
    const blpeakL = [];
    const blpeakR = [];
    const cr150L = [];
    const cr150R = [];
    const crpeakL = [];
    const crpeakR = [];
    let li = 0;
    let ri = 0;

    for (let i = 0; i < tzs.length; i++) {
    if (tzs[i] == 'LHTZ') {
    li += 1;
    indexL.push(li);
    flRFDL.push
    fl150L.push(fl150[i]);
    flpeakL.push(flpeak[i]);
    bl150L.push(bl150[i]);
    blpeakL.push(blpeak[i]);
    cr150L.push(cr150[i]);
    crpeakL.push(crpeak[i]);
    }
    else {
    ri += 1;
    indexR.push(ri);
    fl150R.push(fl150[i]);
    flpeakR.push(flpeak[i]);
    bl150R.push(bl150[i]);
    blpeakR.push(blpeak[i]);
    cr150R.push(cr150[i]);
    crpeakR.push(crpeak[i]);
    }
    }

    let LHTZ_data = {
        'session':{
        'index': indexL,
        'Front leg force at 150ms': fl150L,
        'Front leg peak force': flpeakL,
        'Back leg force at 150ms': bl150L,
        'Back leg peak force': blpeakL,
        'Crush factor at 150ms': cr150L,
        'Peak crush factor': crpeakL
        }
        };

    let RHTZ_data = {
        'session':{
        'index': indexR,
        'Front leg force at 150ms': fl150R,
        'Front leg peak force': flpeakR,
        'Back leg force at 150ms': bl150R,
        'Back leg peak force': blpeakR,
        'Crush factor at 150ms': cr150R,
        'Peak crush factor': crpeakR
        }
        };



    return {'LHTZ': LHTZ_data, 'RHTZ': RHTZ_data}
}

function getDatedSession(squadData, date) {
    var datedSession = squadData[date]

    return datedSession
}

function getDatedSessionUsers(datedSession) {
    var datedSessionUsers = []
    for (name in datedSession) {
        datedSessionUsers.push(name)
    }

    return datedSessionUsers
}


function filterDataSession(metric, LHTZ_data, RHTZ_data) {
    // Filter the data based on the selected metric
    var LHTZ_filteredData = LHTZ_data['session'][metric];
    var RHTZ_filteredData = RHTZ_data['session'][metric];

    var rows = Math.max(RHTZ_filteredData.length, LHTZ_filteredData.length);

    // Return the filtered data
    return {'LHTZ': LHTZ_filteredData, 'RHTZ': RHTZ_filteredData, 'length': rows};
}


function getAsymMetric(metricType, sessionData) {

    if (metricType == 'Peak force'){
        var LHTZ_FLchartData = sessionData['LHTZ']['session']['Front leg peak force'];
        var LHTZ_BLchartData = sessionData['LHTZ']['session']['Back leg peak force'];
        var RHTZ_FLchartData = sessionData['RHTZ']['session']['Front leg peak force'];
        var RHTZ_BLchartData = sessionData['RHTZ']['session']['Back leg peak force'];
    }
    else if (metricType == 'Force at 150ms'){
        var LHTZ_FLchartData = sessionData['LHTZ']['session']['Front leg force at 150ms'];
        var LHTZ_BLchartData = sessionData['LHTZ']['session']['Back leg force at 150ms'];
        var RHTZ_FLchartData = sessionData['RHTZ']['session']['Front leg force at 150ms'];
        var RHTZ_BLchartData = sessionData['RHTZ']['session']['Back leg force at 150ms'];
    }
    else if (metricType == 'RFD 50-150ms'){
        var LHTZ_FLchartData = sessionData['LHTZ']['session']['Front leg RFD 50-150ms'];
        var LHTZ_BLchartData = sessionData['LHTZ']['session']['Back leg RFD 50-150ms'];
        var RHTZ_FLchartData = sessionData['RHTZ']['session']['Front leg RFD 50-150ms'];
        var RHTZ_BLchartData = sessionData['RHTZ']['session']['Back leg RFD 50-150ms'];
    }

    return [LHTZ_FLchartData, LHTZ_BLchartData, RHTZ_FLchartData, RHTZ_BLchartData]
}

function getAsym(asymType, chartData){
    var LHTZ_FLchartData = chartData[0]
    var LHTZ_BLchartData = chartData[1]
    var RHTZ_FLchartData = chartData[2]
    var RHTZ_BLchartData = chartData[3]
    var TZ_asym=[]
    if (asymType == "Transition zone"){
        for (var i = 0; i < LHTZ_FLchartData.length; i++) {
        var asym = 100*(((RHTZ_FLchartData[i]+RHTZ_BLchartData[i])-(LHTZ_FLchartData[i]+LHTZ_BLchartData[i]))/(RHTZ_FLchartData[i]+RHTZ_BLchartData[i]))
        TZ_asym.push(asym)
        }
        }
    else if (asymType == "Front leg"){
        for (var i = 0; i < LHTZ_FLchartData.length; i++) {
        var asym = 100*(((RHTZ_FLchartData[i])-(LHTZ_FLchartData[i]))/(RHTZ_FLchartData[i]))
        TZ_asym.push(asym)
        }
        }
    else if (asymType == "Back leg"){
        for (var i = 0; i < LHTZ_BLchartData.length; i++) {
        var asym = 100*(((RHTZ_BLchartData[i])-(LHTZ_BLchartData[i]))/(RHTZ_BLchartData[i]))
        TZ_asym.push(asym)
        }
    }

    return TZ_asym
}

function updateChartDataAsym(TZ_asym, chartData, sessionData, chart){

     var LHTZ_FLchartData = chartData[0]
     var LHTZ_BLchartData = chartData[1]
     var RHTZ_FLchartData = chartData[2]
     var RHTZ_BLchartData = chartData[3]

     chart.data.datasets[0].data = TZ_asym;
     chart.data.datasets[1].data = LHTZ_FLchartData;
     chart.data.datasets[2].data = LHTZ_BLchartData;
     chart.data.datasets[3].data = RHTZ_FLchartData;
     chart.data.datasets[4].data = RHTZ_BLchartData;

     var labels = []
     for (var i = 0; i < TZ_asym.length; i++) {
        labels.push(i+1)
     }
     chart.data.labels = labels

    chart.options.plugins.tooltip.callbacks.footer = function (context) {
                        var index = context[0].dataIndex; // Get the index of the selected data point
                        var protocol = sessionData['Tags']['Protocol'][index]; // Get the protocol from chartData
                        var matchday = sessionData['Tags']['Matchday'][index]; // Get the matchday from chartData
                        var config = sessionData['Tags']['Phase'][index]; // Get the config from chartData
                        var strategy = sessionData['Tags']['Strategy'][index]; // Get the strategy from chartData

                        // Display footer with additional data
                        return 'Protocol: ' + protocol +'\nMatchday: ' + matchday +'\nConfig: ' + config +'\nStrategy: ' + strategy;
                    };

     chart.update();
}

function updateChartDataSession(filteredData, chart) {
    // Update the data for the LHTZ dataset
    chart.data.datasets[0].data = filteredData['LHTZ'];
    // Update the data for the RHTZ dataset
    chart.data.datasets[1].data = filteredData['RHTZ'];

    var labels = []
    for (var i = 0; i < filteredData['length']; i++) {
        labels.push(i+1)
    }

    chart.data.labels = labels
    // Update the chart
    chart.update();
}

function updateChartDataHistorical(filteredData, chart) {
    // Update the data for the LHTZ dataset
    chart.data.datasets[0].data = filteredData['LHTZ'];
    // Update the data for the RHTZ dataset
    chart.data.datasets[1].data = filteredData['RHTZ'];

    chart.data.labels = filteredData['labels']

    // Update the chart
    chart.update();
}

function filterDataSquad(data, metric, dataDict) {
    // Filter the data based on the selected metric
    var LHTZ_data = [];
    var RHTZ_data = [];
    var labels = [];

    const allKeys = Object.keys(dataDict);
    allKeys.forEach(key => {
      LHTZ_data.push(dataDict[key]['LHTZ'][data][metric][0]);
      RHTZ_data.push(dataDict[key]['RHTZ'][data][metric][0]);
      labels.push(key)
    });

    var rows = Math.max(RHTZ_data.length, LHTZ_data.length);

    // Return the filtered data
    return {'LHTZ': LHTZ_data, 'RHTZ': RHTZ_data, 'length': rows, 'labels':labels};
}

function filterDataHistorical(protocol, data, metric, dataDict) {
  // Extract the data for the chart
  var LHTZ_data = [];
  var RHTZ_data = [];
  var labels = [];

  if (protocol === 'All protocols') {
    const allKeys = Object.keys(dataDict);
    allKeys.forEach(key => {
      LHTZ_data.push(dataDict[key]['LHTZ'][data][metric][0]);
      RHTZ_data.push(dataDict[key]['RHTZ'][data][metric][0]);
      labels.push(key)
    });
  } else {
    const baselineKeys = Object.keys(dataDict).filter(key => key.includes(protocol+':'));
    baselineKeys.forEach(key => {
      LHTZ_data.push(dataDict[key]['LHTZ'][data][metric][0]);
      RHTZ_data.push(dataDict[key]['RHTZ'][data][metric][0]);
      labels.push(key)
    });
  }

  var rows = Math.max(RHTZ_data.length, LHTZ_data.length);


  // Return the filtered data
  return {'LHTZ': LHTZ_data, 'RHTZ': RHTZ_data, 'length': rows, 'labels':labels};
}




function updateTableHistorical(filteredData4, table, session_names2) {
    // Clear the existing content of the table
    table.innerHTML = "";

    // Create the table headers
    var headers = ["Test", "LHTZ score (kg)", "RHTZ score (kg)", "Asymmetry (%)"];
    var headerRow = document.createElement("tr");
    for (var i = 0; i < headers.length; i++) {
        var headerCell = document.createElement("th");
        headerCell.innerHTML = headers[i];
        headerRow.appendChild(headerCell);
    }
    table.appendChild(headerRow);

    // Create the table rows
    for (var i = 0; i < filteredData4['labels'].length; i++) {
        var row = document.createElement("tr");
        var testCell = document.createElement("td");
        testCell.innerHTML = filteredData4['labels'][i];
        row.appendChild(testCell);

        var LHTZValue = filteredData4['LHTZ'][i];
        var RHTZValue = filteredData4['RHTZ'][i];
        var LHTZCell = document.createElement("td");
        LHTZCell.innerHTML = LHTZValue;
        row.appendChild(LHTZCell);

        var RHTZCell = document.createElement("td");
        RHTZCell.innerHTML = RHTZValue;
        row.appendChild(RHTZCell);

        var percentageDiff = ((RHTZValue - LHTZValue) / LHTZValue) * 100;
        var diffCell = document.createElement("td");
        diffCell.innerHTML = percentageDiff.toFixed(2);
        row.appendChild(diffCell);

        table.appendChild(row);
    }
}

// SHARED GRAPHING FUNCTIONS


function updateTable(filteredData, table) {
    // Clear the existing content of the table
    table.innerHTML = "";

    // Create the table headers
    var headers = ["Test number", "LHTZ score (kg)", "RHTZ score (kg)", "Asymmetry (%)"];
    var rows = filteredData['length']
    var headerRow = document.createElement("tr");
    for (var i = 0; i < headers.length; i++) {
        var headerCell = document.createElement("th");
        headerCell.innerHTML = headers[i];
        headerRow.appendChild(headerCell);
    }
    table.appendChild(headerRow);

    // Create the table rows
    for (var i = 0; i < rows; i++) {
        var row = document.createElement("tr");
        var testCell = document.createElement("td");
        testCell.innerHTML = i+1;
        row.appendChild(testCell);

        var LHTZValue = filteredData['LHTZ'][i];
        var RHTZValue = filteredData['RHTZ'][i];
        var LHTZCell = document.createElement("td");
        LHTZCell.innerHTML = LHTZValue;
        row.appendChild(LHTZCell);

        var RHTZCell = document.createElement("td");
        RHTZCell.innerHTML = RHTZValue;
        row.appendChild(RHTZCell);

        var percentageDiff = ((RHTZValue - LHTZValue) / LHTZValue) * 100;
        var diffCell = document.createElement("td");
        diffCell.innerHTML = percentageDiff.toFixed(2);
        row.appendChild(diffCell);

        table.appendChild(row);
    }
}

function updateTableAsym(TZ_asym, chartData, table) {
    var LHTZ_FLchartData = chartData[0]
    var LHTZ_BLchartData = chartData[1]
    var RHTZ_FLchartData = chartData[2]
    var RHTZ_BLchartData = chartData[3]

    // Clear the existing content of the table
    table.innerHTML = "";

    // Create the table headers
    var headers = ["Test number", "LHTZ FL (kg)", "LHTZ BL (kg)", "RHTZ FL (kg)", "RHTZ BL (kg)", "Asymmetry (%)"];
    var headerRow = document.createElement("tr");
    for (var i = 0; i < headers.length; i++) {
        var headerCell = document.createElement("th");
        headerCell.innerHTML = headers[i];
        headerRow.appendChild(headerCell);
    }
    table.appendChild(headerRow);

    // Create the table rows
    for (var i = 0; i < TZ_asym.length; i++) {
        var row = document.createElement("tr");
        var testCell = document.createElement("td");
        testCell.innerHTML = i+1;
        row.appendChild(testCell);

        var LHTZFLValue = LHTZ_FLchartData[i];
        var RHTZFLValue = RHTZ_FLchartData[i];
        var LHTZBLValue = LHTZ_BLchartData[i];
        var RHTZBLValue = RHTZ_BLchartData[i];

        var LHTZFLCell = document.createElement("td");
        LHTZFLCell.innerHTML = LHTZFLValue;
        row.appendChild(LHTZFLCell);
        var LHTZBLCell = document.createElement("td");
        LHTZBLCell.innerHTML = LHTZBLValue;
        row.appendChild(LHTZBLCell);
        var RHTZFLCell = document.createElement("td");
        RHTZFLCell.innerHTML = RHTZFLValue;
        row.appendChild(RHTZFLCell);
        var RHTZBLCell = document.createElement("td");
        RHTZBLCell.innerHTML = RHTZBLValue;
        row.appendChild(RHTZBLCell);

        var percentageDiff = TZ_asym[i]
        var diffCell = document.createElement("td");
        diffCell.innerHTML = percentageDiff.toFixed(2);
        row.appendChild(diffCell);

        table.appendChild(row);
    }
}

function createActivityTable(table, dates, testsCompleted, name, squad, protocol) {
  // Clear the existing content of the table
  table.innerHTML = "";

  // Create the table headers
  var headers = ["Name", "Squad", "Total sessions", "Last session date", "Last session protocol"];
  var headerRow = document.createElement("tr");
  for (var i = 0; i < headers.length; i++) {
    var headerCell = document.createElement("th");
    headerCell.innerHTML = headers[i];
    headerRow.appendChild(headerCell);
  }
  table.appendChild(headerRow);

  // Create the table row for the player
  var playerRow = document.createElement("tr");

  var nameCell = document.createElement("td");
  nameCell.innerHTML = name;
  playerRow.appendChild(nameCell);

  var squadCell = document.createElement("td");
  squadCell.innerHTML = squad;
  playerRow.appendChild(squadCell);

  var totalTestsCell = document.createElement("td");
  totalTestsCell.innerHTML = testsCompleted;
  playerRow.appendChild(totalTestsCell);

  var mostRecentDateCell = document.createElement("td");
  mostRecentDateCell.innerHTML = dates;
  playerRow.appendChild(mostRecentDateCell);

  var mostRecentProtocolCell = document.createElement("td");
  mostRecentProtocolCell.innerHTML = protocol;
  playerRow.appendChild(mostRecentProtocolCell);

  table.appendChild(playerRow);

  return table
}

function updateOverviewBarData(chart, timeframe, chartData) {
  chart.data.datasets[0].data = chartData[timeframe]['FL'];
  chart.data.datasets[1].data = chartData[timeframe]['BL'];
  chart.update();
}

function updateOverviewBarData2(chart, timeframe, dataType, chartData) {
    chart.data.datasets[0].data = [Math.max(chartData[timeframe]['LHTZ FL'][dataType]),
                                    Math.max(chartData[timeframe]['RHTZ FL'][dataType])];
    chart.data.datasets[1].data = [Math.max(chartData[timeframe]['LHTZ BL'][dataType]),
                                    Math.max(chartData[timeframe]['RHTZ BL'][dataType])];
    chart.update();
}

function updateOverviewLineData(chart, type, timeframe, dataType, chartData) {
  if (type === 'dropoff') {
    chart.data.datasets[0].data = chartData[timeframe]['LHTZ FL'][dataType];
    chart.data.datasets[1].data = chartData[timeframe]['LHTZ BL'][dataType];
    chart.data.datasets[2].data = chartData[timeframe]['RHTZ FL'][dataType];
    chart.data.datasets[3].data = chartData[timeframe]['RHTZ BL'][dataType];

    chart.update();
  } else if (type === 'asymmetry') {
    chart.data.datasets[0].data = chartData[timeframe]['Front leg'][dataType];
    chart.data.datasets[1].data = chartData[timeframe]['Back leg'][dataType];
    chart.data.datasets[2].data = chartData[timeframe]['TZ'][dataType];

    chart.update();
  }
  chart.options.plugins.tooltip.callbacks.label = function (context) {
      var index = context.dataIndex; // Get the index of the selected data point
      var datasetIndex = context.datasetIndex; // Get the index of the selected dataset
      var datasetKey = Object.keys(chartData[timeframe])[datasetIndex]; // Get the key of the selected dataset
      var value = chartData[timeframe][datasetKey][dataType][index]; // Get the value from chartData

      // Display tooltip label with value
      return datasetKey + ': ' + value + '%';
    };

    chart.options.plugins.tooltip.callbacks.footer = function (context) {
                        var index = context[0].dataIndex; // Get the index of the selected data point
                        var protocol = chartData[timeframe]['protocol'][index]; // Get the protocol from chartData
                        var matchday = chartData[timeframe]['matchday'][index]; // Get the matchday from chartData
                        var config = chartData[timeframe]['config'][index]; // Get the config from chartData
                        var strategy = chartData[timeframe]['strategy'][index]; // Get the strategy from chartData

                        // Display footer with additional data
                        return 'Protocol: ' + protocol +'\nMatchday: ' + matchday +'\nConfig: ' + config +'\nStrategy: ' + strategy;
                    };
  chart.data.labels = chartData[timeframe]['labels'];
  chart.update();
}

function updateButtonColor(selectedButton) {
    // Reset color for all buttons
    avgButton.classList.remove('selected');
    maxButton.classList.remove('selected');
    // Set color for the selected button
    selectedButton.classList.add('selected');
}


function getScoresFromSessions(data, metric, type) {
  var FLstring = 'Front leg ' + metric;
  var BLstring = 'Back leg ' + metric;
  var LHTZmaxFL = [];
  var LHTZmaxBL = [];
  var RHTZmaxFL = [];
  var RHTZmaxBL = [];
  var labels = []

  for (var session in data) {
    LHTZmaxFL.push(data[session]['LHTZ'][type][FLstring]);
    LHTZmaxBL.push(data[session]['LHTZ'][type][BLstring]);
    RHTZmaxFL.push(data[session]['RHTZ'][type][FLstring]);
    RHTZmaxBL.push(data[session]['RHTZ'][type][BLstring]);
    labels.push(session)
  }

  return [LHTZmaxFL, RHTZmaxFL, LHTZmaxBL, RHTZmaxBL, labels];
}

function getSessionData2(playerSessions, selectedSession) {
    let LHTZ_data = {
        'session':{
        'index': playerSessions[selectedSession]['LHTZ']['session']['index'],
        'Front leg RFD 50-150ms': playerSessions[selectedSession]['LHTZ']['session']['Front leg RFD 50-150ms'],
        'Front leg force at 150ms': playerSessions[selectedSession]['LHTZ']['session']['Front leg force at 150ms'],
        'Front leg peak force': playerSessions[selectedSession]['LHTZ']['session']['Front leg peak force'],
        'Back leg RFD 50-150ms': playerSessions[selectedSession]['LHTZ']['session']['Back leg RFD 50-150ms'],
        'Back leg force at 150ms': playerSessions[selectedSession]['LHTZ']['session']['Back leg force at 150ms'],
        'Back leg peak force': playerSessions[selectedSession]['LHTZ']['session']['Back leg peak force'],
        'Combined RFD 50-150ms': playerSessions[selectedSession]['LHTZ']['session']['Combined RFD 50-150ms'],
        'Crush factor at 150ms': playerSessions[selectedSession]['LHTZ']['session']['Crush factor at 150ms'],
        'Peak crush factor': playerSessions[selectedSession]['LHTZ']['session']['Peak crush factor']
        }
        };

    let RHTZ_data = {
        'session':{
        'index': playerSessions[selectedSession]['RHTZ']['session']['index'],
        'Front leg RFD 50-150ms': playerSessions[selectedSession]['RHTZ']['session']['Front leg RFD 50-150ms'],
        'Front leg force at 150ms': playerSessions[selectedSession]['RHTZ']['session']['Front leg force at 150ms'],
        'Front leg peak force': playerSessions[selectedSession]['RHTZ']['session']['Front leg peak force'],
        'Back leg RFD 50-150ms': playerSessions[selectedSession]['RHTZ']['session']['Back leg RFD 50-150ms'],
        'Back leg force at 150ms': playerSessions[selectedSession]['RHTZ']['session']['Back leg force at 150ms'],
        'Back leg peak force': playerSessions[selectedSession]['RHTZ']['session']['Back leg peak force'],
        'Combined RFD 50-150ms': playerSessions[selectedSession]['RHTZ']['session']['Combined RFD 50-150ms'],
        'Crush factor at 150ms': playerSessions[selectedSession]['RHTZ']['session']['Crush factor at 150ms'],
        'Peak crush factor': playerSessions[selectedSession]['RHTZ']['session']['Peak crush factor']
        }
        };

    let test_info = {
        'Protocol': playerSessions[selectedSession]['LHTZ']['session']['Protocol'],
        'Matchday': playerSessions[selectedSession]['LHTZ']['session']['Matchday'],
        'Strategy': playerSessions[selectedSession]['LHTZ']['session']['Strategy'],
        'Phase': playerSessions[selectedSession]['LHTZ']['session']['Phase']
    };

    return {'LHTZ': LHTZ_data, 'RHTZ': RHTZ_data, 'Tags': test_info}
}


function updateChartDataSession2(sessionData, metric, chart) {
    console.log(sessionData)
    // Update the data for the LHTZ dataset
    chart.data.datasets[0].data = sessionData['LHTZ']['session'][metric];
    // Update the data for the RHTZ dataset
    chart.data.datasets[1].data = sessionData['RHTZ']['session'][metric];

    var labels = []
    var rows = Math.max(sessionData['LHTZ']['session']['index'].length, sessionData['RHTZ']['session']['index'].length);
    for (var i = 0; i < rows; i++) {
        labels.push(i+1)
    }

    chart.options.plugins.tooltip.callbacks.footer = function (context) {
                        var index = context[0].dataIndex; // Get the index of the selected data point
                        var protocol = sessionData['Tags']['Protocol'][index]; // Get the protocol from chartData
                        var matchday = sessionData['Tags']['Matchday'][index]; // Get the matchday from chartData
                        var config = sessionData['Tags']['Phase'][index]; // Get the config from chartData
                        var strategy = sessionData['Tags']['Strategy'][index]; // Get the strategy from chartData

                        // Display footer with additional data
                        return 'Protocol: ' + protocol +'\nMatchday: ' + matchday +'\nConfig: ' + config +'\nStrategy: ' + strategy;
                    };

    chart.data.labels = labels
    // Update the chart
    chart.update();
}

function updateTable2(sessionData, metric, table) {
    // Clear the existing content of the table
    table.innerHTML = "";

    // Create the table headers
    var headers = ["Test number", "LHTZ score (kg)", "RHTZ score (kg)", "Asymmetry (%)"];
    var rows = Math.max(sessionData['LHTZ']['session']['index'].length, sessionData['RHTZ']['session']['index'].length);

    var headerRow = document.createElement("tr");
    for (var i = 0; i < headers.length; i++) {
        var headerCell = document.createElement("th");
        headerCell.innerHTML = headers[i];
        headerRow.appendChild(headerCell);
    }
    table.appendChild(headerRow);

    // Create the table rows
    for (var i = 0; i < rows; i++) {
        var row = document.createElement("tr");
        var testCell = document.createElement("td");
        testCell.innerHTML = i+1;
        row.appendChild(testCell);

        var LHTZValue = sessionData['LHTZ']['session'][metric][i];
        var RHTZValue = sessionData['RHTZ']['session'][metric][i];
        var LHTZCell = document.createElement("td");
        LHTZCell.innerHTML = LHTZValue;
        row.appendChild(LHTZCell);

        var RHTZCell = document.createElement("td");
        RHTZCell.innerHTML = RHTZValue;
        row.appendChild(RHTZCell);

        var percentageDiff = ((RHTZValue - LHTZValue) / RHTZValue) * 100;
        var diffCell = document.createElement("td");
        diffCell.innerHTML = percentageDiff.toFixed(2);
        row.appendChild(diffCell);

        table.appendChild(row);
    }
}


function getRadarData(playerSessions) {
  const sessions = Object.keys(playerSessions);
  console.log(sessions)
  const lastSession = sessions[sessions.length -1];
  console.log(lastSession)
  var peakScores = [];
  var f150Scores = [];
  var rfdScores = [];
  var asymScores = [];
  for (var session in playerSessions) {
    var PeakL = playerSessions[session]['LHTZ']['avg']['Peak crush factor'][0]
    var PeakR = playerSessions[session]['RHTZ']['avg']['Peak crush factor'][0]
    var PeakScore = (PeakL+PeakR)/6
    peakScores.push(PeakScore)

    var F150L = playerSessions[session]['LHTZ']['avg']['Crush factor at 150ms'][0]
    var F150R = playerSessions[session]['RHTZ']['avg']['Crush factor at 150ms'][0]
    var F150Score = (F150L+F150R)/2.4
    f150Scores.push(F150Score)

    var RFDL = playerSessions[session]['LHTZ']['avg']['Combined RFD 50-150ms'][0]
    var RFDR = playerSessions[session]['RHTZ']['avg']['Combined RFD 50-150ms'][0]
    var RFDScore = (RFDL+RFDR)/12.5
    rfdScores.push(RFDScore)

    var AsymP = playerSessions[session]['Asymmetry']['avg']['Peak crush factor'][0]
    var AsymF = playerSessions[session]['Asymmetry']['avg']['Crush factor at 150ms'][0]
    var AsymR = playerSessions[session]['Asymmetry']['avg']['Combined RFD 50-150ms'][0]
    var AsymScore = 100-(Math.abs(AsymP+AsymF+AsymR)/3)
    asymScores.push(AsymScore)

    if (session === lastSession) {
        var lsPeak = PeakScore
        var lsF150 = F150Score
        var lsRFD = RFDScore
        var lsAsym = AsymScore
    };
  };

  if (lsPeak > 100) {
    lsPeak = 100
  };
  if (lsF150 > 100) {
    lsF150 = 100
  };
  if (lsRFD > 100) {
    lsRFD = 100
  };
  if (lsAsym < 0) {
    lsAsym = 0
  };

  var atPeak = Math.max(...peakScores);
  var atF150 = Math.max(...f150Scores);
  var atRFD = Math.max(...rfdScores);
  var atAsym = Math.max(...asymScores);
  if (atPeak > 100) {
    atPeak = 100
  };
  if (atF150 > 100) {
    atF150 = 100
  };
  if (atRFD > 100) {
    atRFD = 100
  };
  if (atAsym < 0) {
    atAsym = 1
  };

  let radarData = {
    'last-session': {
      'Peak force': lsPeak,
      'Force at 150ms': lsF150,
      'RFD': lsRFD,
      'Transition zone similarity': lsAsym
    },
    'PB': {
      'Peak force': atPeak,
      'Force at 150ms': atF150,
      'RFD': atRFD,
      'Transition zone similarity': atAsym
    }
  };

  console.log(radarData)

  return radarData;
}


function extendDatesAndNumTests(dates, numTests) {
  const currentDate = new Date(); // Get the current date
  currentDate.setHours(0, 0, 0, 0); // Set the time to midnight for accurate comparison

  const extendedDates = [...dates]; // Create a copy of the original dates array
  const extendedNumTests = [...numTests]; // Create a copy of the original numTests array

  let date = new Date(dates[dates.length - 1]); // Start with the last date in the original array

  // Extend the arrays until we have a total of 100 dates or reach the current date
  while (extendedDates.length < 100 && date < currentDate) {
    date.setDate(date.getDate() + 1); // Increment the date by one day
    const formattedDate = date.toISOString().split('T')[0]; // Convert the date to string format 'YYYY-MM-DD'

    extendedDates.push(formattedDate); // Add the extended date to the array
    extendedNumTests.push(0); // Add a value of zero for the extended date
  }

  return {
    dates: extendedDates,
    numTests: extendedNumTests
  };
}


function getProgressData(playerSessions, sessionList) {
    const sessions = Object.keys(playerSessions);
    var peakProg = [];
    var f150Prog = [];
    var rfdProg = [];

    var peakAsymProg = [];
    var f150AsymProg = [];
    var rfdAsymProg = [];

    var strategy = [];
    var matchday = [];
    var phase = [];
    var sessionNames = []

    var count = sessionList.length;
    for(var i = 0; i < count; i++) {
        var session = sessionList[i];
        sessionNames.push(session)
        var PeakL = playerSessions[session]['LHTZ']['avg']['Peak crush factor'][0];
        var PeakR = playerSessions[session]['RHTZ']['avg']['Peak crush factor'][0];
        var PeakScore = PeakL + PeakR;
        peakProg.push(PeakScore);
        strategy.push(playerSessions[session]['LHTZ']['session']['Strategy'][0])
        matchday.push(playerSessions[session]['LHTZ']['session']['Matchday'][0])
        phase.push(playerSessions[session]['LHTZ']['session']['Phase'][0])

        var PeakAsym = playerSessions[session]['Asymmetry']['avg']['Peak crush factor'][0];
        peakAsymProg.push(PeakAsym);

        var F150L = playerSessions[session]['LHTZ']['avg']['Crush factor at 150ms'][0];
        var F150R = playerSessions[session]['RHTZ']['avg']['Crush factor at 150ms'][0];
        var F150Score = F150L + F150R;
        f150Prog.push(F150Score);

        var f150Asym = playerSessions[session]['Asymmetry']['avg']['Crush factor at 150ms'][0];
        f150AsymProg.push(f150Asym);

        var RFDL = playerSessions[session]['LHTZ']['avg']['Combined RFD 50-150ms'][0];
        var RFDR = playerSessions[session]['RHTZ']['avg']['Combined RFD 50-150ms'][0];
        var RFDScore = RFDL + RFDR;
        rfdProg.push(RFDScore);

        var rfdAsym = playerSessions[session]['Asymmetry']['avg']['Combined RFD 50-150ms'][0];
        rfdAsymProg.push(rfdAsym);
    };

    return {
        'labels': sessionNames,
        'Peak force': peakProg,
        'Force at 150ms': f150Prog,
        'RFD 50-150ms': rfdProg,
        'Peak force asymmetry': peakAsymProg,
        'Force at 150ms asymmetry': f150AsymProg,
        'RFD 50-150ms asymmetry': rfdAsymProg,
        'Strategy': strategy,
        'Matchday': matchday,
        'Phase': phase
    };
}

function updateChartLegendProgress(progressData, chart) {

    chart.options.plugins.tooltip.callbacks.footer = function (context) {
        var index = context[0].dataIndex; // Get the index of the selected data point
        var matchday = progressData['Matchday'][index]; // Get the matchday from chartData
        var config = progressData['Phase'][index]; // Get the config from chartData
        var strategy = progressData['Strategy'][index]; // Get the strategy from chartData

        // Display footer with additional data
        return 'Matchday: ' + matchday +'\nConfig: ' + config +'\nStrategy: ' + strategy;
    };

    chart.update();
}

function getPlayerMaxScores(playerSessions) {
  const sessions = Object.keys(playerSessions);
  const lastSession = sessions[sessions.length - 1];

  const metrics = ['Peak crush factor', 'Front leg peak force', 'Back leg peak force', 'Crush factor at 150ms', 'Front leg force at 150ms', 'Back leg force at 150ms', 'Combined RFD 50-150ms', 'Front leg RFD 50-150ms', 'Back leg RFD 50-150ms'];

  const maxScores = {
    'Best all-time': {},
    'Best last session': {}
  };

  for (const session in playerSessions) {
    const isLastSession = session === lastSession;

    for (const metric of metrics) {
      for (const TZ of ['LHTZ', 'RHTZ']) {
        if (!maxScores['Best all-time'][metric]) {
          maxScores['Best all-time'][metric] = {};
        }
        if (!maxScores['Best all-time'][metric][TZ]) {
          maxScores['Best all-time'][metric][TZ] = [];
        }

        if (isLastSession) {
          if (!maxScores['Best last session'][metric]) {
            maxScores['Best last session'][metric] = {};
          }
          if (!maxScores['Best last session'][metric][TZ]) {
            maxScores['Best last session'][metric][TZ] = [];
          }
        }

        const score = playerSessions[session][TZ]['max'][metric];
        maxScores['Best all-time'][metric][TZ].push(score);

        if (isLastSession) {
          maxScores['Best last session'][metric][TZ].push(score);
        }
      }
    }
  }

  for (const key in maxScores) {
    for (const metric in maxScores[key]) {
      for (const TZ in maxScores[key][metric]) {
        maxScores[key][metric][TZ] = [Math.max(...maxScores[key][metric][TZ])];
      }
    }
  }

  return maxScores;
}


function getDropoffFromMax(type, leg, protocol, strategy, phase, day, timeframe, session, playerSessions, maxScores) {
    var metric = leg === 'Combined legs' ? (type === 'peak force' ? 'Peak crush factor' : type === 'force at 150ms' ? 'Crush factor at 150ms' :  'Combined ' + type) : leg + ' ' + type;

    var maxScoreObj = maxScores[timeframe][metric];
    var score = { 'LHTZ': [], 'RHTZ': [] };
    var dropoff = { 'LHTZ': [], 'RHTZ': [] };

    ['LHTZ', 'RHTZ'].forEach(function (side) {
        playerSessions[session][side]['session']['Protocol'].forEach(function (val, i) {
            if (
                (strategy === playerSessions[session][side]['session']['Strategy'][i] || strategy === 'All strategies') &&
                (phase === playerSessions[session][side]['session']['Phase'][i] || strategy === 'All configs') &&
                (day === playerSessions[session][side]['session']['Matchday'][i] || strategy === 'Any day') &&
                (protocol === val || strategy === 'Any protocol')
            ) {
                score[side].push(playerSessions[session][side]['session'][metric][i]);
            }
        });

        score[side].push(Math.max(...score[side]));
        var dropoffVal = Math.abs(maxScoreObj[side] - score[side][0]) / ((maxScoreObj[side][0] + score[side][0]) / 2);
        dropoff[side].push(dropoffVal);
    });

    return {
        'score': score,
        'dropoff': dropoff
    };
}

function getProgressTooltipLists(playerSessions, selectedSessions) {
    var phaseList = [];
    var stratList = [];
    var matchList = [];
    var sessionList = []
    for (var session of selectedSessions) {
        phaseList.push(...playerSessions[session]['LHTZ']['session']['Phase'])
        stratList.push(...playerSessions[session]['LHTZ']['session']['Strategy'])
        matchList.push(...playerSessions[session]['LHTZ']['session']['Matchday'])

        for (var i of playerSessions[session]['LHTZ']['session']['index']) {
            sessionList.push(session)
        }
    }

    return {
        'session': sessionList,
        'strategy': stratList,
        'phase': phaseList,
        'match': matchList
    }
}




