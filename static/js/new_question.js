$(document).ready(function(){
   $('#question_answertext').hide();
   $("label[for='question_answertext']").hide();
   $('#question_responsible').parent().parent().hide();
   $('#question_perccomplete').parent().parent().hide();
   $('#question_execstatus').parent().parent().hide();
   $('#question_xpos').parent().parent().hide();
   $('#question_ypos').parent().parent().hide();
   $('#question_chosenai').parent().after('&nbsp&nbsp<input type="BUTTON" id="wolflookup" ' +
         'value="Wolfram Alpha" class="btn btn-primary btn-xs btn-group-xs" onclick="wolfram_alpha_lookup()">');
   $('#wolflookup').after('<input type="BUTTON" id="wikiplookup" ' +
         'value="Wikipedia" class="btn btn-primary btn-xs btn-group-xs" onclick="wikipedia_lookup()">');
   $('#wikiplookup').after('&nbsp&nbsp<input type="BUTTON" id="openailookup" ' +
         'value="OpenAI" class="btn btn-primary btn-xs btn-group-xs" onclick="openai_lookup()">');
   $('#openailookup').after('&nbsp&nbsp<input type="BUTTON" id="undolookup" ' +
         'value="Undo" class="btn btn-primary btn-xs btn-group-xs" onclick="undo_lookup()">');
   $('#undolookup').after('&nbsp&nbsp<input type="BUTTON" id="clearlookup" ' +
         'value="Clear" class="btn btn-primary btn-xs btn-group-xs" onclick="clear_lookup()">');

   $('#question_aianswer').attr('readonly', true);

  /*   $('#question_notes__label').append('<p></p><input type="BUTTON" id="wolflookup" ' + 'value="Lookup Answer on Wolfram Alpha" class="btn btn-primary btn-xs btn-group-xs"
         onclick="wolfram_alpha_lookup()"></p>');
    */
          $('#question_qtype').change(function(){
              if($('#question_qtype option:selected').text()=='action' )
                 {//$('#question_factopinion').parent().parent().hide();
                  $('#question_answer1').val('Approve');
                  $('#question_answer2').val('Disapprove');
                  $('#question_answer1').parent().parent().hide();
                  $('#question_answer2').parent().parent().hide();
                  $('#question_answertext').parent().parent().hide();};
               if($('#question_qtype option:selected').text()=='issue' )
                 {$('#question_answer1').val('Approve');
                  $('#question_answer2').val('Disapprove');
                  $('#question_answer1').parent().parent().hide();
                  $('#question_answer2').parent().parent().hide();
                  $('#question_answertext').parent().parent().show();};
              if($('#question_qtype option:selected').text()=='quest'){
                  $('#question_factopinion').parent().parent().show();
                  $('#question_factopinion option:selected').text()=='Opinion';
                  $('#question_answer1').val('');
                  $('#question_answer2').val('');
                  $('#question_answer1').parent().parent().show();
                  $('#question_answer2').parent().parent().show();
                  $('#question_answertext').parent().parent().show();};
                 });

          $('#question_factopinion').change(function(){
              if($('#question_factopinion option:selected').text()=='Fact')
                {$('#question_answer1').val('Yes');
                 $('#question_answer2').val('No');
                $('#question_answer1').hide();
                $("label[for='question_answer1']").hide();
                 $('#question_answer2').hide();
                 $("label[for='question_answer2']").hide();
                 $("label[for='question_answertext']").show();
                 $('#question_answertext').show();
                 $('#question_status option:selected').text()=='Resolved'
};
              if($('#question_factopinion option:selected').text()=='Opinion')
                {$('#question_answer1').show();
                $("label[for='question_answer1']").show();
                 $('#question_answer2').show();
                 $("label[for='question_answer2']").show();
                 $('#question_answertext').hide();
                 $("label[for='question_answertext']").hide();}


          if($('#question_factopinion option:selected').text()=='AI_Opinion')
                {$('#question_answer1').show();
                $("label[for='question_answer1']").show();
                 $('#question_answer2').show();
                 $("label[for='question_answer2']").show();
                 $('#question_answertext').hide();
                 $("label[for='question_answertext']").hide();
                 }
                });

                $('#question_qtype').change();
                $('#question_factopinion').change();
});





