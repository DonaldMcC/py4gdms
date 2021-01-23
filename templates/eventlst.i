<div>
<h1 class="title is-3">Event For This Project</h1>
[[if events:]]
<table id='Events' class='table'>
<tbody>
<tr>
<th width="10%">Name</th>
<th width="60%">Description</th>
<th width="10%">Start</th>
<th width="10%">End</th>
<th width="10%">Status</th>
</tr>
[[for row in events:]]
<tr>
<th>[[=row.evt_name]]</th>
<td>[[=row.description]]</td>
<td class="text-center">[[=row.startdatetime.strftime('%a %d %b %Y %H:%M')]]</td>
<td class="text-center">[[=row.enddatetime.strftime('%a %d %b %Y %H:%M')]]</td>
<td id="eventstatus">[[=row.status]] and [[=row.evt_shared and 'Shared' or 'Not Shared']]</td>
</tr>
[[pass]]
</tbody>
</table>
[[pass]]
</div>