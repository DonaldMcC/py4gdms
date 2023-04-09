
<div class="ganttdiv">
<link rel="stylesheet" href="[[=URL('static','css/jsgantt.css')]]">
<script src="[[=URL('static','js/jsgantt.js')]]"></script>


<h1 class="title h4">Action Gantt Chart <INPUT TYPE=BUTTON id="key" class="button btn-sm btn-outline btn-warning" onClick="edit_click()" data-toggle =" popover"
title ="Toggle to turn on or off editing the Gantt chart" data-content="" VALUE="Edit"></h1>
<div style="position:relative" class="gantt" id="GanttChartDIV"></div>
</div>
 <script>
 [[include 'gantt.js']]
 </script>
