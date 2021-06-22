$(document).ready(function () {

    $("#profile-pic").on("click", function (e) {
        e.preventDefault();
        $(".context-menu").css({
            "left": e.pageX,
            "top": e.pageY
        })
        $(".context-menu").toggleClass("context-menu-open")
    })
    $("#receivers").select2({
        dir: "rtl",
        minimumResultsForSearch: 20,
    });
    $("#projects").select2({
        dir: "rtl",
    });
    $("#related-letters").select2({
        dir: "rtl",
        minimumResultsForSearch: 20,
    });
    $('[data-toggle="tooltip"]').tooltip();

    $("#show-body").on("click", function () {
        $(".secs").removeClass("showing");
        $("#body-sec").addClass("showing")
    })
    $("#show-references").on("click", function (e) {
        $(".secs").removeClass("showing");
        $("#references-sec").addClass("showing");
    })

})
