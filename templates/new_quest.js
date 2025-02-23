
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

    }


    var ans_success = function(res) {
        //console.log(res.data);
        var jsonobj =  JSON.parse(res.data);
        $('#question_answer3').parent().parent().show();
        $('#question_answer4').parent().parent().show();
        $("#question_answer1").val(jsonobj[0].text);
        $("#question_answer2").val(jsonobj[1].text);

        $("#question_answer3").val(jsonobj[2].text);
        $("#question_answer4").val(jsonobj[3].text);

    };

    function wolfram_alpha_lookup() {
    var qtext = $('#question_questiontext').val();
    /^ Now we call via ajax and put returned value into notes */

    //$("#question_chosenai")
    result= Q.ajax("POST", "[[=URL('wolfram_alpha_lookup')]]", {
            questiontext: qtext
        }).then(qsuccess).catch(qerror);

};

    function wikipedia_lookup() {
    var qtext = $('#question_questiontext').val();
    /* Now we call via ajax and put returned value into notes */

     result= Q.ajax("POST", "[[=URL('wikipedia_lookup')]]", {
            questiontext: qtext
        }).then(qsuccess).catch(qerror);

};

    function gen_answers() {
    var qtext = $('#question_questiontext').val();
    var qtype = $('#question_qtype').val();
    /^ Now we call via ajax and put returned value into notes */
    result= Q.ajax("POST", "[[=URL('gen_answers')]]", {
            questiontext: qtext,
            qtype: qtype,
            scenario: 'gen_answers'
        }).then(ans_success).catch(qerror);
    };

        function openai_lookup() {
    var qtext = $('#question_questiontext').val();
    /^ Now we call via ajax and put returned value into notes */
    result= Q.ajax("POST", "[[=URL('openai_lookup')]]", {
            questiontext: qtext,
            scenario: 'answer'
        }).then(qsuccess).catch(qerror);
};

                function bard_lookup() {
    var qtext = $('#question_questiontext').val();
    /^ Now we call via ajax and put returned value into notes */

    result= Q.ajax("POST", "[[=URL('bard_lookup')]]", {
            questiontext: qtext
        }).then(qsuccess).catch(qerror);
};
