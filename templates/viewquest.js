
$(document).on('change', '#urgslide', function () {
    Q.ajax("POST", "[[=URL('urgency')]]", {
            questid: questid,
            urgency: $(this).val()
        }).then(onsuccess).catch(onerror);
});

$(document).on('change', '#impslide', function () {
    Q.ajax("POST", "[[=URL('importance')]]", {
            questid: questid,
            importance: $(this).val()
        }).then(onsuccess).catch(onerror);
});


    var qsuccess = function(res) {
    $("#question_aianswer").val(res.data);
    };

    var qerror = function(res) {
        alert('ERROR in call from viewquest');
    };

        function openai_lookup() {
            //this will need a parameter in a bit for whether we want issue, question or action
    var qtext = $('#question_questiontext').val();
    /^ Now we call via ajax and put returned value into notes */
        
    result= Q.ajax("POST", "[[=URL('openai_lookup')]]", {
            questiontext: qtext
            scenario: 'answer'
        }).then(qsuccess).catch(qerror);
};

