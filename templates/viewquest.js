
$(document).on('change', '#urgslide', function () {
    Q.ajax("POST", "[[=URL('urgency')]]", {
            questid: questid,
            urgency: $(this).val()
        }).then(onsuccess).catch(onerror);
});

$(document).on('change', '#impslide', function () {
    Q.ajax("POST", "[[=URL('importance')]]", {
            questid: questid,
            importance: $(this).val()
        }).then(onsuccess).catch(onerror);
});