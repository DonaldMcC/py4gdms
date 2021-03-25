var g = new JSGantt.GanttChart(document.getElementById('GanttChartDIV'), 'day');


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


g.setShowTaskInfoLink(1);
g.setEditable(0);
var textstring = "[[=project]]"
JSGantt.parseXMLString(textstring,g);
g.Draw();


function editValue(list, task, event, cell, column) {
    console.log('editing');
  /*console.log(list, task, event, cell, column);*/
  const found = list.find(item => item.pID == task.getOriginalID());
  if (!found) {
    return;
  }
  else {
    found[column] = event ? event.target.value : '';
  }
}

/* struggling to find any sort of after edit event - so think we will just have a save button and export
XML as an option after updating
 */
/* https://github.com/jsGanttImproved/jsgantt-improved/pull/61  and demo may help*/
/*https://github.com/jsGanttImproved/jsgantt-improved/blob/master/docs/index.js#L78 */
/*https://github.com/jsGanttImproved/jsgantt-improved/blob/master/docs/index.js#L199*/
