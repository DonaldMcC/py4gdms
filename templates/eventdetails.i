<div>
<h1 class="title is-3">Event Details</h1>
<table id='TabAnswers' class='table'>
<tbody>
<tr>
<th width="10%"></th>
<th width="60%">[[=eventrow.event_name]]</th>
<th width="15%" >Start</th>
<th width="15%">End</th>
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
<td></td>
<td></td>
</tr>
</tbody>
</table>
</div>