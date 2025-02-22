
    var qsuccess = function(res) {
        $('#question_aianswer').attr('readonly', false);
        $("#question_aianswer").val(res.data);
        autoResizeTextarea(document.querySelectorAll("#question_aianswer"), {maxHeight: 320});
        $('#question_aianswer').attr('readonly', true);
        $("#question_answertext").val(res.data);
        //allow selection of answer once knowledge engine used
        $('#question_correctans').show();
        $("label[for='question_correctans']").show();
        $('#question_correctans').parent().nextAll("p").first().show();
    };
    var qerror = function (res) {
        alert('ERROR in call from new_quest');
    };

    function clear_lookup() {
        $('#question_aianswer').attr('readonly', false);
    $("#question_aianswer").val('');
    $('#question_aianswer').attr('readonly', true);
    $('#question_chosenai').attr('readonly', false);
     $("#question_chosenai option[value=1]").prop('selected', true);
     $('#question_chosenai').attr('readonly', true);
    }


    function wolfram_alpha_lookup() {
    var qtext = $('#question_questiontext').val();
    /^ Now we call via ajax and put returned value into notes */
    $('#question_chosenai').attr('readonly', false);
     $("#question_chosenai option[value=2]").prop('selected', true);
     $('#question_chosenai').attr('readonly', true);

    //$("#question_chosenai")
    result= Q.ajax("POST", "[[=URL('wolfram_alpha_lookup')]]", {
            questiontext: qtext
        }).then(qsuccess).catch(qerror);

};

    function wikipedia_lookup() {
    var qtext = $('#question_questiontext').val();
    /* Now we call via ajax and put returned value into notes */
         $('#question_chosenai').attr('readonly', false);
     $("#question_chosenai option[value=3]").prop('selected', true);
    $('#question_chosenai').attr('readonly', true);

     result= Q.ajax("POST", "[[=URL('wikipedia_lookup')]]", {
            questiontext: qtext
        }).then(qsuccess).catch(qerror);

};

    function lookup_answers() {
        console.log('I fired')
    };

        function openai_lookup() {
    var qtext = $('#question_questiontext').val();
    /^ Now we call via ajax and put returned value into notes */
        $('#question_chosenai').attr('readonly', false);
     $("#question_chosenai option[value=4]").prop('selected', true);
    $('#question_chosenai').attr('readonly', true);

    result= Q.ajax("POST", "[[=URL('openai_lookup')]]", {
            questiontext: qtext,
            scenario: 'answer'
        }).then(qsuccess).catch(qerror);
};

                function bard_lookup() {
    var qtext = $('#question_questiontext').val();
    /^ Now we call via ajax and put returned value into notes */
        $('#question_chosenai').attr('readonly', false);
     $("#question_chosenai option[value=5]").prop('selected', true);
    $('#question_chosenai').attr('readonly', true);

    result= Q.ajax("POST", "[[=URL('bard_lookup')]]", {
            questiontext: qtext
        }).then(qsuccess).catch(qerror);
};
