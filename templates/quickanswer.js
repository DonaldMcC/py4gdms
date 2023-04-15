    var onsuccess = function(res) {
    Q.flash({'message':res.data, 'class':'info'})
    console.log('success');
    };
    var onerror = function(res) {
    Q.flash({'message':'Error', 'class':'error'})
        alert('ERROR in call');
    };

    function quickanswer(questid, answer, sourcebutton) {
        setTimeout(function(){sourcebutton.disabled=true;},0);
        Q.ajax("POST", "[[=URL('quickanswer')]]", {
            questid: questid,
            answer: answer
        }).then(onsuccess).catch(onerror);
    }

    function nextevent(eid, sourcebutton) {
         $("#nextevent").prepend('Created ');
         $("#next_event").prop('disabled', true);
        Q.ajax("POST", "[[=URL('create_next_event')]]", {
            eid: eid
        }).then(onsuccess).catch(onerror);
    }


