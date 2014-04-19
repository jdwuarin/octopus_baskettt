angular.module('App.services').factory('User',
	['$cookies', '$http', '$location', '$route',
	function($cookies, $http, $location, $route) {

		function getUrl(req) {
			return 'api/v1/user/' + req + '/?format=json';
		}

		var LoggedIn = (angular.copy(window.activeUser).length !== 0);

		return {
			login: function(email, password, callback,errorcb) { // POST /user/login
				return $http({
					url: getUrl('login'),
					method: "POST",
					headers: {'Content-Type': 'application/json'},
					data: {email:email, password:password}
				}).success(callback).error(errorcb);
			},
			logout: function(callback) { // GET /user/logout
				return $http({
					url: getUrl('logout'),
					method: "GET"
				}).success(callback);
			},
			redirect: function(url){
				// Redirect to the given url (defaults to '/')
				url = url || '/';
				$location.path(url);
			},
			isLoggedIn: function() {
				return LoggedIn;
			},
			setLoggedIn: function(val) {
				LoggedIn = val;
			},
			signup: function(email, password, passwordConfirmation, user_settings_hash, callback, errorcb) {
				return $http({
					url: getUrl('signup'),
					method: "POST",
					headers: {'Content-Type': 'application/json'},
					data: {
						email:email,
						password:password,
						password_confirm: passwordConfirmation,
						user_settings_hash:user_settings_hash
					}
				}).success(callback).error(errorcb);
			},
			registerBeta: function(email, callback) {
				return $http({
					url: getUrl('beta_subscription'),
					method: "POST",
					headers: {'Content-Type': 'application/json'},
					data: {email:email}
				}).success(callback);
			},
			resetPasswordEmail: function(emailAddress, callback) {

				return $http({
					url: '/api/v1/user/password/reset/',
					method: "POST",
					data: $.param({email: emailAddress}),
					headers: {'Content-Type': 'application/x-www-form-urlencoded'}
				}).success(callback);

			},
			resetPasswordConfirm: function(uidb64, token, newPassword1, newPassword2, callback) {
				return $http({
					url: '/api/v1/user/password/reset/' + uidb64 + '/' + token + '/',
					method: 'POST',
					data: $.param({
						new_password1: newPassword1,
						new_password2: newPassword2
					}),
					headers: {'Content-Type': 'application/x-www-form-urlencoded'}
				}).success(callback);
			},
			updateInfos: function(email, recommendation_email_subscription, news_email_subscription, callback) {
				return $http({
					url: getUrl('update_settings'),
					method: 'POST',
					headers: {'Content-Type': 'application/json'},
					data: {
						email:email,
						recommendation_email_subscription: recommendation_email_subscription,
						news_email_subscription: news_email_subscription
					}
				}).success(callback);
			},
			getSettings: function(callback){
				return $http({
					url: getUrl('settings'),
					method: 'GET',
					headers: {'Content-Type': 'application/json'}
				}).success(callback);
			},
			// Check if logged in in Django backend
			// Avoid losing a session when a user reloads the page
			requestLoggedIn: function(callback) {
				return $http({
					url: getUrl('current'),
					method: "GET",
					headers: {'Content-Type': 'application/json'},
				}).success(callback);
			},
			email: function(){
				return angular.copy(window.activeUser);
			},
			subscribeToEmail: function(){
				return true;
			}
		};
	}]);
