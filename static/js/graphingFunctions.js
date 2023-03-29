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
    const fl150L = [];
    const fl150R = [];
    const flpeakL = [];
    const flpeakR = [];
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


function getAsymMetric(metricType, LHTZ_data, RHTZ_data) {

    if (metricType == 'Peak force'){
        var LHTZ_FLchartData = LHTZ_data['session']['Front leg peak force'];
        var LHTZ_BLchartData = LHTZ_data['session']['Back leg peak force'];
        var RHTZ_FLchartData = RHTZ_data['session']['Front leg peak force'];
        var RHTZ_BLchartData = RHTZ_data['session']['Back leg peak force'];
    }
    else if (metricType == 'Force at 150ms'){
        var LHTZ_FLchartData = LHTZ_data['session']['Front leg force at 150ms'];
        var LHTZ_BLchartData = LHTZ_data['session']['Back leg force at 150ms'];
        var RHTZ_FLchartData = RHTZ_data['session']['Front leg force at 150ms'];
        var RHTZ_BLchartData = RHTZ_data['session']['Back leg force at 150ms'];
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
        var asym = 100*(((RHTZ_FLchartData[i]+RHTZ_BLchartData[i])-(LHTZ_FLchartData[i]+LHTZ_BLchartData[i]))/(LHTZ_FLchartData[i]+LHTZ_BLchartData[i]))
        TZ_asym.push(asym)
        }
        }
    else if (asymType == "Front leg"){
        for (var i = 0; i < LHTZ_FLchartData.length; i++) {
        var asym = 100*(((RHTZ_FLchartData[i])-(LHTZ_FLchartData[i]))/(LHTZ_FLchartData[i]))
        TZ_asym.push(asym)
        }
        }
    else if (asymType == "Back leg"){
        for (var i = 0; i < LHTZ_BLchartData.length; i++) {
        var asym = 100*(((RHTZ_BLchartData[i])-(LHTZ_BLchartData[i]))/(LHTZ_BLchartData[i]))
        TZ_asym.push(asym)
        }
    }

    return TZ_asym
}

function updateChartDataAsym(TZ_asym, chartData, chart){

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

function updateChartDataHistorical(filteredData, chart, session_names) {
    // Update the data for the LHTZ dataset
    chart.data.datasets[0].data = filteredData['LHTZ'];
    // Update the data for the RHTZ dataset
    chart.data.datasets[1].data = filteredData['RHTZ'];


    chart.data.labels = session_names
    // Update the chart
    chart.update();
}

// HISTORICAL FILTER FUNCTION
function filterDataHistorical(data, metric, dataDict) {
    // Extract the data for the chart
    var LHTZ_data = [];
    var RHTZ_data = [];
    for (var session in dataDict) {
      LHTZ_data.push(dataDict[session]['LHTZ'][data][metric][0]);
      RHTZ_data.push(dataDict[session]['RHTZ'][data][metric][0]);
    }
    var rows = Math.max(RHTZ_data.length, LHTZ_data.length);

    // Return the filtered data
    return {'LHTZ': LHTZ_data, 'RHTZ': RHTZ_data, 'length': rows};
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
    for (var i = 0; i < session_names2.length; i++) {
        var row = document.createElement("tr");
        var testCell = document.createElement("td");
        testCell.innerHTML = session_names2[i];
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

