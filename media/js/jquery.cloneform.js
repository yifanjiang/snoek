//The jQuery Setup
$(document).ready(function(){
	
	$('#clonetrigger').click(function(){
		var yourclass=".clonable";  //The class you have used in your form
		var clonecount = $(yourclass).length;	//how many clones do we already have?
		var newid = Number(clonecount) + 1;		//Id of the new clone   
		
		$(yourclass+":first").fieldclone({		//Clone the original elelement
			newid_: newid,						//Id of the new clone, (you can pass your own if you want)
			target_: $("#formbuttons"),			//where do we insert the clone? (target element)
			insert_: "before",					//where do we insert the clone? (after/before/append/prepend...)
			limit_: 4							//Maximum Number of Clones
		});
		return false;
	});

});


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
			var fieldclone = $(this).clone();
			var node = $(this)[0].nodeName;
			var classes = $(this).attr("class");

			//==> Increment every input id <==//
			var srcid = 1;
			$(fieldclone).find(':input').each(function(){
				var s = $(this).attr("name"); 			
				$(this).attr("name", s.replace(eval('/_'+srcid+'/ig'),'_'+settings.newid_)); 
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