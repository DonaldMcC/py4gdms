
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
    $("#ai_response").text(res.data);
    };

        var qreview = function(res) {
    $("#ai_review").text(res.data);
    };


    var qerror = function(res) {
        alert('ERROR in call from viewquest');
    };

        function openai_lookup(scenario) {
            //this will need a parameter in a bit for whether we want issue, question or action
    var qtext = $('#questiontext').text();
    /^ Now we call via ajax and put returned value into notes */

    result= Q.ajax("POST", "[[=URL('openai_lookup')]]", {
            questiontext: qtext,
            scenario: scenario
        }).then(qsuccess).catch(qerror);
};

         [[if not quest['aianswer']:]]
        $(document).ready(function () {
              var qtext = $('#questiontext').text();

            if (got_ai == 'No') {
                result = Q.ajax("POST", "[[=URL('openai_review')]]", {
                    questiontext: "[[=quest['questiontext'] ]]",
                    qtype: "[[=quest['qtype'] ]]",
                    qid: "[[=quest['id']  ]]"
                }).then(qreview).catch(qerror);
            };
});
         [[pass]]
