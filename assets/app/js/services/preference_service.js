angular.module('App.services').service('Preference', [ function() {

		var preferenceList = {};
		preferenceList.cuisine= [];

		var isUndefined = function(variable){
			return typeof variable == "undefined";
		};

		return {
			setCuisine: function(cuisineName, presentStatus) {

				var position = preferenceList.cuisine.indexOf(cuisineName);

				if(position === -1 && presentStatus){
					preferenceList.cuisine.push(cuisineName);
				} else if(!presentStatus){
					preferenceList.cuisine.splice(position,1);
				}

			},
			setParameters: function(preferences) {

				preferenceList.cuisine = preferences.cuisine;
				preferenceList.price_sensitivity  = preferences.price_sensitivity;
				preferenceList.people = preferences.people;
				preferenceList.days = preferences.days;

			},
			getAll: function() {
				return preferenceList;
			},
			isNotValid: function(list) {

				// First check to avoid an error with length
				if(isUndefined(list.cuisine) ||
					isUndefined(list.people) ||
					isUndefined(list.price_sensitivity) ||
					isUndefined(list.days)) {
					return true;
				} else if(list.cuisine.length === 0 ||
					list.people.length === 0 ||
					list.price_sensitivity.length === 0 ||
					list.days.length === 0) {
					return true;
				} else if(list.people < 0 ||
					list.price_sensitivity < 0 ||
					list.price_sensitivity > 1 ||
					list.days < 0){
					return true;
				}
				else {
					return false;
				}
			}
		};
	}]);
