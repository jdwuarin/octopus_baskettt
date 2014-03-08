// describe('ProductListController', function(){

// 	var ctrlScope, ctrl, $httpBackend, _Tesco;

// 	// Mock responses for the porting
// 	var successful_porting = [
// 	{"name": "Tesco Smooth Peanut Butter 340G","success": "True"},
// 	{"name": "Tesco Everyday Value Chopped Tomatoes 400G", "success": "True"},
// 	{"name": "Amoy Reduced Salt Soy Sauce 150Ml","success": "True"}
// 	],
// 	failed_porting = [
// 	{"name": "Tesco Smooth Peanut Butter 340G","success": "True"},
// 	{"name": "Tesco Everyday Value Chopped Tomatoes 400G", "success": "False"},
// 	{"name": "Amoy Reduced Salt Soy Sauce 150Ml","success": "False"}
// 	];

// 	//Loading App
// 	beforeEach(function(){
// 		module("App");
// 	});

// 	beforeEach(inject(function($rootScope, $controller, $injector, Tesco) {

// 		ctrlScope = $rootScope.$new();
// 		_Tesco=Tesco;

// 		spyOn(Tesco, 'getUnsuccessful').andCallThrough();

// 		ctrl = $controller("ProductListController",
// 			{ $scope: ctrlScope, Tesco: _Tesco });
// 	}));


// 	describe("Port the basket to a provider",function(){

// 		it("Should find unsuccessfully transfered items", function(){
// 			expect(_Tesco.getUnsuccessful(failed_porting).length).toBe(2);
// 		});

// 		it("Should find successful transfered items", function(){
// 			expect(_Tesco.getUnsuccessful(successful_porting).length).toBe(0);
// 		});

// 	});

// });

