module.exports = function(grunt) {

	// Load the plugins
	grunt.loadNpmTasks('grunt-contrib-less');
	grunt.loadNpmTasks('grunt-karma');

	// Default task(s).
	grunt.registerTask('default', ['less']);
	grunt.registerTask('test-watch', ['karma:watch']);

	var karmaConfig = function(configFile, customOptions) {
		var options = { configFile: configFile, keepalive: true };
		var travisOptions = process.env.TRAVIS && { browsers: ['Firefox'], reporters: 'dots' };
		return grunt.util._.extend(options, customOptions, travisOptions);
	};

  	// Project configuration.
	grunt.initConfig({
		pkg: grunt.file.readJSON('package.json'), //To read the values of the package.json file
		
		less: {
			compile: {
				options: {
					paths:["octopusProducts/static/less"], //Directory to check for @imports
					yuicompress: true,
					strictImports: true //Force evaluation of imports.
				},
				files: {
					"octopusProducts/static/css/style.css": "octopusProducts/static/less/style.less",
				},

			},
			
			bootstrap: {
				options: {
					paths:["octopusProducts/static/bootstrap/less"],
					yuicompress: true,
					strictImports: true //Force evaluation of imports.
				},
				files: {
					"octopusProducts/static/bootstrap/css/bootstrap.css": "octopusProducts/static/bootstrap/less/bootstrap.less"
				},
			}
		},
		karma: {
			unit: { options: karmaConfig('test_angular/config/unit.js') },
			watch: { options: karmaConfig('test_angular/config/unit.js', { singleRun:false, autoWatch: true}) }
		}
	});


};