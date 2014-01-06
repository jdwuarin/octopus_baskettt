'use strict';
angular.module('App', [
  'ngCookies',
  'ngRoute',
  'ngAnimate',
  'App.filters',
  'App.services',
  'App.directives',
  'App.controllers'
]).config([
  '$httpProvider',
  function ($httpProvider) {
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.useXDomain = true;
    delete $httpProvider.defaults.headers.common['X-Requested-With'];
  }
]).config([
  '$routeProvider',
  function ($routeProvider) {
    $routeProvider.when('/', {
      templateUrl: 'static/app/partials/home.html',
      requireLogin: false
    }).when('/signup', {
      controller: 'RegistrationController',
      templateUrl: 'static/app/partials/signup.html',
      requireLogin: false
    }).when('/login', {
      controller: 'LoginController',
      templateUrl: 'static/app/partials/login.html',
      requireLogin: false
    }).when('/basket', {
      controller: 'ProductListController',
      templateUrl: 'static/app/partials/product_list.html',
      requireLogin: false
    }).when('/onboarding/:id', {
      controller: 'OnboardingController',
      templateUrl: 'static/app/partials/onboarding.html',
      requireLogin: false
    }).when('/transfer', {
      controller: 'TransferController',
      templateUrl: 'static/app/partials/transfer.html',
      requireLogin: true
    }).otherwise({ redirectTo: '' });
  }
]).run([
  '$cookies',
  '$http',
  '$rootScope',
  'User',
  function ($cookies, $http, $rootScope, User) {
    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
    $http.defaults.headers.common['X-CSRFToken'] = $cookies.csrftoken;
    $rootScope.$on('$routeChangeStart', function (event, currRoute, prevRoute) {
      if (!User.isLoggedIn()) {
        User.requestLoggedIn(function (res) {
          if (res.success) {
            User.setLoggedIn(true);
          } else {
            User.setLoggedIn(false);
            if (currRoute.requireLogin) {
              User.redirect('/login');
            }
          }
        });
      }
      if (currRoute.controller === 'OnboardingController') {
        var onboarding_id = parseInt(currRoute.params.id, 10);
        if (onboarding_id === 0 || onboarding_id > 2) {
          User.redirect('/');
        }
      }
    });
  }
]);
'use strict';
angular.module('App.controllers', [
  'ngSanitize',
  'ui.bootstrap'
]).controller('OnboardingController', [
  '$scope',
  '$routeParams',
  'Preference',
  function ($scope, $routeParams, Preference) {
    $scope.cuisines = [
      {
        'name': 'Italian',
        'image': 'italian.png'
      },
      {
        'name': 'Chinese',
        'image': 'chinese.png'
      },
      {
        'name': 'Indian',
        'image': 'indian.png'
      },
      {
        'name': 'Spanish',
        'image': 'spanish.png'
      },
      {
        'name': 'Thai',
        'image': 'thai.png'
      },
      {
        'name': 'French',
        'image': 'french.png'
      }
    ];
    $scope.preference = {};
    var page_id = parseInt($routeParams.id, 10);
    $scope.page = page_id;
    $scope.preference = Preference.getAll();
    $scope.saveData = function () {
      Preference.setParameters($scope.preference);
    };
    $scope.isActive = function (id) {
      return id === page_id;
    };
    $scope.getNextPage = function () {
      if (page_id < 2 && page_id > 0) {
        return '#/onboarding/' + (page_id + 1).toString();
      } else if (page_id === 2) {
        return '#/basket';
      } else {
        return '#/';
      }
    };
  }
]).controller('ProductListController', [
  '$rootScope',
  '$scope',
  'Preference',
  'Basket',
  'Product',
  'User',
  'Tesco',
  'Alert',
  function ($rootScope, $scope, Preference, Basket, Product, User, Tesco, Alert) {
    var preferenceList = Preference.getAll();
    $scope.user = {};
    $scope.tescoCredential = {};
    $scope.search_result = {};
    $rootScope.$on('CloseSignUpForm', function () {
      $scope.closeForm();
      $scope.toggleTescoForm(true);
    });
    $rootScope.$on('removeProduct', function (event, $productIndex) {
      $scope.products.splice($productIndex, 1);
      $scope.$apply();
    });
    Basket.post(preferenceList, function (res) {
      console.log(res);
      $scope.products = res;
    });
    $scope.searchProducts = function () {
      if ($scope.queryTerm) {
        Product.search($scope.queryTerm, function (res) {
          $scope.search_result = res;
        }, function (res) {
          Alert.add('Could find this product', 'danger');
          $scope.search_result = {};
        });
      } else {
        $scope.search_result = {};
      }
    };
    $scope.transferBasket = function () {
      if (!User.isLoggedIn()) {
        $scope.toggleForm(true);
      } else {
        $scope.toggleTescoForm(true);
      }
    };
    $scope.closeForm = function () {
      $scope.toggleForm(false);
    };
    $scope.signup = function () {
      var user = $scope.user;
      if ($scope.signupForm.$valid) {
        User.signup(user.email, user.password, function (data) {
          $rootScope.$emit('UserSignedUp');
        });
      }
    };
    $scope.sendToTesco = function () {
      var tescoCredential = $scope.tescoCredential;
      var list = $scope.products;
      if ($scope.tescoForm.$valid) {
        $scope.toggleTescoForm(false);
        $scope.viewLoading = true;
        Tesco.post(tescoCredential.email, tescoCredential.password, list, function (res) {
          $scope.viewLoading = false;
          Alert.add('Your products have been transfered to Tesco', 'success');
        });
      }
    };
    $scope.closeTescoForm = function () {
      $scope.toggleTescoForm(false);
    };
    $scope.addProduct = function (new_product) {
      var $products = $scope.products, isPresent = false;
      for (var i = $products.length - 1; i >= 0; i--) {
        if ($products[i].name === new_product.name) {
          isPresent = true;
          $products[i].quantity += 1;
          break;
        }
      }
      if (!isPresent) {
        new_product.quantity = 1;
        $scope.products.push(new_product);
      } else {
        $scope.products = $products;
      }
    };
  }
]).controller('RegistrationController', [
  '$scope',
  'User',
  function ($scope, User) {
    $scope.user = {};
    $scope.signup = function () {
      var user = $scope.user;
      if ($scope.signupForm.$valid) {
        User.signup(user.email, user.password, function (data) {
          User.redirect('/');
        });
      }
    };
  }
]).controller('LoginController', [
  '$sanitize',
  '$scope',
  'User',
  'Alert',
  function ($sanitize, $scope, User, Alert) {
    $scope.user = {};
    var sanitizeCredentials = function (credentials) {
      return {
        email: $sanitize(credentials.email),
        password: $sanitize(credentials.password)
      };
    };
    $scope.login = function () {
      var user = $scope.user;
      if ($scope.loginForm.$valid) {
        user = sanitizeCredentials(user);
        User.login(user.email, user.password, function (data) {
          User.setLoggedIn(true);
          Alert.add('Successfully logged in.', 'success');
          User.redirect('/');
        });
      }
    };
  }
]).controller('AlertController', [
  '$scope',
  'Alert',
  function ($scope, Alert) {
    $scope.alerts = Alert.getAll();
    $scope.closeAlert = function (index) {
      Alert.close(index);
      $scope.alerts = Alert.getAll();
    };
  }
]);
'use strict';
angular.module('App.services', ['LocalStorageModule']).factory('Product', [
  '$http',
  function ($http) {
    function getUrl(id) {
      id = typeof id !== 'undefined' ? id : '';
      return 'http://127.0.0.1:8000/api/v1/product/' + id + '?format=json';
    }
    return {
      get: function (id, callback) {
        return $http.get(getUrl(id)).success(callback);
      },
      query: function (callback) {
        return $http.get(getUrl()).success(callback);
      },
      save: function (product, callback) {
        return $http.post(getUrl(), product).success(callback);
      },
      remove: function (id, callback) {
        return $http.delete(getUrl(id)).success(callback);
      },
      put: function (product, callback) {
        return $http.put(getUrl(product.id), product).success(callback);
      },
      search: function (term, callback, errorcb) {
        return $http.get(getUrl('search/') + '&term=' + term).success(callback).error(errorcb);
      }
    };
  }
]).factory('User', [
  '$cookies',
  '$http',
  '$location',
  function ($cookies, $http, $location) {
    function getUrl(req) {
      return 'http://127.0.0.1:8000/api/v1/user/' + req + '/?format=json';
    }
    var LoggedIn = null;
    return {
      login: function (email, password, callback) {
        return $http({
          url: getUrl('login'),
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          data: {
            email: email,
            password: password
          }
        }).success(callback);
      },
      logout: function (callback) {
        return $http({
          url: getUrl('logout'),
          method: 'GET'
        }).success(callback);
      },
      redirect: function (url) {
        url = url || '/';
        $location.path(url);
      },
      isLoggedIn: function () {
        return LoggedIn;
      },
      setLoggedIn: function (val) {
        LoggedIn = val;
      },
      signup: function (email, password, callback) {
        return $http({
          url: getUrl('signup'),
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          data: {
            email: email,
            password: password
          }
        }).success(callback);
      },
      requestLoggedIn: function (callback) {
        return $http({
          url: 'http://127.0.0.1:8000/api/v1/user/current/?format=json',
          method: 'GET',
          headers: { 'Content-Type': 'application/json' }
        }).success(callback);
      }
    };
  }
]).service('Preference', [
  'localStorage',
  function (localStorage) {
    var preferenceList = {};
    preferenceList.cuisine = [];
    return {
      getCuisine: function () {
        var local_cuisine = localStorage.get('preferences').cuisine;
        if (local_cuisine) {
          return local_cuisine;
        } else {
          return preferenceList.cuisine;
        }
      },
      setCuisine: function (scope) {
        var isPresent = false;
        for (var i = preferenceList.cuisine.length - 1; i >= 0; i--) {
          if (preferenceList.cuisine[i] == scope.cuisine.name) {
            isPresent = true;
            if (!scope.selectedStatus) {
              preferenceList.cuisine.splice(i, 1);
            }
          }
        }
        if (!isPresent && scope.selectedStatus) {
          preferenceList.cuisine.push(scope.cuisine.name);
        }
      },
      setParameters: function (preferences) {
        preferenceList.people = preferences.people;
        preferenceList.days = preferences.days;
        preferenceList.budget = preferences.budget;
        var pref_str = JSON.stringify(preferenceList);
        localStorage.add('preferences', pref_str);
      },
      getAll: function () {
        return localStorage.get('preferences');
      }
    };
  }
]).factory('localStorage', [
  'localStorageService',
  function (localStorageService) {
    return {
      add: function (key, value) {
        localStorageService.add(key, value);
      },
      get: function (key) {
        return localStorageService.get(key);
      }
    };
  }
]).factory('Basket', [
  '$http',
  function ($http) {
    var productList = {};
    return {
      post: function (preferences, callback) {
        return $http({
          url: 'http://127.0.0.1:8000/api/v1/user/basket/?format=json',
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          data: preferences
        }).success(callback);
      },
      add: function (product) {
        productList.push(product);
      },
      getAll: function () {
        return productList;
      }
    };
  }
]).factory('Tesco', [
  '$http',
  function ($http) {
    return {
      post: function (email, password, list, callback) {
        return $http({
          url: 'http://127.0.0.1:8000/spider/?format=json',
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          data: {
            email: email,
            password: password,
            products: list
          }
        }).success(callback);
      }
    };
  }
]).factory('Alert', [function () {
    var alertList = [];
    return {
      add: function (message, type) {
        alertList.push({
          msg: message,
          type: type
        });
      },
      close: function (index) {
        alertList.splice(index, 1);
      },
      getAll: function () {
        return alertList;
      }
    };
  }]);
'use strict';
angular.module('App.directives', []).directive('click', [
  'Preference',
  function (Preference) {
    return function (scope, element, attrs) {
      var selected_preference = Preference.getCuisine();
      var selected = selected_preference.some(function (el) {
          return scope.cuisine.name === el;
        });
      scope.selectedStatus = selected;
      element.bind('click', function () {
        scope.selectedStatus = !scope.selectedStatus;
        Preference.setCuisine(scope);
        scope.$apply();
      });
    };
  }
]).directive('signup', [function () {
    return {
      link: function (scope, element, attrs) {
        scope.isVisible = false;
        scope.toggleForm = function (value) {
          scope.isVisible = value;
        };
      },
      restrict: 'E',
      templateUrl: 'static/app/partials/_sign_up.html'
    };
  }]).directive('tesco', [function () {
    return {
      link: function (scope, element, attrs) {
        scope.tescoIsVisible = false;
        scope.toggleTescoForm = function (value) {
          scope.tescoIsVisible = value;
        };
      },
      restrict: 'E',
      templateUrl: 'static/app/partials/_tesco.html'
    };
  }]).directive('navbar', [
  '$rootScope',
  'User',
  function ($rootScope, User) {
    return {
      link: function (scope, element, attrs) {
        $rootScope.$on('UserSignedUp', function () {
          User.requestLoggedIn(function (res) {
            if (res.success) {
              User.setLoggedIn(true);
              scope.userIsLoggedIn();
              $rootScope.$emit('CloseSignUpForm');
            }
          });
        });
        scope.userIsLoggedIn = function () {
          return User.isLoggedIn();
        };
        scope.logout = function () {
          User.logout(function (data) {
            User.setLoggedIn(false);
            User.redirect('/');
          });
        };
      },
      restrict: 'E',
      templateUrl: 'static/app/partials/_nav_bar.html'
    };
  }
]).directive('remove', [
  '$rootScope',
  function ($rootScope) {
    return {
      link: function (scope, element, attrs) {
        element.bind('click', function () {
          $rootScope.$emit('removeProduct', scope.$index);
        });
      },
      template: '<button class="btn-gray btn-remove"><i class="glyphicon glyphicon-remove"></i></button>',
      transclude: true
    };
  }
]);
'use strict';
angular.module('App.filters', []).filter('filteredrecipes', [function () {
    return function (recipes, diets) {
      if (recipes === undefined)
        return;
      var result = recipes.slice();
      var recipe;
      angular.forEach(diets, function (value, key) {
        if (value) {
          for (var index = 0; index < result.length; index++) {
            recipe = result[index];
            if (recipe.title.indexOf(key) == -1) {
              result.splice(index--, 1);
            }
          }
        }
      });
      return result;
    };
  }]);