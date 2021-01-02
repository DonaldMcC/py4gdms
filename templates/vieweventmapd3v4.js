[[import simplejson]]
    var inputmode = 'V';
    var newitems = false;
    var prevclass = 'graph-V'

    var onsuccess = function(res) {
    console.log('success');
    };

    var onerror = function(res) {
        alert('ERROR in call');
    };

    $('#radioBtn a').on('click', function(){
    var sel = $(this).data('title');
    var tog = $(this).data('toggle');
    $('#'+tog).prop('value', sel);
    inputmode = sel;
    //console.log(inputmode);

    $('a[data-toggle="'+tog+'"]').not('[data-title="'+sel+'"]').removeClass('active').addClass('notActive');
    $('a[data-toggle="'+tog+'"][data-title="'+sel+'"]').removeClass('notActive').addClass('active');

    if (inputmode == 'A') {
        $('#graph').removeClass(prevclass).addClass('graph-A')
        prevclass = 'graph-A'
    }
    else if (inputmode == 'L') {
        $('#graph').removeClass(prevclass).addClass('graph-L')
        prevclass = 'graph-L'
    }
        else if (inputmode == 'D') {
        $('#graph').removeClass(prevclass).addClass('graph-D')
        prevclass = 'graph-D'
    }
        else if (inputmode == 'V') {
        $('#graph').removeClass(prevclass).addClass('graph-V')
        prevclass = 'graph-V'
    }
    else if (inputmode == 'E') {
        $('#graph').removeClass(prevclass).addClass('graph-E')
        prevclass = 'graph-E'
    }
});

    var d32py =  {
        vieweventmap: true,
        editable: [[=eventowner]],
        eventid: [[=str(eventid)]],
        projid: [[=str(projid)]],
        edges: [],
        qtext: '',
        ajaxquesturl: "[[=URL('network','ajaxquest')]]",
        redraw: [[=redraw]],
        xpos: 0,
        ypos: 0,
        formaction: '',
        globalnode: []
  };
        var nodes = '';
        var nodes = [[=XML(simplejson.dumps(nodes, default=myconverter))]];
        var links = [[=XML(simplejson.dumps(links, default=myconverter))]];
        var edges = [];

        console.log(nodes);

        var itemUrl = '[[=URL('submit', 'new_questload.load')]]';
        var baselowerUrl = '[[=URL('event', 'vieweventmapd3.html')]]';
        //location.href = "http://127.0.0.1:8081/gdms/event/vieweventmapd3.html/"
        var sub

        $('#itemload').hide();

        function initform(posx, posy) {
                $('#question_qtype').focus();
                $('#question_xpos').val(posx);
                $('#question_ypos').val(posy);
                $('#question_xpos__row').hide();
                $('#question_ypos__row').hide();
            };

        function questadd(action, posx, posy, node) {
            $('#itemload').show();

            if ($('#notloggedin').is(':contains(logged)')) {
                out('You must be signed in in to add items')
            }

            d32py.xpos = posx;
            d32py.ypos = posy;
            d32py.formaction = action;
            d32py.globalnode = node;
            var serverid = '';

            if (action == 'New') {
                $.web2py.component(itemUrl + '/', 'itemload');
                setTimeout(function () {
                    initform(posx, posy)
                }, 1000);
            }

            if (action == 'Edit') {

                if (node.serverid == true) {
                serverid = node.serverid
                }
                else  {
                    serverid = node.title
                }

                $.web2py.component(itemUrl + '/' + serverid, 'itemload');
                //let's wait for fire event to do this properly in later version of web2py
                setTimeout(function () {
                    initform(posx, posy)
                }, 1000);

            }
        };


        function amendnode(qtext) {
              updatenode(d32py.globalnode, qtext);
        };


        function requestLink(sourceId,targetId, action)
        {
        Q.ajax("POST", "[[=URL('linkrequest')]]", {
            sourceid: sourceId,
            targetid: targetId,
            action: action
        }).then(onsuccess).catch(onerror);
        };


        function deleteLink(sourceId,targetId, action)
        {
        Q.ajax("POST", "[[=URL('linkrequest')]]", {
            sourceid: sourceId,
            targetid: targetId,
            action: action
        }).then(onsuccess).catch(onerror);
        };

        function deleteNode(nodeid, eventid, action)
        {
        Q.ajax("POST", "[[=URL('nodedelete')]]", {
            nodeid: sourceId,
            eventid: eventid,
            action: action
        }).then(onsuccess).catch(onerror);
        };

        function demoteNode(nodeid, eventid, parentid, action)
        {
        Q.ajax("POST", "[[=URL('nodedemote')]]", {
            nodeid: nodeid,
            eventid: eventid,
            parentid: parentid,
            action: action
        }).then(onsuccess).catch(onerror);

        };

        function promoteNode(nodeid, eventid, action)
        {
        Q.ajax("POST", "[[=URL('nodedemote')]]", {
            nodeid: nodeid,
            eventid: eventid,
            parentid: parentid,
            action: action
        }).then(onsuccess).catch(onerror);

        };

        function moveElement(sourceid, sourceposx, sourceposy)
        {
        Q.ajax("POST", "[[=URL('move')]]", {
            sourceid: sourceid,
            sourceposx: sourceposx,
            sourceposy: sourceposy
        }).then(onsuccess).catch(onerror);

        };
