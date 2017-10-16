/*
$('#headerCarousel').carousel({
    interval: 5000,
    cycle: true
});*/

if ($(document).height() <= $(window).height()) {
    $("footer.footer").addClass("fixed-bottom");
    $("footer.footer").addClass("footer-bottom-p");
    $("div.copyright").addClass("fixed-bottom");
}