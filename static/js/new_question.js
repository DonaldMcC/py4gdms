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
              if($('#question_qtype option:selected').text()=='issue' || $('#question_qtype option:selected').text()=='action' )
                 {$('#question_factopinion').hide();
                  $("label[for='question_factopinion']").hide();
                  $('#question_answer1').val('Approve');
                  $('#question_answer1').hide();
                  $("label[for='question_answer1']").hide();
                  $('#question_answer2').show();
                  $('#question_answer2').val('Disapprove');
                  $('#question_answer2').hide();
                  $("label[for='question_answer2']").hide();
                  $("label[for='question_answertext']").hide();
                  $('#question_answertext').hide();};
              if($('#question_qtype option:selected').text()=='quest'){
                  $('#question_factopinion').show();
                  $("label[for='question_factopinion']").show();
                  $('#question_factopinion option:selected').text()=='Fact';
                  $('#question_answer1').show();
                  $("label[for='question_answer1']").show();
                  $('#question_answer2').show();
                  $("label[for='question_answer2']").show();
                  $('#question_answertext').hide();
                  $("label[for='question_answertext']").hide();
                 };
                 });

          $('#question_factopinion').change(function(){
              if($('#question_factopinion option:selected').text()=='Fact')
                {$('#question_answer1').hide();
                $("label[for='question_answer1']").hide();
                 $('#question_answer2').hide();
                 $("label[for='question_answer2']").hide();
                 $("label[for='question_answertext']").show();
                 $('#question_answertext').show();
                 $('#question_status option:selected').text()=='Resolved'
                 $('#question_buttons').append('<p></p><input type="BUTTON" id="wolflookup" ' +
         'value="Lookup Answer on Wolfram Alpha" class="btn btn-primary btn-xs btn-group-xs" onclick="wolfram_alpha_lookup()"></p>');
                 $('#question_buttons').append('<p></p><input type="BUTTON" id="wikiplookup" ' +
         'value="Lookup Answer on Wikipedia" class="btn btn-primary btn-xs btn-group-xs" onclick="wikipedia_lookup()"></p>');
};
              if($('#question_factopinion option:selected').text()=='Opinion')
                {$('#question_answer1').show();
                $("label[for='question_answer1']").show();
                 $('#question_answer2').show();
                 $("label[for='question_answer2']").show();
                 $('#question_answertext').hide();
                 $("label[for='question_answertext']").hide();}
                });
});





