$('#res_actions').DataTable({responsive: true, paging: false, searching:false, info: false});
$('#res_actions').on('change', 'input', function () {
    var row = $(this).closest('tr');
        var perc = row.find("input[type='range']").val();
        var resp = row.find("input[type='text']").val();
        var due = row.find("input[type='date']").val();
                console.log(due);
    Q.ajax("POST", "[[=URL('perccomplete')]]", {
            questid: row.attr('id'),
            perccomplete: perc,
            responsible: resp,
            duedate: due
        }).then(onsuccess).catch(onerror);
});

