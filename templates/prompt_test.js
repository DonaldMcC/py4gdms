    var qsuccess = function(res) {
    console.log('success');
            console.log(res.data);
    $("#airesults").text('');
        $("#airesults").text(res.data);
        //autoResizeTextarea(document.querySelectorAll("#airesults"), {maxHeight: 320});

        };

    var qerror = function (res) {
        alert('ERROR in call querror function');
    };

    $(document).ready(function() {
        $('.btn-primary').parent().parent().hide();
    });

    function openai_lookup() {
    var qtext = $('#no_table_test_text').val();
    var scenario = $('#no_table_scenario').val();
    console.log(qtext)
      $("#airesults").text('Looking up');

    result= Q.ajax("POST", "[[=URL('openai_lookup')]]", {
            questiontext: qtext,
            scenario: 'answer'
        }).then(qsuccess).catch(qerror);
};
