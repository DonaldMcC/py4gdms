<div>
<h1 class="title is-5">Project Details</h1>
<table id='TabAnswers' class='table'>
<tbody>
<tr>
<th width="10%"></th>
<th width="60%">[[=projectrow.proj_name]]</th>
<th width="15%" >Start</th>
<th width="15%">End</th>
</tr>
<tr>
<th>Description</th>
<td>[[=projectrow.description]]</td>
<td class="text-center">[[=projectrow.startdate]]</td>
<td class="text-center">[[=projectrow.enddate]]</td>
</tr>
<tr>
<th>Owner</th>
<td>[[=projectrow.proj_owner.first_name+' '+projectrow.proj_owner.last_name]]</td>
<td>Website</td>
<td>[[=A(projectrow.proj_url, _href=projectrow.proj_url)]]</td>
</tr>
<tr>
<th>Status: </th>
<td id="projectstatus">[[=projectrow.proj_status]] and [[=projectrow.proj_shared and 'Shared' or 'Not Shared']]</td>
<td></td>
<td></td>
</tr>
</tbody>
</table>
</div>