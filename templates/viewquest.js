$(document).on('change', '#urgslide', function () {
    console.log('I calld' + $(this).val())
    Q.ajax("POST", "[[=URL('urgency')]]", {
            questid: '[[=quest['id'] ]]',
            urgency: $(this).val()
        }).then(onsuccess).catch(onerror);
});

$(document).on('change', '#impslide', function () {
    console.log('I cad' + $(this).val())
    Q.ajax("POST", "[[=URL('importance')]]", {
            questid: '[[=quest['id'] ]]',
            importance: $(this).val()
        }).then(onsuccess).catch(onerror);
});