<div>
<h1 class="title is-3">Event Details</h1>
<table id='TabAnswers' class='table'>
<tbody>
<tr>
<th width="10%"></th>
<th width="60%">[[=eventrow.evt_name]]</th>
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
<th>Location</th>
<td>[[=eventrow.locationid.location_name]]</td>
<td></td>
<td></td>
</tr>
<tr>
<th>Status: </th>
<td id="eventstatus">[[=eventrow.status]] and [[=eventrow.evt_shared and 'Shared' or 'Not Shared']]</td>
<td></td>
<td></td>
</tr>
</tbody>
</table>
</div>