
    var qsuccess = function(res) {
    $('#question_aianswer').attr('readonly', false);
    $("#question_aianswer").val(res.data);
    $('#question_aianswer').attr('readonly', true);
    //allow selection of answer once knowledge engine used
    $('#question_correctans').show();
    $("label[for='question_correctans']").show();
    $('#question_correctans').parent().nextAll("p").first().show();
    };
    var qerror = function(res) {
        alert('ERROR in call');
    };

    function clear_lookup() {
        $('#question_aianswer').attr('readonly', false);
    $("#question_aianswer").val('');
    $('#question_aianswer').attr('readonly', true);
    }


    function wolfram_alpha_lookup() {
    var qtext = $('#question_questiontext').val();
    /^ Now we call via ajax and put returned value into notes */
     $("#question_notes").val('Looking up answer on Wolfram Alpha');
     $("#question_chosenai option[value=2]").prop('selected', true);

    //$("#question_chosenai")
    result= Q.ajax("POST", "[[=URL('wolfram_alpha_lookup')]]", {
            questiontext: qtext
        }).then(qsuccess).catch(qerror);

};

    function wikipedia_lookup() {
    var qtext = $('#question_questiontext').val();
    /* Now we call via ajax and put returned value into notes */
     $("#question_notes").val('Looking up answer on Wikipedia');
     $("#question_chosenai option[value=4]").prop('selected', true);

     result= Q.ajax("POST", "[[=URL('wikipedia_lookup')]]", {
            questiontext: qtext
        }).then(qsuccess).catch(qerror);

};

        function openai_lookup() {
    var qtext = $('#question_questiontext').val();
    /^ Now we call via ajax and put returned value into notes */
     $("#question_notes").val('Looking up answer on Open AI');
     $("#question_chosenai option[value=3]").prop('selected', true);

    result= Q.ajax("POST", "[[=URL('openai_lookup')]]", {
            questiontext: qtext
        }).then(qsuccess).catch(qerror);
};

