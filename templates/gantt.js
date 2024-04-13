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


g.setOptions({
// EVENTS

  // OnChangee
  vEventsChange: {
    taskname: console.log,
    res: console.log,
  },
  // EventsClickCell
  vEvents: {
    taskname: console.log,
    res: console.log,
    dur: console.log,
    comp: console.log,
    start: console.log,
    end: console.log,
    planstart: console.log,
    planend: console.log,
    cost: console.log,
    additional_category: console.log, // for additional fields
    beforeDraw: ()=>console.log('before draw listener'),
    afterDraw: ()=>console.log('before after listener')
  },
  vEventClickRow: console.log,
  vEventClickCollapse: console.log
});

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

/* now found some events and added in with console logging for now */
/* hopefully new ajax function similar to ones on the actions grid to update */
/* dates and so forth on change */
/* https://github.com/jsGanttImproved/jsgantt-improved/pull/61  and demo may help*/
/*https://github.com/jsGanttImproved/jsgantt-improved/blob/master/docs/index.js#L78 */
/*https://github.com/jsGanttImproved/jsgantt-improved/blob/master/docs/index.js#L199*/
