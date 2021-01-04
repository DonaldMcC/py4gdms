    var onsuccess = function(res) {
    console.log('success');
    };
    var onerror = function(res) {
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
