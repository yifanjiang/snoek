$(document).ready(function() {


	$('#app').css('margin', '15px auto 15px auto').css('width', 'auto').css('background', 'transparent');
	$('.bookmark').imagesLoaded(function(){
			$('#app').masonry({
				itemSelector: '.bookmark',
				columnWidth: 50,
				isFitWidth: true
			});
	});

	var getUrlPk = function(url) {
		var pattern = /library\/\d+/;
		var result = pattern.exec(url);
		if(result != null)
			return result[0].split('/')[1];
		else
			return null;
	};

	var getBook = function(e) {
			e.preventDefault();
			$("#edit-book").html("<div class=modal> <div class=modal-body><img src=/media/image/spin.gif></div> </div>");
			$.ajax({
				type: "GET",
				url:e.target,
				//when brower go to other site,when user clicked backbutton, the ajax result would show,
				//this is not allowd.
				cache:false,
				success:function(data) {
					$('#edit-book').html(data);
					$('#edit-book').modal({
						backdrop: false,
						keyboard: false,
						show: true
					});
					//manipulate url
					//tobe fixed 
					//history.pushState({}, "", "http://localhost:8000/library/"+getUrlPk(e.target));
					if (e.target != document.URL)
						history.pushState({}, "", e.target);
				},
				error:function(data) {
					$("#edit-book").html("");
					alert("Can NOT get information, check your network");
				},
			});
			return false;
	};

	$('.view').click(getBook);
	$('.edit').click(getBook);
	
	
	//check url to trigger an event
	//trigger pop state
	$(window).bind('popstate', function() {
		var pk = getUrlPk(document.URL);
		if (pk != null)
			$('#book'+pk).click();
		else
			$('#edit-book').modal('hide');
	});
});
