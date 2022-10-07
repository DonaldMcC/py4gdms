
[[if filetype != None:]]
<div class="border box">
[[sourcefile =URL(urlpath, scheme=True, use_appname=True)]]
[[if filetype == 'video/mp4':]]
<video width="320" height="240" controls>
    <source src=[[=sourcefile]] type=filetype=[[=filetype]]>
    Your browser does not support the video tag.
</video>
[[pass]]

[[if filetype == 'audio/mpeg':]]
<audio controls>
    <source src=[[=sourcefile]] type=filetype=[[=filetype]]>
    Your browser does not support the audio tag.
</audio>
[[pass]]

[[if filetype == 'image':]]
<img src=[[=sourcefile]] alt="Image not supported" width="320" height="240">
[[pass]]
</div>
[[else:]]
<div></div>
[[pass]]