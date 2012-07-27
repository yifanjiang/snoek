$(document).ready(function() {
	$('.cancel').live("click",function(e){
		e.preventDefault();
		$('#edit-book').modal("hide"); 
		history.pushState({}, "", "http://localhost:8000/library/");
	});

	$('.save').live("click", function(e){
		e.preventDefault();
		var options = {
			target:"#edit-book",
		};
		$("#book-form").ajaxSubmit(options);
	});

	$('.delete').live("click", function(e){
		e.preventDefault();
		$.ajax({
			type:"GET",
			url:e.target,
			success:function(data) {
				$("#edit-book").html(data);
			}
		});
	});

	$('.getinfo').live("click", function(e){
		$("#edit-book").html("<div class=modal> <div class=modal-body><img src=/media/image/spin.gif></div></div>");
	});
});
