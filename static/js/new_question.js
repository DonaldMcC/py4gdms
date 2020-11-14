$(document).ready(function(){
   $('#question_answertext').hide();
   $("label[for='question_answertext']").hide();
      $('#question_responsible').hide();
   $("label[for='question_responsible']").hide();
         $('#question_perccomplete').hide();
   $("label[for='question_perccomplete']").hide();
         $('#question_execstatus').hide();
   $("label[for='question_execstatus']").hide();
      $("label[for='question_startdate']").hide();
         $('#question_startdate').hide();
   $("label[for='question_enddate']").hide();
         $('#question_enddate').hide();

  /*   $('#question_notes__label').append('<p></p><input type="BUTTON" id="wolflookup" ' + 'value="Lookup Answer on Wolfram Alpha" class="btn btn-primary btn-xs btn-group-xs"
         onclick="wolfram_alpha_lookup()"></p>');
    */

          $('#question_qtype').change(function(){
              if($('#question_qtype option:selected').text()=='issue')
                {$('#question_answer1').hide()}
              if($('#question_qtype option:selected').text()=='action')
                {$('#question_answer1').hide()}
              if($('#question_qtype option:selected').text()=='quest')
                {$('#question_answer1').show()}
                });

          $('#question_factopinion').change(function(){
              console.log("changed");
              if($('#question_factopinion option:selected').text()=='Fact')
                {$('#question_answer1').hide();
                $("label[for='question_answer1']").hide();
                 $('#question_answer2').hide();
                 $("label[for='question_answer2']").hide();
                 $("label[for='question_answertext']").show();
                 $('#question_answertext').show();};
              if($('#question_factopinion option:selected').text()=='Opinion')
                {$('#question_answer1').show();
                $("label[for='question_answer1']").show();
                 $('#question_answer2').show();
                 $("label[for='question_answer2']").show();
                 $('#question_answertext').hide();
                 $("label[for='question_answertext']").hide();}
                });
});


function wolfram_alpha_lookup() {
    var qtext = $('#question_questiontext').val();
    /^ Now we call via ajax and put returned value into notes */
     $("#question_notes").val("Looking up answer on Wolfram Alpha");


   result2 =  $.ajax({
  url: "{{=URL('submit','wolfram_alpha_lookup')}}" + '/' + encodeURI(qtext),
  context: document.body
}).done(function(result) {
  $("#question_notes").val(result);
});

    /*result = ajax("{{=URL('submit','wolfram_alpha_lookup')}}', [question_questiontext], ':eval')")*/
}


