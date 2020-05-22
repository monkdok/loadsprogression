$(document).ready(function() {
    $("#edit{{ workout.slug }}").on("click", modal)
    function modal () {
        let title = $("#title{{ workout.slug }}").text();
        alert(title);
    }
});
