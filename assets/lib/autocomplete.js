/* --- Made by justgoscha and licensed under MIT license --- */

var app = angular.module('autocomplete', []);

app.directive('autocomplete', ['$rootScope',function($rootScope){
	var index = -1;

	return {
		restrict: 'E',
		scope: {
			suggestions: '=data',
			onType: '=onType',
			clear: '=clear'
		},
		controller: function($scope, $element, $attrs){

			$scope.searchParam = "";

			// with the searchFilter the suggestions get filtered
			$scope.searchFilter;

			// the index of the suggestions that's currently selected
			$scope.selectedIndex = -1;

			// set new index
			$scope.setIndex = function(i){
				$scope.selectedIndex = parseInt(i,10);
			};

			this.setIndex = function(i){
				$scope.setIndex(i);
				$scope.$apply();
			};

			$scope.getIndex = function(i){
				return $scope.selectedIndex;
			};

			// watches if the parameter filter should be changed
			var watching = true;

			// autocompleting drop down on/off
			$scope.completing = false;

			// starts autocompleting on typing in something
			$scope.$watch('searchParam', function(){
				if(watching) {
					$scope.completing = true;
					$scope.searchFilter = $scope.searchParam;
					$scope.selectedIndex = -1;
				}

				// function thats passed to on-type attribute gets executed
				if($scope.onType){
					$scope.onType($scope.searchParam);
				}

			});

			// for hovering over suggestions
			this.preSelect = function(suggestion){

				watching = false;

				// this line determines if it is shown
				// in the input field before it's selected:
				//$scope.searchParam = suggestion;

				$scope.$apply();
				watching = true;
			};


			$scope.preSelect = this.preSelect;

			this.preSelectOff = function(){
				watching = true;
			};

			$scope.preSelectOff = this.preSelectOff;

			// selecting a suggestion with RIGHT ARROW or ENTER
			$scope.select = function(suggestion){
				$scope.searchParam = suggestion;
				$scope.searchFilter = suggestion;
				watching = false;
				setTimeout(function(){watching = true;},1000);
				$scope.completing = false;
			};

		},
		link: function(scope, element, attrs){

			var preSelect = scope.preSelect,
			preSelectOff = scope.preSelectOff,
			select = scope.select,
			setIndex = scope.setIndex,
			getIndex = scope.getIndex;

			scope.search = function(query){
				$rootScope.$emit('searchEnter',query);
				scope.completing = false;
			};

			element.keydown(function (e){
				var key = {left: 37, up: 38, right: 39, down: 40 , enter: 13, esc: 27};
				var keycode = e.keyCode || e.which;

				var l = angular.element(this).find('li').length;

				scope.$eval(scope.clear);

				// implementation of the up and down movement in the list of suggestions
				switch (keycode){
					case key.up: {
						index = getIndex()-1;

						if(index<-1){
							index = l-1;
						} else if (index >= l ){
							index = -1;
							setIndex(index);
							preSelectOff();
							break;
						}
						setIndex(index);

						if(index!==-1){
							preSelect(angular.element(this).find('li')[index].innerText);
						}

						scope.$apply();

						break;
					}

					case key.down:{
						index = getIndex()+1;
						if(index<-1){
							index = l-1;
						} else if (index >= l ){
							index = -1;
							setIndex(index);
							preSelectOff();
							scope.$apply();
							break;
						}
						setIndex(index);

						if(index!==-1){
							preSelect(angular.element(this).find('li')[index].innerText);
						}

						break;
					}

					case key.left: {break;}
					case key.right: {break;}

					case key.enter:{
						index = getIndex();
						// preSelectOff();
						if(index !== -1){
							select(angular.element(this).find('li')[index].innerText);
						}

						setIndex(-1);
						scope.search(scope.searchParam);
						scope.$apply();
						break;
					}
					case key.esc:{
						scope.completing = false;
						scope.searchParam = "";
						scope.$apply();
					}
					default:{ return;}

				}

				if(getIndex()!==-1 || keycode == key.enter) {
					e.preventDefault();
				}
			});
		},
		template: '<div class="autocomplete">'+
		'<div class="input-container">'+
		'<input type="text" ng-model="searchParam" placeholder="Search for products"/>' +
		'</div>' +
		'<button class="btn-black" type="submit" ng-click="search(searchParam)">Search</button>'+
		'<ul ng-show="searchParam && completing">' +
		'<li suggestion ng-repeat="suggestion in suggestions | filter:searchFilter | orderBy:\'toString()\'" '+
		'index="{{$index}}" val="{{suggestion}}" ng-class="{active: '+
		'($index == selectedIndex)}" ng-click="select(suggestion)">'+
		'{{suggestion}}'+
		'</li>'+
		'</ul>'+
		'</div>'
		}
	}]);

app.directive('suggestion', function(){
	return {
		restrict: 'A',
	require: '^autocomplete', // ^look on controller on parents element
	link: function(scope, element, attrs, autoCtrl){
		element.bind('mouseenter', function() {
			autoCtrl.preSelect(attrs['val']);
			autoCtrl.setIndex(attrs['index']);
		});

		element.bind('mouseleave', function() {
			autoCtrl.preSelectOff();
		});
	}
}
});
