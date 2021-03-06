<p>
<div class="field is-grouped">>
<INPUT TYPE=BUTTON id="help" class="button is-small is-outlined is-rounded is-warning " onClick="" data-toggle =" popover"
        title ="In view mode you can drag items around the screen and shift click to create items, edit text or create directed links.
Use edit, link, add and delete modes button to edit, link and create/delete without using shift key eg on a touchscreen
Delete requires both a click/touch to select and a second click to remove the item but only links are removed from database until decison made on deletion of nodes" data-content="" VALUE="Help">
<INPUT TYPE=BUTTON id="key" class="button is-small is-outlined is-rounded is-warning " onClick="" data-toggle =" popover"
title ="Issues: Blue<br>Questions: Green <br>Actions: Yellow<br>Colour depth: priority<br>Resolved items have thicker border" data-content="" VALUE="Key">
<div id="radioBtn">
<a class="button is-small is-outlined is-primary is-rounded" data-toggle="fun" data-title="V">View</a>
<a class="button is-small is-outlined is-info is-rounded" data-toggle="fun" data-title="E">Edit</a>
<a class="button is-small is-outlined is-info is-rounded" data-toggle="fun" data-title="L">Link</a>
<a class="button is-small is-outlined is-info is-rounded" data-toggle="fun" data-title="A">Add</a>
<a class="button is-small is-outlined is-info is-rounded" data-toggle="fun" data-title="D">Delete</a>
<a id="redraw-graph" class="button is-small is-outlined is-info is-rounded" data-toggle="fun" data-title="D">Redraw</a>
<a class="button is-small is-outlined is-info is-rounded modal-button" data-target="#myModal" aria-haspopup="true">Archive</a>

<div class="modal" id="myModal">
  <div class="modal-background"></div>
  <div class="modal-content">
    <div class="box">This set the archiving event to archived which permanently locks the outcome - make sure everything is
            set before doing this as it cannot be undone. Archived status returns resolved questions and disagreed issues
             to the unspecified event but agreed issues, unresolved questions and actions which are not completed will
              roll-forward to the next event
               [[if not eventrow.next_event:]] WARNING: this event does not currently have a next event set.[[else:]]
        which has been created for this project.[[pass]]
                   <button type="button" class="mode-close button is-small is-info is-rounded">Close</button>
                  <button type="button" class="button is-small is-warning is-rounded"
                  onclick="archive('[[=eventrow.id]]')">
              Save changes</button>.
           </div>
  </div>
</div>

</div>
<input type="hidden" name="fun" id="fun">
</div>
<div id="target"></div>
<div id="graph" class="graph-V">
</div>
