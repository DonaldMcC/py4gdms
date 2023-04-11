<div>
    <br>
<h1 class="title h5">Events For This Project</h1>
[[if events:]]
<table id='Events' class='table table-bordered border-info'>
<thead class='table-info'>
<tr>
<th>Name</th>
<th>Description</th>
<th>Start</th>
<th class="is-hidden-touch">End</th>
<th>Status</th>
<th>Action</th>
</thead>
</tr>
<tbody>
[[for row in events:]]
<tr>
<th>[[=A(row.event_name, _href=URL('view_event/'+str(row.id)))]]</th>
<td>[[=XML(markmin2html(row.description))]]</td>
<td class="text-center">[[=row.startdatetime.strftime('%a %d %b %Y %H:%M')]]</td>
<td class="is-hidden-touch text-center">[[=row.enddatetime.strftime('%a %d %b %Y %H:%M')]]</td>
<td id="eventstatus">[[=row.status]]</td>
<td> [[if row.next_event==0:]]
    <INPUT TYPE=button class="button is-small is-rounded" onclick="nextevent('[[=row.id]]',this)", VALUE="Next Event">
    [[pass]]</td>
</tr>
[[pass]]
</tbody>
</table>
[[pass]]
</div>
