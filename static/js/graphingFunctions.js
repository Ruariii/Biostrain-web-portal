// SINGLE SESSION FILTER FUNCTION
function filterDataSession(metric, LHTZ_data, RHTZ_data) {
    // Filter the data based on the selected metric
    var LHTZ_filteredData = LHTZ_data['session'][metric];
    var RHTZ_filteredData = RHTZ_data['session'][metric];

    // Return the filtered data
    return {'LHTZ': LHTZ_filteredData, 'RHTZ': RHTZ_filteredData};
}
function updateChartDataSession(filteredData, chart) {
    // Update the data for the LHTZ dataset
    chart.data.datasets[0].data = filteredData['LHTZ'];
    // Update the data for the RHTZ dataset
    chart.data.datasets[1].data = filteredData['RHTZ'];
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

    // Return the filtered data
    return {'LHTZ': LHTZ_data, 'RHTZ': RHTZ_data};
}

function updateChartDataHistorical(filteredData, chart) {
    // Update the data for the LHTZ dataset
    chart.data.datasets[0].data = filteredDataHistorical['LHTZ'];
    // Update the data for the RHTZ dataset
    chart.data.datasets[1].data = filteredDataHistorical['RHTZ'];
    // Update the chart
    chart.update();
}

function updateTableHistorical(filteredData4, table, session_names2) {
    // Clear the existing content of the table
    table.innerHTML = "";

    // Create the table headers
    var headers = ["Test number", "LHTZ score (kg)", "RHTZ score (kg)", "Asymmetry (%)"];
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
        testCell.innerHTML = session_names[i];
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
    var headerRow = document.createElement("tr");
    for (var i = 0; i < headers.length; i++) {
        var headerCell = document.createElement("th");
        headerCell.innerHTML = headers[i];
        headerRow.appendChild(headerCell);
    }
    table.appendChild(headerRow);

    // Create the table rows
    for (var i = 0; i < labels.length; i++) {
        var row = document.createElement("tr");
        var testCell = document.createElement("td");
        testCell.innerHTML = labels[i];
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
