angular.module('App.directives').directive('dragAndDrop',
	['Gesture', 'Cart',
	function(Gesture, Cart) {

		return {
			link: function (scope, element, attrs) {
				var posX=0, posY=0,
				lastPosX=0, lastPosY=0,
				animationID;

				var $dropzone = $('#dropzone');

				window.requestAnimationFrame = window.requestAnimationFrame || window.mozRequestAnimationFrame ||
					window.webkitRequestAnimationFrame || window.msRequestAnimationFrame;

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
					console.log('dropzone',ev);
					var target = ev.gesture.target;
					return target.className === "empty-basket" || target.id === "dropzone";
				};

				Gesture.drag(element[0], function(ev){

					switch(ev.type){

						case 'drag':

						posX = ev.gesture.deltaX + lastPosX;
						posY = ev.gesture.deltaY + lastPosY;
						console.log('drag', animationID);
						if(angular.isUndefined(animationID)){
							animationID = requestAnimationFrame(translationAnimation);
						}

						if(isOnDropzone(ev)){
							$dropzone.css("background-color","red");
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
							console.log('dropzon');
							scope.$apply(function(){
								Cart.add(scope.product);
								// translateTo({x:0, y:0});
								element[0].style.display = "none";
								$dropzone.css("background-color","white");

							});
						} else{
							lastPosX=0;
							lastPosY=0;
							translateTo({x:0, y:0});
						}

						cancelAnimationFrame(animationID);

						break;

					}

				});

				var translationAnimation = function() {
					console.log('animation frame');
					translateTo({x: posX, y: posY});
					animationID = requestAnimationFrame(translationAnimation);
				};

			},
		};
	}]);
