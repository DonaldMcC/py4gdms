
    var onsuccess = function(res) {
    $("#question_notes").val(res.data);
    };
    var onerror = function(res) {
        alert('ERROR in call');
    };


    function wolfram_alpha_lookup() {
    var qtext = $('#question_questiontext').val();
    /^ Now we call via ajax and put returned value into notes */
     $("#question_notes").val('Looking up answer on Wolfram Alpha');

    result= Q.ajax("POST", "[[=URL('wolfram_alpha_lookup')]]", {
            questiontext: qtext
        }).then(onsuccess).catch(onerror);

};

    function wikipedia_lookup() {
    var qtext = $('#question_questiontext').val();
    /^ Now we call via ajax and put returned value into notes */
     $("#question_notes").val('Looking up answer on Wikipedia');

    result= Q.ajax("POST", "[[=URL('wikipedia_lookup')]]", {
            questiontext: qtext
        }).then(onsuccess).catch(onerror);

};

