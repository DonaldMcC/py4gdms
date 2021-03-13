    var onsuccess = function(res) {
    Q.flash({'message':'Answer noted:'+res.data, 'class':'info'})
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
        Q.ajax("POST", "[[=URL('create_next_event')]]", {
            eid: eid
        }).then(onsuccess).catch(onerror);
    }

$(document).on('change', '#urgslide', function () {
    console.log('I calld' + $(this).val())
    Q.ajax("POST", "[[=URL('urgency')]]", {
            questid: '[[=quest['id'] ]]',
            urgency: $(this).val()
        }).then(onsuccess).catch(onerror);
});

$(document).on('change', 'impslide', function () {
    Q.ajax("POST", "[[=URL('importance')]]", {
            questid: '[[=quest['id'] ]]',
            importanc: $(this).val()
        }).then(onsuccess).catch(onerror);
});
