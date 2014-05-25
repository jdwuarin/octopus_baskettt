angular.module('App.directives').directive('scrollTo',
	[function(){
		return function(scope, element, attrs){
			element.bind("click", function(event){
				var $selector = $(attrs.scrollTo);
				if($selector.length){
					$("html, body").animate({
						// 65 because it looks about right
						scrollTop : $selector[0].offsetTop - 65
					}, 1000);
				}
			});
		};
	}]);
