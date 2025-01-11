
    var qsuccess = function(res) {
    console.log('success');
        $("#airesults").val(res.data);
        //autoResizeTextarea(document.querySelectorAll("#airesults"), {maxHeight: 320});
        };

    var qerror = function (res) {
        alert('ERROR in call querror function');
    };

    function clear_lookup() {
        $('#question_aianswer').attr('readonly', false);
    $("#question_aianswer").val('');
    $('#question_aianswer').attr('readonly', true);
    $('#question_chosenai').attr('readonly', false);
     $("#question_chosenai option[value=1]").prop('selected', true);
     $('#question_chosenai').attr('readonly', true);
    };

    function openai_lookup() {
    var qtext = $('#no_table_test_text').val();
    var scenario = $('#no_table_scenario').val();
    console.log(qtext)

    result= Q.ajax("POST", "[[=URL('openai_lookup')]]", {
            questiontext: qtext,
            scenario: 'answer'
        }).then(qsuccess).catch(qerror);
    console.log('called')
};
