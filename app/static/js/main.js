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

	replaceTags();
	return true;
}

/* Highlight.js load */
hljs.initHighlightingOnLoad({
    singleLine: true
});
hljs.initLineNumbersOnLoad();
/* Highlight.js load end */

tinymce.init({
    menubar: false,
    selector: 'textarea#inputPostContent',
    height: 300,
    width: '100%',
    block_formats: 'Header 3=h3;Header 4=h4;Normal=p',
    image_dimentions: false,
    plugins: [
        "codesample",
        "advlist autolink lists link image charmap print preview anchor",
        "searchreplace visualblocks code fullscreen",
        "insertdatetime media table contextmenu paste imagetools"
    ],
    codesample_languages: [
        {text: 'HTML/XML', value: 'markup'},
        {text: 'JavaScript', value: 'javascript'},
        {text: 'CSS', value: 'css'},
        {text: 'PHP', value: 'php'},
        {text: 'Ruby', value: 'ruby'},
        {text: 'Python', value: 'python'},
        {text: 'Java', value: 'java'},
        {text: 'C', value: 'c'},
        {text: 'C#', value: 'csharp'},
        {text: 'C++', value: 'cpp'},
        {text: 'Shell', value: 'sh'}
    ],
    toolbar: "insertfile undo redo | formatselect bold italic | alignleft aligncenter alignright alignjustify | bullist numlist table | link image media | codesample",

    content_css: [
    '//www.tinymce.com/css/codepen.min.css'
    ],

    setup: function(ed){
        ed.on('init', function (ed) {
        ed.target.editorCommands.execCommand("fontName", false, "Roboto");
        });
        
        function toSpan() {
            
        }
    },
});
