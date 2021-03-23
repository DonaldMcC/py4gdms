<link rel="stylesheet" href="[[=URL('static','css/jsgantt.css')]]"/>
<script src="[[=URL('static','js/jsgantt.js')]]"></script>

<h1 class="title is-4">Action Gantt Chart <INPUT TYPE=BUTTON id="key" class="button is-small is-outlined is-rounded is-warning " onClick="edit_click()" data-toggle =" popover"
title ="Toggle to turn on or off editing the Gantt chart" data-content="" VALUE="Edit"></h1>
<div style="position:relative" class="gantt" id="GanttChartDIV"></div>

<script>
var g = new JSGantt.GanttChart(document.getElementById('GanttChartDIV'), 'day');
g.setShowTaskInfoLink(1);
g.setEditable(0);
var textstring = "[[=project]]"
JSGantt.parseXMLString(textstring,g);
g.Draw();

function edit_click() {
    console.log($('#key').val());
    if ($('#key').val()=='Edit') {
        g.setEditable(1);
        $('#key').prop('value', 'Lock');
        }
    else {
      $('#key').prop('value', 'Edit');
    g.setEditable(0);
    };

    g.Draw();
};
</script>