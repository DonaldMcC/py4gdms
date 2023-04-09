<div>
<h1 class="title h5">Project Details</h1>
<table id='ProjDetails' class='table table-bordered border-danger'>
<tbody class='table-danger'>
<tr>
<th>Project Name</th>
<th>[[=projectrow.proj_name]]</th>
<th>Start</th>
<th>End</th>
</tr>
<tr>
<th>Description</th>
<td>[[=XML(markmin2html(projectrow.description))]]</td>
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