<div>
<table id='EvtDetails' class="table">
<thead>
<tr class="table-primary">
<th>Event Name</th>
<th>[[=eventrow.event_name]]</th>
<th>Start</th>
<th>End</th>
</tr>
</thead>
<tbody>
<tr class='is-selected'>
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
<td id="eventstatus">[[=eventrow.status]]</td>
<td>Next Event</td>
<td> [[if eventrow.next_event==0:]]
    <INPUT TYPE=button class="btn btn-primary" id="next_event" onclick="nextevent('[[=eventrow.id]]',this)", VALUE="Create Next Event">
    [[else:]]
    [[=A(next_event_name, _href=URL('view_event/'+str(next_event_id)))]]</th>
    [[pass]]</td>
</tr>
<tr>
<th></th>
<td><INPUT TYPE=button class="btn btn-primary"
           onClick="parent.location='[[=URL('new_question/None/issue/'+str(eventid)+'/0/0/view_event')]]'" VALUE="New Issue">
</td>
    <td><INPUT TYPE=button class="btn btn-success"
           onClick="parent.location='[[=URL('new_question/None/quest/'+str(eventid)+'/0/0/view_event')]]'" VALUE="New Question">
</td>
    <td><INPUT TYPE=button class="btn btn-warning"
           onClick="parent.location='[[=URL('new_question/None/action/'+str(eventid)+'/0/0/view_event')]]'" VALUE="New Action">
</td>
</tr>
</tbody>
</table>
</div>