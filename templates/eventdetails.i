<div>
<table id='EvtDetails' class="table table-bordered border-info">
<thead>
<tr class="table-info">
<th>Event Name</th>
<th>[[=eventrow.event_name]]</th>
<th>Start</th>
<th>End</th>
</tr>
</thead>
<tbody>
<tr>
    <th>Description</th>
<td>[[=XML(markmin2html(eventrow.description))]]</td>
<td class="text-center">[[=eventrow.startdatetime.strftime('%a %d %b %Y %H:%M')]]</td>
<td class="text-center">[[=eventrow.enddatetime.strftime('%a %d %b %Y %H:%M')]]</td>
</tr>
<tr>
<th>Project</th>
<td>[[=eventrow.projid.proj_name]]</td>
<td>Location</td>
<td>[[=eventrow.locationid.location_name]]</td>
</tr>
<tr>
<th>Status: </th>
<td id="eventstatus">[[=eventrow.status]]
    [[if eventrow.status == 'Open':]]
<a class="btn btn-sm btn-outline-info" id="eventarchive" data-title="C" data-bs-toggle="modal" data-bs-target="#ArchiveModal">Archive</a>
[[pass]]
</td>
<td>Next Event</td>
<td id='nextevent'> [[if eventrow.next_event==0:]]
    <INPUT TYPE=button class="btn btn-primary" id="next_event" onclick="nextevent('[[=eventrow.id]]',this)", VALUE="Create Next Event">
    [[else:]]
    [[=A(next_event_name, _href=URL('view_event/'+str(next_event_id)))]]</th>
    [[pass]]</td>
</tr>
<tr>
<th></th>
<td><INPUT TYPE=button class="btn btn-primary"
           onClick="parent.location='[[=URL('new_question/None/issue/'+str(eventid)+'/0/0/view_event/')]]'" VALUE="New Issue">
</td>
    <td><INPUT TYPE=button class="btn btn-success"
           onClick="parent.location='[[=URL('new_question/None/quest/'+str(eventid)+'/0/0/view_event/')]]'" VALUE="New Question">
</td>
    <td><INPUT TYPE=button class="btn btn-warning"
           onClick="parent.location='[[=URL('new_question/None/action/'+str(eventid)+'/0/0/view_event/')]]'" VALUE="New Action">
</td>
</tr>
</tbody>
</table>
</div>
<div class="modal fade" id="ArchiveModal" tabindex="-1">
  <div class="modal-dialog"></div>
  <div class="modal-content">
      <div class="modal-header">
          <h5 class="modal-title">Archive Event</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
       <div class="modal-body">This set the archiving event to archived which permanently locks the outcome - make sure everything is
            set before doing this as it cannot be undone. Archived status returns resolved questions and disagreed issues
             to the unspecified event but agreed issues, unresolved questions and actions which are not completed will
              roll-forward to the next event
               [[if not eventrow.next_event:]] WARNING: this event does not currently have a next event set.[[else:]]
        which has been created for this project.[[pass]]
            </div>
       <div class="modal-footer">
           <button type="button" id="modal_archive" class="btn btn-small btn-warning" data-bs-dismiss="modal"
                  onclick="archive('[[=eventrow.id]]')">Save changes</button>
                   <button type="button" class="btn btn-small btn-info" data-bs-dismiss="modal">Close</button>

       </div>
           </div>
  </div>
</div>