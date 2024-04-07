// This is now main d3 v4 graph layout it should be used for 5 different functions
    // 1 vieweventmap for eventmap views

    // Basic eventmap now working again - but need the links and nodes to be prettied up a bit
    // this will need mapped out and there will be some issues
    // the tooltip setup also needs confirmed and the force graph parameters need sorted

    // How to get link ids instead of index
    // http://stackoverflow.com/questions/23986466/d3-force-layout-linking-nodes-by-name-instead-of-index
    // embedding web2py in d3
    // http://stackoverflow.com/questions/34326343/embedding-d3-js-graph-in-a-web2py-bootstrap-page

    // tooltips have stopped working - no idea why but think will move to always building and then just showing on
    // mouseover - but not now  https://medium.com/@kj_schmidt/show-data-on-mouse-over-with-d3-js-3bf598ff8fc2

    //console.log(nodes);
    var consts =  {
    selectedClass: "selected",
    connectClass: "connect-node",
    circleGClass: "conceptG",
    nodeRadius: 80
  };

// below will all move into some sort of object maybe combine with above
    var textHeight = 10;
    var lineHeight = textHeight + 5;
    var lines = [];
    initLines();

    var graphvars = {
          selectedNode: null,
          selectedEdge: null,
          mouseDownNode: null,
          mouseDownLink: null,
          touchlinking: false,
          justDragged: false,
          justScaleTransGraph: false,
          lastKeyDown: -1,
          shiftNodeDrag: false,
          selectedText: null,
          lastserverid: ''
      };

    var lastxpos = '';
    var lastypos = '';
    var edges = [];

    // handle redraw graph
    d3.select("#redraw-graph").on("click", function(){redrawGraph();});
    // below should revert to the iterative with additional link values and link types to be added
    links.forEach(function(e) {
        var sourceNode = nodes.filter(function(n) {return n.serverid === e.source;})[0],
            targetNode = nodes.filter(function(n) {return n.serverid === e.target;})[0];
        edges.push({
            source: sourceNode,
            target: targetNode,
            dasharray: e.dasharray,
            value: 1});
    });

    // this was being used for some of the force values - to be considered
    edges.forEach(function(e) {
        if (!e.source["linkcount"]) e.source["linkcount"] = 0;
        if (!e.target["linkcount"]) e.target["linkcount"] = 0;
        e.source["linkcount"]++;
        e.target["linkcount"]++;
    });

        var height = window.innerHeight;
        var width = window.innerWidth - 70;

        nodes.forEach(function(e) {
            //don't think there is a problem here unless debugging
            //e.x = Math.max(consts.nodeRadius, Math.min(width - consts.nodeRadius, rescale(e.xpos, width, 1000)));
            //e.y = Math.max(consts.nodeRadius, Math.min(height - consts.nodeRadius, rescale(e.ypos, width, 1000)));
            e.x = rescale(e.xpos, width, 1000);
            e.y = rescale(e.ypos, height, 1000);
    });

        function rescale(point, newscale, oldscale) {
            if (oldscale != 0 ) {return (point * newscale) / oldscale}
            else {return point}
        }

    // may look at making this dynamic again at some point
    // will now take from v4js for now var width = 960, height = 600;
    function redrawlinks() {
      svg = d3.select("#graph").select('svg');

      //var tdSize=svg.select("#links").selectAll('.link').size();
        var link = svg.select("#links").selectAll('.link')
            .data(edges)
            .attr("class", "link")
            .attr("d", function(d){return "M" + d.source.x + "," + d.source.y + "L" + d.target.x + "," + d.target.y;})
            .classed("link", true)
            .attr("stroke", "purple")
            .style("stroke-width", function(d){return d.linethickness})
            .style("stroke-dasharray", function(d){return d.dasharray})
            .attr("marker-end", "url(#end-arrow)")
            .style('marker-end', 'url(#end-arrow)');

            link.enter()
                .append("path")
                .attr("class", "link")
                .attr("d", function(d){return "M" + d.source.x + "," + d.source.y + "L" + d.target.x + "," + d.target.y;})
                .classed("link", true)
                .attr("stroke", "purple")
                .style("stroke-width", function(d){return d.linethickness})
                .style("stroke-dasharray", function(d){return d.dasharray})
                .attr("marker-end", "url(#end-arrow)")
                .style('marker-end', 'url(#end-arrow)')
                .on("click", function(event, d) {linkclick(event, d);})
                .on("touchstart", function(event, d) {linkclick(event, d);});

            link.exit().remove();
    }

function redrawnodes() {
    //this is main function that draws the graph
    svg = d3.select("#graph").select('svg');
    node = svg.select("#nodes").selectAll(".node")
        .data(nodes);

    node.enter().append("g")
        .attr("class", function (d) {return "node " + d.type;})
        .attr("id", function (d) {return "circle" + d.serverid})
        .attr("transform", function (d) {return "translate(" + d.x + "," + d.y + ")";})
        .on("click", function(event, d) {nodeclick(event, d);})
        .call(d3.drag()
            .on("start", dragnodestarted)
            .on("drag", dragnode)
            .on("end", dragnodeended))
        .append('circle')
        .attr('r', String(consts.nodeRadius))
        .style("fill", function (d) {return d.fillclr})
        .style("stroke", function (d) {return d.scolour})
        .style("stroke-width", function (d) {return d.swidth})
        .style("stroke-dasharray", function (d) {
            if (d.status == 'Draft') {return ("8,8")}
            else {return ("1,1")}
            })
        .each(function (d) {
            var numquests = 0;
            if (d.subquests != null)
            { var numquests = d.subquests.length}
            wrapText(d3.select(this.parentNode), d.title, numquests, d.qtype, d.perccomplete);
            });

        // add the nodes
        node.attr("class", function (event, d) {return "node " + d.type;})
        .attr("id", function (d) {return "circle" + d.serverid})
        .attr("transform", function (d) {return "translate(" + d.x + "," + d.y + ")";})
        ;

    node.select('circle')
        .attr('r', String(consts.nodeRadius))
        .style("fill", function (d) {return d.fillclr})
        .style("stroke", function (d) {return d.scolour})
        .style("stroke-width", function (d) {if (d.selected) {return (11)} else {return d.swidth}});


    node.each(function (d) {
        clearText(d3.select(this), d.title);
        var numquests = 0;
        if (d.subquests != null)
            { var numquests = d.subquests.length};
            wrapText(d3.select(this), d.title, numquests, d.qtype, d.perccomplete);
            node.exit().remove();
            });
    }

    svg = d3.select("#graph").append("svg")
            .attr("width", width)
            .attr("height", height)
            .attr("id", "svgarea");

   svg.append("svg:defs").selectAll("marker-end")
    .data(["end-arrow"])      // Different link/path types can be defined here
   .enter().append("svg:marker")    // This section adds in the arrows
    .attr("id", 'end-arrow')
    .attr("viewBox", "0 -5 10 10")
    .attr("refX", "46")   /* Moves the arrow head out, allow for radius */
    .attr("refY", 0)   /* -1.5  */
    .attr("markerWidth", 3.5)
    .attr("markerHeight", 3.5)
    .attr("orient", "auto")
    .append("svg:path")
    .attr("d", "M0,-5L10,0L0,5");
    svg.append("g").attr("id", "links");
    svg.append("g").attr("id", "nodes");

    var link = svg.select("#links").selectAll('.link')
            .data(edges)
            .classed(consts.selectedClass, function(event, d){return d === state.selectedEdge;})
            .enter()
            .append("path")
            .attr("class", "link")
            .on("click", function(event, d) {linkclick(event, d);})
            .on("touchstart", function(event, d) {linkclick(event, d);})
            .attr("d", function(d){return "M" + d.source.x + "," + d.source.y + "L" + d.target.x + "," + d.target.y;})
        .classed("link", true)
        .attr("stroke", "purple")
        .style("stroke-width", function(event, d){return d.linethickness})
        .style("stroke-dasharray", function(event, d){return d.dasharray})
        .attr("marker-end", "url(#end-arrow)")
        .style('marker-end', 'url(#end-arrow)');

    //below commented out as this now only called on inital load and exit impossible
    //link.exit().remove();
    var node = svg.select("#nodes").selectAll(".node")
            .data(nodes)
            .enter().append("g")
            .attr("class", function(d) { return "node " + d.type;})
            .attr("id", function (d) {return "circle" + d.serverid})
            .attr("transform", function(d){return "translate(" + d.x + "," + d.y + ")";})
            .on("click", function(event, d) {nodeclick(event, d);})
            .on("touchstart", function(event, d) {nodeclick(event, d);})
            .call(d3.drag()
                .on("start", dragnodestarted)
                .on("drag", dragnode)
                .on("end", dragnodeended));

    // add the nodes
    node.append('circle')
        .attr('r', String(consts.nodeRadius))
        .style("fill", function(d){return d.fillclr})
        .style("stroke", function(d){return d.scolour})
        .style("stroke-dasharray", function(d){if (d.status=='Draft') {return ("8,8")} else {return ("1000,1")}}) // make the stroke dashed
        .style("stroke-width", function(d){return d.swidth});

    node.each(function(d) {
        var numquests = 0;
        if (d.subquests != null)
        { var numquests = d.subquests.length};
        wrapText(d3.select(this), d.title,  numquests, d.qtype, d.perccomplete);
        drawtooltip(d);});

        //V E L A D M view, edit, link, add, delete, demote
        //So getting real problems with click events not triggering instead only the
        //drag event was firing - think we overcome this with a justDragged variable
        //and calling fromdrag for now
    function rectclick(event) {
        // lets replace this with launching question url in new tab
        //console.log("you clicked rectd ", d.serverid);
        //think this will become an ajax load presently
        location.href = baselowerUrl+'/1/'+d.serverid+'/';
        event.stopPropagation();};

    function urlclick(event, d) {
        // lets replace this with launching question url in new tab
        //console.log("you clicked rectd ", d.serverid);
        //think this will become an ajax load presently
        //console.log('you clicked url')
        //console.log(d)
        event.stopPropagation();
        if (d.question_url >'') {
            window.open(d.question_url, '_blank').focus();
            event.stopPropagation();
        };};

    function nodeclick(event, d) {
        //alert("you clicked node", d.serverid);
        //console.log(d.serverid);
        switch(inputmode) {
            case 'E':
                //Edit - this should load the URL and possibly view would bring up
                //full thing as view quest
                //console.log("you clicked edit", d.serverid);
                //console.log("calling quetsadd");
                if (d.locked != 'Y') {questadd('Edit', event.x, event.y, d);}
                else {questadd('View', event.x, event.y, d);}
                break;
            case 'L':
                if (graphvars.mousedownnode && graphvars.mousedownnode != d) {
                    //console.log(" link request to make", d.serverid);
                    var newEdge = {source: graphvars.mousedownnode, target: d};
                    edges.unshift(newEdge);
                    var linksource = graphvars.mousedownnode.serverid.toString();
                    var linkdest = d.serverid.toString();
                    if (linksource == '0') {
                        linksource = graphvars.mousedownnode.title;
                    }
                    if (linksource == '0') {linksource = d.serverid.title;}
                    console.log("calling request link")
                    requestLink(linksource, linkdest, 'create');
                    redrawlinks();
                    graphvars.mousedownnode.selected = false;
                    graphvars.mousedownnode = null;
                    }
                else {
                    if (graphvars.mousedownnode) {
                        //clicked on same node as previously
                        console.log("clicking same node")
                    {
                        graphvars.mousedownnode.selected = true
                    }
                }
                else {
                    graphvars.mousedownnode = d;
                    graphvars.mousedownnode.selected = true;
                }
            }
                redrawnodes();
                break;
            case 'M':
                if (graphvars.mousedownnode && graphvars.mousedownnode != d) {
                    //console.log("move node down into", d.serverid);
                    var nodeid = graphvars.mousedownnode.serverid.toString();
                if (nodeid == '0') {
                    nodeid = graphvars.mousedownnode.serverid.title;
                }
                demoteNode(nodeid, d32py.eventid, d.serverid);
                if (d.subquests) {
                    d.subquests.push(nodeid)}
                else {d.subquests = [nodeid] }
                nodes.splice(nodes.indexOf(graphvars.mousedownnode), 1);
                spliceLinksForNode(graphvars.mousedownnode);
                graphvars.mousedownnode = null;
                redrawlinks();
                redrawnodes();
                redrawnodes();
                graphvars.mousedownnode = null;
                }
                else {
                    graphvars.mousedownnode = d;
                    graphvars.mousedownnode.selected = true;
                    redrawnodes();
                }
                break;
            case 'D':
                var nodeid = d.serverid.toString();
                if (nodeid == '0') {
                    nodeid = d.serverid.title;
                }
                d3.select("body").select('div.tooltip').remove();
                deleteNode(nodeid, d32py.eventid);
                nodes.splice(nodes.indexOf(d), 1);
                spliceLinksForNode(event, d);
                graphvars.mousedownnode = null;
                //console.log(nodes);
                redrawlinks();
                redrawnodes();
                redrawnodes();
                break;
            case 'P':
                //console.log(nodes);
                //console.log("you clicked promote", d.serverid);
                var nodeid = d.serverid.toString();
                if (nodeid == '0') {
                    nodeid = d.serverid.title;
                }
                d3.select("body").select('div.tooltip').remove();
                promoteNode(nodeid, d32py.eventid, 'promote');
                nodes.splice(nodes.indexOf(d), 1);
                spliceLinksForNode(event, d);
                graphvars.mousedownnode = null;
                //console.log(nodes);
                redrawlinks();
                redrawnodes();
                redrawnodes();
                break;
            default:
                //console.log("view or add on a node do nothing", d.serverid);
        }
            //event.stopPropagation();
        }


    spliceLinksForNode = function(node) {
        toSplice = edges.filter(function(l) {
      return (l.source === node || l.target === node);
    });
    toSplice.map(function(l) {
      edges.splice(edges.indexOf(l), 1);
    });
  };

    function linkclick(event, d) {
        //console.log("you clicked link", d);
        switch (inputmode) {
            case 'D':
                //Edit - this should load the URL and
                //console.log("this will call delete link");
                deleteLink(edges[edges.indexOf(d)].source.serverid.toString(), edges[edges.indexOf(d)].target.serverid.toString(), 'delete');
                //console.log(edges.length);
                //console.log(d.source,d.target);
                var index = edges.indexOf(d);
                edges.splice(index, 1);
                //console.log(edges.length)
                //console.log(edges);
                redrawlinks();
                graphvars.mousedownnode = null;
                break;
            default:
                //console.log("probably do nothing", d.source);
        }
        event.stopPropagation();
    }


    svg.on("click", backclick);

    function backclick(event, d) {
        //console.log("you clicked background");
        switch(inputmode) {
        case 'A':
            //Edit - this should load the URL and
            //console.log("this will add a new node at", event.x);
            questadd('New', Math.floor(rescale(event.x, 1000, width)), Math.floor(rescale(event.y, 1000, width)));
            break;
            default:
            //console.log("reset the source if linking");
        }
    }


    function drawtooltip(d) {
     var fieldformat = "<TABLE class='table table-bordered table-condensed bg-info'>";
        var qtype = 'Action';
        var notes = '';

        if (d.qtype == 'quest') {
                qtype = 'Question';
            } else if (d.qtype == 'issue') {
                qtype = 'Issue';
        };

        if (d.notes != null) {
            notes = d.notes;
            notes = notes.substring(0, 300);
        };
        if (d.aianswer != null) {
            notes = 'Notes:' + notes + '<br>AI answer:' + d.aianswer;
            notes = notes.substring(0, 300);
        };

        if (notes == '') {
            notes = 'No notes or AI Answer';
        }

        fieldformat += "<TR><TD><B>" + qtype + "</B></TD><TD colspan='3'>" + notes + "</TD></TR>";
        if (qtype == 'Action') {
            fieldformat += "<TR><TD><B>Due Date</B></TD><TD>" + d.duedate + "</TD><TD><B>" + " Responsible:" + "</B></TD><TD>" + d.responsible + "</TD></TR>";
        };

        fieldformat += "<TR><TD><B>Status</B></TD><TD>"+ d.status+"</TD><TD><B>"+" Priority:"+"</B></TD><TD>"+ d.priority+"</TD></TR>";
        if (d.question_url > '') {
                fieldformat += "<TR><TD><B>Link</B></TD><TD colspan='3'>" + d.question_url + "</TD></TR>";
            };

        fieldformat += "</TABLE>";
        // Define 'div' for tooltips
        svgposition = document.getElementById("graph");

        var div = d3.select("#graph").append("div")  // declare the tooltip div
	            .attr("class", "tooltip")              // apply the 'tooltip' class
                .attr("id", "tooltip" + d.serverid)
                .html(fieldformat)
                .style("position", "absolute")
                .style("left",  svgposition.offsetLeft + d.x + 20 + "px")
                .style("top", svgposition.offsetTop + d.y + 30 + "px")
                .style("width", 50 + "px")
                .transition()
                .duration(800)
                .style("opacity", 0);};

//need to actually figure out what goes in the tooltip 
    node.on("mouseover", function(event, d) {
        newid = "#tooltip" + this.id.substring(6)
        var g = d3.select(newid).style("opacity", 1);});

    node.on("mouseout", function(event, d) {
        newid = "#tooltip" + this.id.substring(6)
        var g = d3.select(newid).style("opacity", 0);});


    function(dragnodestarted(event, d) {
        //do nothing
    }


    function dragnode(event, d) {
            switch (inputmode) {
                case 'E':
                    //d.fx = event.x;
                    //d.fy = event.y;
                    d.x = event.x;
                    d.y = event.y;
                    d3.select(this).attr("transform", function (d) {
                    return "translate(" + d.x + "," + d.y + ")";
                    });
                    redrawlines();
                    break;
            default:
                //console.log("do nothing ");
                    }
        }

        function dragnodeended(event, d) {
            //console.log('drag ended');
            //d.fx = null;
            //d.fy = null;
            lastserverid = d.serverid.toString();
            lastxpos = Math.floor(rescale(d.x,1000,width));
            lastypos = Math.floor(rescale(d.y,1000,height));
            moveElement(lastserverid, lastxpos.toString(), lastypos.toString() );
            graphvars.justDragged = false;
            graphvars.justDragged = true;
        }

    if (d32py.redraw == true) {redrawGraph()}

    // ** Update data section (Called from the onclick)
    function redrawlines() {
    svg.selectAll('.link')
        .data(edges)
        .attr("d", function (d) {return "M" + d.source.x + "," + d.source.y + "L" + d.target.x + "," + d.target.y;});
    };


    function redrawGraph() {
        var attractForce = d3.forceManyBody().strength(2000).distanceMax(100000)
                     .distanceMin(1000);
        var repelForce = d3.forceManyBody().strength(-3000).distanceMax(800)
                   .distanceMin(1);
        var simulation = d3.forceSimulation()
            .force("attractForce",attractForce)
            .force("link", d3.forceLink().id(function(event, d) { return d.id; }))
            .force("repelForce",repelForce)
            .force("center", d3.forceCenter(width / 2, height / 2))
            .force("y", d3.forceY(height / 2).strength(0.07))
            .force("x", d3.forceX(width / 2).strength(0.05));

        function strength() { return 0.1; }
        function distance() { return 200; }

        simulation
            .nodes(nodes)
            .on("tick", tick)
            .on('end', function() {
            // layout is done
            writetoserver();
            });

        simulation.force("link")
            .links(edges)
            .distance(distance)
            .strength(strength);

        function tick() {
            node.attr("transform", function (d) {d.x = Math.max(consts.nodeRadius, Math.min(width - consts.nodeRadius, d.x));
            d.y = Math.max(consts.nodeRadius, Math.min(height - consts.nodeRadius, d.y));
            return "translate(" + d.x + "," + d.y + ")";
        });

        redrawlines();
    }
}

    function writetoserver() {
        if (d32py.vieweventmap == true && d32py.editable == true) {
            // if owner and eventmapiterate through nodes and call function to write new positions to server
            nodes.forEach(function (e) {
            //console.log(e.serverid.toString() + ':' + Math.floor(e.x).toString() + ':' + Math.floor(rescale(e.x, 1000, width)).toString());
            moveElement(e.serverid.toString(), Math.floor(rescale(e.x, 1000, width)).toString(),
                Math.floor(rescale(e.y, 1000, height)).toString());})
        }
    }

    function clearText(gEl) {
        var el = gEl.selectAll("text");
        el.remove('tspan');
    }

    // think these may become methods from naming setup
    function wrapText(gEl, title, numsubs, qtype, perccomplete) {
        var i = 0;
        var line = 0;
        var words = title.split(" ");

        var rc = gEl.append("rect")
             .attr("x", 45)
             .attr("y", 45)
             .attr("stroke", "blue")
             .attr("width", 20)
             .attr("height", 20)
             .on("click", function(event, d) {urlclick(event, d)});
        var rct = gEl.append("text")
             .attr("x", 52)
             .attr("y", 59)
             .attr("font-size", "10px")
             .text("L");

    if (qtype=='action') {
        var ac = gEl.append("rect")
            .attr("x", -68)
            .attr("y", 45)
            .attr("width", 20)
            .attr("height", 20)
            .on("click", function() {rectclick()});
        //   .text(function(d) { return d.numsubs});
        var act = gEl.append("text")
            .attr("x", -59)
            .attr("y", 59)
            .attr("text-anchor", "middle")
            .attr("font-size", "10px")
            .text(perccomplete);
    }

     var el = gEl.append("text")
         .attr("text-anchor", "middle")
         .attr("font-size", "11px")
         .attr("dy", "-" + 7.3 * 7.5);

     while (i < lines.length && words.length > 0) {
         line = lines[i++];
         var lineData = calcAllowableWords(line.maxLength, words);
         //console.log(lineData);
         var tspan = el.append('tspan').text(lineData.text);
         if (i > 1)
             tspan.attr('x', 0).attr('dy', '15');
         words.splice(0, lineData.count);
     }

 }

        // calculate how many words will fit on a line

function calcAllowableWords(maxWidth, words) {
    var testLine = "";
    var spacer = "";
    var fittedWidth = 0;
    var fittedText = "";
    //ctx.font = font;

    for (var i = 0; i < words.length; i++) {
        testLine += spacer + words[i];
        spacer = " ";

        //var width = ctx.measureText(testLine).width;
        var width = testLine.length * 5;
        if (width > maxWidth) {
            if (i > 0) {
            return ({count: i, width: fittedWidth, text: fittedText});}
            else {return ({count: 1, width: maxWidth, text: words[0]
            });}
        }

        fittedWidth = width;
        fittedText = testLine;
    }
    return ({count: i, width: fittedWidth, text: fittedText});
}

    function initLines() {
        var radius  = 80;
        for (var y = radius * .9; y > -radius; y -= lineHeight) {
            var h = Math.abs(radius - y);
            if (y - lineHeight < 0) {h += 20;}
            var length = 2 * Math.sqrt(h * (2 * radius - h)) + 5;
            if (length && length > 10) {lines.push({y: y, maxLength: length});}
        }
    }

    function out(m) {$('#target').html(m);}

    function addnode(itemtext, posx, posy, qtype) {
        var nodecolour = "rgb(215,255,215)"
        if (qtype == 'action') {nodecolour = 'rgb(255,255,220)'};
        if (qtype == 'issue') {nodecolour = 'rgb(215,215,255)'};
        nodes.push({
            answers: ['yes', 'no'],
            fillclr: nodecolour,
            id: nodes.length,
            locked: "N",
            priority: 25,
            qtype: qtype,
            perccomplete: 0,
            r: 160,
            selected: false,
            fixed: false,
            scolour: 'orange',
            linkcount: 0,
            fontsize: 10,
            serverid: 0,
            status: "Draft",
            swidth: 2,
            textclr: "white",
            title: itemtext,
            xpos: posx,
            ypos: posy,
            x: rescale(posx, width, 1000),
            y: rescale(posy, height, 1000)});
    };

    function updatenode(node, itemtext) {
        //console.log(node.serverid, itemtext);
        node.title = itemtext;
        redrawnodes();
    };