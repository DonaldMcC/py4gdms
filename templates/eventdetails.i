<div>
<h1 class="title is-5">Event Details</h1>
<table id='TabAnswers' class='table'>
<tbody>
<tr>
<th></th>
<th>[[=eventrow.event_name]]</th>
<th>Start</th>
<th>End</th>
</tr>
<tr class='is-selected'>
<th>Description</th>
<td>[[=eventrow.description]]</td>
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
    <INPUT TYPE=button class="button is-small is-rounded" onclick="nextevent('[[=eventrow.id]]',this)", VALUE="Create Next Event">
    [[else:]]
    [[=A(next_event_name, _href=URL('view_event/'+str(next_event_id)))]]</th>
    [[pass]]</td>
</tr>
<tr>
<th>Create</th>
<td><INPUT TYPE=button class="button is-small is-success is-rounded"
           onClick="parent.location='[[=URL('new_question/None/issue')]]'"VALUE="New Issue">
</td>
    <td><INPUT TYPE=button class="button is-small is-success is-rounded"
           onClick="parent.location='[[=URL('new_question/None/quest')]]'"VALUE="New Question">
</td>
    <td><INPUT TYPE=button class="button is-small is-success is-rounded"
           onClick="parent.location='[[=URL('new_question/None/action')]]'"VALUE="New Action">
</td>
</tr>
</tbody>
</table>
</div>