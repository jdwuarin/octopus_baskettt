angular.module('App.directives').directive('dragAndDrop',
	['Gesture', 'Cart',
	function(Gesture, Cart) {

		return {
			link: function (scope, element, attrs) {
				var posX=0, posY=0,
				lastPosX=0, lastPosY=0;

				var translateTo = function(position) {
					var transform = "translate3d("+position.x+"px,"+position.y+"px, 0)";
					console.log(transform);
					element[0].style.transform = transform;
					element[0].style.oTransform = transform;
					element[0].style.msTransform = transform;
					element[0].style.mozTransform = transform;
					element[0].style.webkitTransform = transform;
				};

				var isOnDropzone = function(ev) {
					return ev.gesture.target.className === "empty-basket";
				};

				Gesture.drag(element[0], function(ev){

					switch(ev.type){

						case 'drag':

						posX = ev.gesture.deltaX + lastPosX;
						posY = ev.gesture.deltaY + lastPosY;
						translateTo({x: posX, y: posY});

						if(isOnDropzone(ev)){
							ev.gesture.target.style.borderColor = "purple";
							ev.gesture.target.style.color = "purple";
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
								translateTo({x:0, y:0});
							});
						} else{
							lastPosX=0;
							lastPosY=0;
							translateTo({x:0, y:0});
						}
						break;

					}

				});

			},
		};
	}]);
