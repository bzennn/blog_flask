/*
$('#headerCarousel').carousel({
    interval: 5000,
    cycle: true
});*/

/* Sticky footer */
if ($(document).height() <= $(window).height()) {
    $("footer.footer").addClass("fixed-bottom");
    $("footer.footer").addClass("footer-bottom-p");
    $("div.copyright").addClass("fixed-bottom");
}
/* Sticky footer end */

/* File size and ext check */
function validate() {
    var file = $(".file_upload")[0].files[0];
    var fileExtension = /(\.jpg|\.jpeg|\.bmp|\.gif|\.png)$/i;
    var fullPath = document.getElementById('inputPicture').value;

    if (!fileExtension.exec(fullPath)){
        $("#inputPicture").addClass("is-invalid");
        $(".file_upload_text").html("Only images (2mb size)");
        return false
    }

    if (file.size>2097152) {
		$("#inputPicture").addClass("is-invalid");
		$(".file_upload_text").html("Only images (2mb size)");
		return false;
	}

	return true;
}
/* File size and ext check end */

/* Highlight.js load */
hljs.initHighlightingOnLoad();
/* Highlight.js load end */