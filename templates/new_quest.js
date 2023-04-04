
    var qsuccess = function(res) {
    $('#question_aianswer').attr('readonly', false);
    $("#question_aianswer").val(res.data);
    $('#question_aianswer').attr('readonly', true);
    };
    var qerror = function(res) {
        alert('ERROR in call');
    };


    function wolfram_alpha_lookup() {
    var qtext = $('#question_questiontext').val();
    /^ Now we call via ajax and put returned value into notes */
     $("#question_notes").val('Looking up answer on Wolfram Alpha');

    result= Q.ajax("POST", "[[=URL('wolfram_alpha_lookup')]]", {
            questiontext: qtext
        }).then(qsuccess).catch(qerror);

};

    function wikipedia_lookup() {
    var qtext = $('#question_questiontext').val();
    /^ Now we call via ajax and put returned value into notes */
     $("#question_notes").val('Looking up answer on Wikipedia');

    result= Q.ajax("POST", "[[=URL('wikipedia_lookup')]]", {
            questiontext: qtext
        }).then(qsuccess).catch(qerror);

};

        function openai_lookup() {
    var qtext = $('#question_questiontext').val();
    /^ Now we call via ajax and put returned value into notes */
     $("#question_notes").val('Looking up answer on Open AI');

    result= Q.ajax("POST", "[[=URL('openai_lookup')]]", {
            questiontext: qtext
        }).then(qsuccess).catch(qerror);
};

