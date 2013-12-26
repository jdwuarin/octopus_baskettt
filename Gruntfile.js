module.exports = function(grunt) {

	// Load the plugins
	grunt.loadNpmTasks('grunt-contrib-less');
	grunt.loadNpmTasks('grunt-karma');
	grunt.loadNpmTasks('grunt-contrib-concat');
	grunt.loadNpmTasks('grunt-contrib-uglify');
	grunt.loadNpmTasks('grunt-contrib-imagemin');

	// Default task(s).
	grunt.registerTask('style', ['less']);
	grunt.registerTask('js', ['concat','uglify']);
	grunt.registerTask('img', ['imagemin']);
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
					paths:["media/less"], //Directory to check for @imports
					yuicompress: true,
					strictImports: true //Force evaluation of imports.
				},
				files: {
					"static/css/style.css": "media/less/style.less",
				}

			}
		},

		concat: {
			options: {
				separator: ';',
			},
			dist: {
				src: ['media/app/js/*.js'],
				dest: 'static/js/built.js',
			},
		},

		uglify: {
			js: {
				options: {
					flatten: true
				},
				files: {
					'static/js/built.min.js': ['static/js/built.js']
				}
			}
		},

		imagemin: {
			png: {
				options: {
					optimizationLevel: 7
				},
				files: [{
				// Set to true to enable the following options…
				expand: true,
				// cwd is 'current working directory'
				cwd: 'media/img/',
				src: ['*.png'],
				dest: 'static/img/',
				ext: '.png'
			}]
          }
      },

      karma: {
		unit: { options: karmaConfig('test_angular/config/unit.js') },
		watch: { options: karmaConfig('test_angular/config/unit.js', { singleRun:false, autoWatch: true}) }
      }

  });


};