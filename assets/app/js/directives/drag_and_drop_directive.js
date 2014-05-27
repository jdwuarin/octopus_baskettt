angular.module('App.directives').directive('dragAndDrop',
	['Gesture', 'Cart',
	function(Gesture, Cart) {

		return {
			link: function (scope, element, attrs) {
				var posX=0, posY=0,
				lastPosX=0, lastPosY=0,
				animationID;

				var $dropzone = $('#dropzone');
				var $sidebar = $('#sidebar');


				window.requestAnimationFrame = window.requestAnimationFrame || window.mozRequestAnimationFrame ||
					window.webkitRequestAnimationFrame || window.msRequestAnimationFrame;

				var translateTo = function(position) {
					var transform = "translate3d("+position.x+"px,"+position.y+"px, 0)";
					element[0].style.transform = transform;
					element[0].style.oTransform = transform;
					element[0].style.msTransform = transform;
					element[0].style.mozTransform = transform;
					element[0].style.webkitTransform = transform;
				};

				var isOnDropzone = function(ev) {
					var parents = angular.element(ev.gesture.target).parents();

					var onSideBar = parents.filter(function(key, value){
						return value.className ==='sidebar';
					});

					var isInside = parents.filter(function(key, value){
						return value.id === 'dropzone';
					});

					var target = ev.gesture.target;
					return (target.className === "empty-basket" || target.id === "dropzone" || isInside) && lastPosX > 281;
				};

				Gesture.drag(element[0], function(ev){

					switch(ev.type){

						case 'drag':

						posX = ev.gesture.deltaX + lastPosX;
						posY = ev.gesture.deltaY + lastPosY;

						if(angular.isUndefined(animationID)){
							animationID = requestAnimationFrame(translationAnimation);
						}

						$sidebar.addClass('sidebar-active');

						if(isOnDropzone(ev)){
							$dropzone.addClass("ondropzone");
							console.log('addClass');
						}

						break;

						case 'dragend':
						lastPosX = posX;
						lastPosY = posY;

						break;

						case 'release':
						lastPosX = posX;
						lastPosY = posY;

						if(isOnDropzone(ev)){

							scope.$apply(function(){
								Cart.add(scope.product);
								console.log('dropzon', scope.product);
								element[0].style.display = "none";
								$dropzone.removeClass("ondropzone");
							});
						} else{

							translateTo({x:0, y:0});
						}

						$sidebar.removeClass('sidebar-active');
						lastPosX=0;
						lastPosY=0;
						posX=0;
						posY=0;
						cancelAnimationFrame(animationID);
						animationID = undefined;
						break;

					}

				});

				var translationAnimation = function() {
					console.log('animation frame', posX, posY);
					translateTo({x: posX, y: posY});
					animationID = requestAnimationFrame(translationAnimation);
				};

			},
		};
	}]);
