$(document).ready(function () {

    $("#profile-pic").on("click", function (e) {
        e.preventDefault();
        $(".context-menu").css({
            "left": e.pageX,
            "top": e.pageY
        })
        $(".context-menu").toggleClass("context-menu-open")
    })
})