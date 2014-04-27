angular.module('App.services').service('Gesture', [ function() {

	return {
		drag: function(element, callback) {

			Hammer(element, {}).on('drag dragend release', function(ev) {
				callback(ev);
			});

		}
	}

}]);
