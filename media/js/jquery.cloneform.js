//The Plugin Script
(function($) {

    $.fn.fieldclone = function(options) { 
    
		//==> Options <==//
		var settings = {
			newid_ : 0,
			target_: $(this),
			insert_: "before",
			limit_: 0
		};
        if (options) $.extend(settings, options);           

		if( (settings.newid_ <= (settings.limit_+1)) || (settings.limit_==0) ){	//Check the limit to see if we can clone

			//==> Clone <==//
			//var fieldclone = $(this).clone();
            var fieldclone = form_template;
			var node = $(this)[0].nodeName;
			var classes = $(this).attr("class");

			//==> Increment every input id <==//
			var srcid = 1;
			$(fieldclone).find(':input').each(function(){
				var s = $(this).attr("name"); 			
				$(this).attr("name", s.replace(eval('/vote'+srcid+'/i'),'vote'+settings.newid_)); 
				var s = $(this).attr("id"); 			
				$(this).attr("id", s.replace(eval('/vote'+srcid+'/i'),'vote'+settings.newid_)); 
			});

			//==> Locate Target Id <==//
			var targetid = $(settings.target_).attr("id");
			if(targetid.length<=0){
				targetid = "clonetarget";
				$(settings.target_).attr("id",targetid);
			}		

			//==> Insert Clone <==//
			var newhtml = $(fieldclone).html().replace(/\n/gi,"");
			newhtml = '<'+node+' class="'+classes+'">'+newhtml+'</'+node+'>';
			
			eval("var insertCall = $('#"+targetid+"')."+settings.insert_+"(newhtml)"); 
		}
    };

})(jQuery);
