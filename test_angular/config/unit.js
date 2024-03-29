module.exports = function(config) {
	config.set({
	// base path, that will be used to resolve files and exclude
	basePath : '../..',

	frameworks: ["jasmine"],

	// list of files / patterns to load in the browser
	files : [
	'bower_components/jquery/jquery.js',
	'bower_components/angular/angular.js',
	'bower_components/angular-local-storage/angular-local-storage.js',
	'bower_components/angular/angular.js',
	'bower_components/angular-cookies/angular-cookies.js',
	'bower_components/angular-local-storage/angular-local-storage.js',
	'bower_components/angular-mocks/angular-mocks.js',
	'bower_components/angular-route/angular-route.js',
	'bower_components/angular-sanitize/angular-sanitize.js',
	'bower_components/angular-bootstrap/ui-bootstrap-tpls.js',
	'bower_components/html5shiv/dist/html5shiv.js',
	'bower_components/html5shiv/dist/html5shiv-printshiv.js',
	'bower_components/respond/dest/respond.src.js',
	'bower_components/angular-animate/angular-animate.js',
	'bower_components/json3/lib/json3.min.js',
	'bower_components/angulartics/dist/angulartics.min.js',
	'bower_components/angulartics/dist/angulartics-ga.min.js',
	'test_angular/unit/**/*.spec.js',
	'test_angular/unit/**/*.spec.js',
	'bower_components/fastclick/lib/fastclick.js',
	'assets/lib/autocomplete.js',
	'assets/app/js/*.js',
	'bower_components/jquery-ui/ui/jquery.ui.core.js',
	'bower_components/jquery-ui/ui/jquery.ui.widget.js',
	'bower_components/jquery-ui/ui/jquery.ui.mouse.js',
	'bower_components/jquery-ui/ui/jquery.ui.slider.js',
	'bower_components/angular-ui-slider/src/slider.js'
	],

	// use dots reporter, as travis terminal does not support escaping sequences
	// possible values: 'dots' || 'progress'
	reporters : ['progress', 'coverage'],

	preprocessors: {
		// source files, that you wanna generate coverage for
		// do not include tests or libraries
		// (these files will be instrumented by Istanbul)
		'assets/app/js/*.js': ['coverage']
	},
	coverageReporter : {
		type : 'html',
		dir : 'test_angular/coverage/'
	},

	// these are default values, just to show available options

	// web server port
	port : 8089,

	// cli runner port
	runnerPort : 9109,

	urlRoot : '/__test_angular/',

	// enable / disable colors in the output (reporters and logs)
	colors : true,

	// level of logging
	// possible values: LOG_DISABLE || LOG_ERROR || LOG_WARN || LOG_INFO || LOG_DEBUG
	logLevel : config.LOG_INFO,

	// enable / disable watching file and executing tests whenever any file changes
	autoWatch : false,

	// polling interval in ms (ignored on OS that support inotify)
	autoWatchInterval : 0,

	// Start these browsers, currently available:
	// - Chrome
	// - ChromeCanary
	// - Firefox
	// - Opera
	// - Safari
	// - PhantomJS
	browsers : ['Chrome'],

	// Continuous Integration mode
	// if true, it capture browsers, run tests and exit
	singleRun : true



	});
};
