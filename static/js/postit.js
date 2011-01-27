$(document).ready(function() {
    var postit_id = 0;

    var markup = '<fieldset class="postit" style="display:none;">';
    markup += '<label class="pblock">Title: <input name="title${id}" class="title" type="text" value="" /></label>';
    markup += '<label class="pblock">Description: <textarea name="description${id}" row="9" col="40"></textarea></label>';
    markup += '<label>Assignee:<input name="assignee${id}" class="assignee" type="text" value="" /></label>';
    markup += '<label>Priority:<input name="priority${id}" class="priority" type="text" value="" /></label>';
    markup += '<label>Points:<input name="points${id}" class="points" type="text" value="" /></label>';
    markup += '<div class="pbuttons"><a class="add_postit" href="#">add</a>';
    markup += '<a class="rem_postit" href="#">rem</a></div>';
    markup += '</fieldset>';
    $.template("postit_template", markup);

    $('.add_postit').live("click", function () {
        postit_id += 1;
        $.tmpl( "postit_template", {id: postit_id}).appendTo("#postit_group");
        $("fieldset:hidden:last").fadeIn(300);
        return false;
    });

    $('.rem_postit').live("click", function () {
        var postit = $(this).parent().parent()
        postit.fadeOut(300, function() {
            $(this).remove();
        });
        return false;
    });
 
    
});

