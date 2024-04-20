
<div class="ganttdiv">
<link rel="stylesheet" href="[[=URL('static','css/jsgantt.css')]]">
<script src="[[=URL('static','js/jsgantt.js')]]"></script>


<h1 class="title h4">Action Gantt Chart <INPUT TYPE=BUTTON id="key" class="button btn-sm btn-warning" onClick="edit_click()" data-toggle =" popover"
title ="Toggle to turn on or off editing the Gantt chart" data-content="" VALUE="Edit">
<INPUT TYPE=BUTTON id="exportkey" class="button btn-sm  btn-info" onClick="exportGantt()" data-toggle =" popover"
title ="Toggle to turn on or off editing the Gantt chart" data-content="" VALUE="Save"></h1>
<div style="position:relative" class="gantt" id="GanttChartDIV"></div>
</div>
 <script>
 [[include 'gantt.js']]
 </script>
