var questions = {
	show_str: 'Show answers',
	hide_str: 'Hide answers',
	init : function(){
		var self = this;
		$('#hideanswers').html(self.show_str);
		$('.answers').hide();
		$('a.showanswer').toggle(function(){
			// open
			$(this).html(self.hide_str);
			$(this).next('.answers').show();
			return false;
		},function(){
			// close
			$(this).html(self.show_str);
			$(this).next('.answers').hide();
			return false;
		});
	}
}
 
// answers :
var answers = {
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