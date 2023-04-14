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
<a class="btn btn-sm btn-outline-info" id="eventarchive" data-title="C" data-bs-toggle="modal" data-bs-target="#ArchiveModal">Archive</a>
</div>

<div class="modal fade" id="ArchiveModal" tabindex="-1">
  <div class="modal-dialog"></div>
  <div class="modal-content">
      <div class="modal-header">
          <h5 class="modal-title">Archive Event</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
       <div class="modal-body">This set the archiving event to archived which permanently locks the outcome - make sure everything is
            set before doing this as it cannot be undone. Archived status returns resolved questions and disagreed issues
             to the unspecified event but agreed issues, unresolved questions and actions which are not completed will
              roll-forward to the next event
               [[if not eventrow.next_event:]] WARNING: this event does not currently have a next event set.[[else:]]
        which has been created for this project.[[pass]]
            </div>
       <div class="modal-footer">
           <button type="button" id="modal_archive" class="btn btn-small btn-warning" data-bs-dismiss="modal"
                  onclick="archive('[[=eventrow.id]]')">Save changes</button>
                   <button type="button" class="btn btn-small btn-info" data-bs-dismiss="modal">Close</button>

       </div>
           </div>
  </div>
</div>
</div>


<div>
<input type="hidden" name="fun" id="fun">
</div>
<div id="target"></div>
<div id="graph" class="graph-V">
</div>
