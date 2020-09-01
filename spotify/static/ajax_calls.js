$(document).ready(function () {
    $(".pause").click(function () {
        $.ajax({
            type: 'GET',
            url: 'http://127.0.0.1:8000/spotify/player/pause/',
        });
    });
});
$(document).ready(function () {
    $(".play").click(function () {
        $.ajax({
            type: 'GET',
            url: 'http://127.0.0.1:8000/spotify/player/play/',
        });
    });
});