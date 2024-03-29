function hide_options() {
     /* hide optional fields - will move this after working*/
    $('#question_notes').parent().parent().hide();
    $('#question_shared_editing').parent().parent().hide();
    $('#question_social_media').parent().parent().hide();
    $('#question_question_media').parent().parent().parent().hide();
    $('#question_question_url').parent().parent().hide();
};

function show_options() {
     /* hide optional fields - will move this after working*/
    $('#question_notes').parent().parent().show();
    $('#question_shared_editing').parent().parent().show();
    $('#question_social_media').parent().parent().show();
    $('#question_question_media').parent().parent().parent().show();
    $('#question_question_url').parent().parent().show();
};

$(document).ready(function(){
   $('#question_answertext').hide();
   $("label[for='question_answertext']").hide();
   $('#question_responsible').parent().parent().hide();
   $('#question_perccomplete').parent().parent().hide();
   $('#question_execstatus').parent().parent().hide();
   $('#question_xpos').parent().parent().hide();
   $('#question_ypos').parent().parent().hide();
   $('#question_correctans').parent().nextAll("p").first().hide();
   $('#question_correctans').hide();
   $('#question_correctanstext').parent().parent().hide();
   $("label[for='question_correctans']").hide();
   //$('#question_aianswer').parent().nextAll("label").first().
    $('#question_aianswer').parent().parent().children().first()
   $('#question_aianswer').parent().prepend('<div class="btn-group"><input type="BUTTON" id="wolflookup" ' +
         'value="Wolfram Alpha" class="btn btn-primary" onclick="wolfram_alpha_lookup()">');
   $('#wolflookup').after('&nbsp&nbsp<input type="BUTTON" id="wikiplookup" ' +
         'value="Wikipedia" class="btn btn-primary btn-success" onclick="wikipedia_lookup()">');
   $('#wikiplookup').after('&nbsp&nbsp<input type="BUTTON" id="openailookup" ' +
         'value="OpenAI" class="btn btn-primary btn-info" onclick="openai_lookup()">');
  // $('#openailookup').after('&nbsp&nbsp<input type="BUTTON" id="bardlookup" ' +
   //s      'value="Bard" class="btn btn-primary btn-warning" onclick="bard_lookup()"></div>');
   $('#openailookup').after('&nbsp&nbsp<input type="BUTTON" id="clearlookup" ' +
         'value="Clear" class="btn btn-primary btn-danger" onclick="clear_lookup()"></div>');


   $('#question_aianswer').parent().parent().children().first().append('<div class="btn-group mt-4"><input type="BUTTON" ' +
                'id="showoptions" value="Show more" class="btn btn-primary" onclick="show_options()">');

   $('#question_aianswer').attr('readonly', true);
   $('#question_chosenai').attr('readonly', true);
   $('#question_chosenai').parent().parent().hide();

    hide_options();

  /*   $('#question_notes__label').append('<p></p><input type="BUTTON" id="wolflookup" ' + 'value="Lookup Answer on Wolfram Alpha" class="btn btn-primary btn-xs btn-group-xs"
         onclick="wolfram_alpha_lookup()"></p>');
    */
              $('#question_correctans').change(function(){
                  console.log('correctans fired')
                 if ($('#question_correctans').val())
                 {
                 $('#question_status option[value="Resolved"]').prop('selected', true);
                 }
                 else {
                     $('#question_status option[value="In Progress"]').prop('selected', true);
                 }

              });

          $('#question_qtype').change(function(){
              if($('#question_qtype option:selected').text()=='action' )
                 {$('#question_factopinion').parent().parent().hide();
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
                 $('#question_status option[value="Resolved"]').prop('selected', true);
}
              else {
                  $('#question_status option[value="In Progress"]').prop('selected', true);
              }


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





