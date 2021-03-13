<div>
<h1 class="title is-3">Events For This Project</h1>
[[if events:]]
<table id='Events' class='table'>
<tbody>
<tr>
<th width="15%">Name</th>
<th width="30%">Description</th>
<th width="15%">Start</th>
<th width="15%">End</th>
<th width="15%">Status</th>
<th width="10%">Action</th>
</tr>
[[for row in events:]]
<tr>
<th>[[=A(row.evt_name,_href=URL('view_event/'+str(row.id)))]]</th>
<td>[[=row.description]]</td>
<td class="text-center">[[=row.startdatetime.strftime('%a %d %b %Y %H:%M')]]</td>
<td class="text-center">[[=row.enddatetime.strftime('%a %d %b %Y %H:%M')]]</td>
<td id="eventstatus">[[=row.status]] and [[=row.evt_shared and 'Shared' or 'Not Shared']]</td>
<td> [[if row.next_evt==0:]]<INPUT TYPE=button class="button is-small is-rounded" onclick="nextevent('[[=row.id]]',this)", VALUE="Next Event">[[pass]]</td>
</tr>
[[pass]]
</tbody>
</table>
[[pass]]
</div>

