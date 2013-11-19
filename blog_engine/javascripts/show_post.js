// This should probably be an Underscore template!
new_comment_form_html = '<p><em>Leave a comment</em></p><form id="new_comment_form">' + '\n' +
'  <p><strong>Name:</strong> <input type="text" id="name" placeholder="your name"></p>' + '\n' +
'  <p><strong>Email:</strong> <input type="text" id="email" placeholder="your email"></p>' + '\n' +
'  <p><strong>Your comment</strong></p>' + '\n' +
'  <textarea rows="8" cols="50" id="comment" placeholder="your comment"></textarea>' + '\n' +
'  <p><input type="submit" id="submit_comment" value="Submit comment!"></p>' + '\n' +
'</form>'

$(document).ready(function() {
    $('#new_comment_link').on("click", function(event) {
	event.preventDefault();
	$('#new_comment_link').remove();
	var form = $('<div class="form_holder"></div>').html(new_comment_form_html);
	$('#comments').append(form.hide().fadeIn(400));
    });
});
