    var onsuccess = function(res) {
    Q.flash({'message':'Answer noted', 'class':'info'})
    console.log('success');
    };
    var onerror = function(res) {
    Q.flash({'message':'Error, 'class':'error'})
        alert('ERROR in call');
    };

    function quickanswer(questid, answer) {
        Q.ajax("POST", "[[=URL('quickanswer')]]", {
            questid: questid,
            answer: answer
        }).then(onsuccess).catch(onerror);
    }

$(document).ready(function() {
      Q.flash({'message':'hello there', 'class':'info'});
      });
