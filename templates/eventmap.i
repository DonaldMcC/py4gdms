<p>
<div class="input-group">>
<INPUT TYPE=BUTTON id="help" class="btn btn-sm btn-warning" onClick="" data-toggle =" popover"
        title ="In view mode you can drag items around the screen and shift click to create items, edit text or create directed links.
Use edit, link, add and delete modes button to edit, link and create/delete without using shift key eg on a touchscreen
Delete requires both a click/touch to select and a second click to remove the item but only links are removed from database until decison made on deletion of nodes" data-content="" VALUE="Help">
<INPUT TYPE=BUTTON id="key" class="btn btn-sm btn-warning " onClick="" data-toggle =" popover"
title ="Issues: Blue, Questions: Green, Actions: Yellow, Colour depth: priority, Resolved items have thicker border" data-content="" VALUE="Key">
<div id="radioBtn" class="btn-group">
<a class="btn btn-sm btn-outline-primary" data-toggle="fun" data-title="V">View</a>
<a class="btn btn-sm btn-outline-info" data-toggle="fun" data-title="E">Edit</a>
<a class="btn btn-sm btn-outline-info" data-toggle="fun" data-title="L">Link</a>
<a class="btn btn-sm btn-outline-info" data-toggle="fun" data-title="A">Add</a>
<a class="btn btn-sm btn-outline-info" data-toggle="fun" data-title="D">Delete</a>
<a id="redraw-graph" class="btn btn-sm btn-outline-info" data-title="R">Redraw</a>
</div>
</div>


<div>
<input type="hidden" name="fun" id="fun">
</div>
<div id="target"></div>
<div id="graph" class="graph-V">
</div>
