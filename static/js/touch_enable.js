//enable dropdown menus on touchscreens
$('.hover').on('touchstart touchend', function(e){
    $(this).toggleClass('hover_effect');
});

