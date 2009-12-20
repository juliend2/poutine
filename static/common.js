// answers :
var addanswer = {
	init: function(){
		$('li.question>form').hide();
		$('li.question>a.newanswer').toggle(function(){
			// open
			$(this).siblings('form').show();
			return false;
		},function(){
			// close
			$(this).siblings('form').hide();
			return false;
		});
	}
}