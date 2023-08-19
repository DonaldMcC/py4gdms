<div>
<table id='questlinks' class="table table-bordered border-info">
<thead>
</thead>
<tbody>
<tr>
<td><INPUT TYPE=button class="btn btn-primary"
           onClick="parent.location='[[=URL(f"new_question/None/issue/{quest['eventid']}/0/0/view_event/")]]'" VALUE="New Issue">
</td>
    <td><INPUT TYPE=button class="btn btn-success"
           onClick="parent.location='[[=URL(f"new_question/None/quest/{quest['eventid']}/0/0/view_event/")]]'" VALUE="New Question">
</td>
    <td><INPUT TYPE=button class="btn btn-warning"
           onClick="parent.location='[[=URL(f"new_question/None/action/{quest['eventid']}/0/0/view_event/")]]'" VALUE="New Action">
</td>
</tr>
</tbody>
</table>
</div>