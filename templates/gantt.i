<link rel="stylesheet" href="[[=URL('static','css/jsgantt.css')]]"/>
<script src="[[=URL('static','js/jsgantt.js')]]"></script>

<h1 class="title is-4">Action Gantt Chart</h1>
<div style="position:relative" class="gantt" id="GanttChartDIV"></div>

<script>
var g = new JSGantt.GanttChart(document.getElementById('GanttChartDIV'), 'day');
g.setShowTaskInfoLink(1);
g.setEditable(1);
var textstring = "[[=project]]"
JSGantt.parseXMLString(textstring,g);
g.Draw();
</script>