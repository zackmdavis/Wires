new_comment_form_html = '<p><em>Leave a comment</em></p><form id="new_comment_form">' + '\n' +
'  <p><strong>Name:</strong> <input type="text" id="comment_author" placeholder="your name"></p>' + '\n' +
'  <p><strong>Email:</strong> <input type="text" id="comment_email" placeholder="your email"></p>' + '\n' +
'  <p><strong>Your comment</strong></p>' + '\n' +
'  <textarea rows="8" cols="50" id="comment_body" placeholder="your comment"></textarea>' + '\n' +
'  <p><input type="submit" id="submit_comment" value="Submit comment!"></p>' + '\n' +
'</form>'

$(document).ready(function() {
    $('#new_comment_link').on("click", function(event) {
	event.preventDefault();
	$('#new_comment_link').remove();
	var form = $('<div id="comment_form_holder"></div>').html(new_comment_form_html);
	$('#comments').append(form.hide().fadeIn(400));
	$('#submit_comment').on("click", function(event) {
	    event.preventDefault();
	    $('#submit_comment').prop("value", "Submitting ...")
	    $('#new_comment_form :input').prop("disabled", true)
	    $.ajax({
		url: "/comments",
		type: "POST",
		data: {
		    author: $('#comment_author').val(),
		    email: $('#comment_email').val(),
		    body: $('#comment_body').val(),
		    post_id: $('#post_title').data("id")
		},
		success: function(response) {
		    console.log(response)
		    $('#no_comments').remove();
		    $('#comment_form_holder').remove();
		    $('#comments').append($(response.html).hide().fadeIn(400));
		}
	    });
	});
    });
});
