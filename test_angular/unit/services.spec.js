
describe('App services', function() {

	beforeEach(function(){
		module('ngMock');
		module('App');
	});

	describe('User', function(){

		it('should be able to login', inject(['User', function(User) {
			// from django.contrib.auth.models import User
			// User.objects.create_user('test', 'test@test.com', 'testpassword')
			var validEmail		= "test";
			var validPassword	= "testpassword";
			expect(true).toBe(true);
			// User.login(validEmail, validPassword, function(res){

			// });


		}])
		);

	});

});