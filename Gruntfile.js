module.exports = function(grunt) {

  // Load grunt tasks automatically
  require('load-grunt-tasks')(grunt);

	// Default task(s).
	grunt.registerTask('style', ['less']);
	grunt.registerTask('js', ['concat','uglify']);
	grunt.registerTask('img', ['imagemin']);
	grunt.registerTask('test-watch', ['karma:watch']);

  grunt.registerTask('production',[
    'clean:dist',
    'bower-install',
    'useminPrepare',
    'less',
    'concat',
    'ngmin',
    'copy:dist',
    //'uncss',
    'uglify',

    //'rev',
    'usemin',
   // 'htmlmin'

    ]);


	var karmaConfig = function(configFile, customOptions) {
		var options = { configFile: configFile, keepalive: true };
		var travisOptions = process.env.TRAVIS && { browsers: ['Firefox'], reporters: 'dots' };
		return grunt.util._.extend(options, customOptions, travisOptions);
	};

	// Project configuration.
	grunt.initConfig({
		pkg: grunt.file.readJSON('package.json'), //To read the values of the package.json file

    // Project settings
    app: {
      index: 'octopusProducts/templates/products/index.html',
      indexFolder: 'octopusProducts/templates/products/',
      source: 'media',
      dist: 'static'
    },

		less: {
			compile: {
				options: {
					paths:['<%= app.source %>/less'], //Directory to check for @imports
					yuicompress: true,
					strictImports: true //Force evaluation of imports.
				},
				files: {
					'<%= app.dist %>/styles/style.css': '<%= app.source %>/less/style.less',
				}

			}
		},

		// concat: {
		// 	options: {
		// 		separator: ';',
		// 	},
		// 	dist: {
		// 		src: ['media/app/js/*.js'],
		// 		dest: 'static/js/built.js',
		// 	},
		// },

		// uglify: {
		// 	js: {
		// 		options: {
		// 			flatten: true
		// 		},
		// 		files: {
		// 			'static/js/built.min.js': ['static/js/built.js']
		// 		}
		// 	}
		// },

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
      },

    // Empties folders to start fresh
    clean: {
      dist: {
        files: [{
          dot: true,
          src: [
            '.tmp',
            '<%= app.dist %>/scripts/*.js',
            '<%= app.dist %>/styles/*.css',
            '<%= app.dist %>/img/*',
            '<%= app.dist %>/fonts/*'
          ]
        }]
      },
      server: '.tmp'
    },

    'bower-install': {

      target: {

        // Point to the files that should be updated when
        // you run `grunt bower-install`
        src: ['<%= app.index %>'],

        // Optional:
        // ---------
        cwd: '',
        ignorePath: '',
        exclude: [],
        fileTypes: {}
      }
    },

    // Reads HTML for usemin blocks to enable smart builds that automatically
    // concat, minify and revision files. Creates configurations in memory so
    // additional tasks can operate on them
    useminPrepare: {
      html: '<%= app.index %>',
      options: {
        dest: './',
        root: './',
      }
    },

    // Allow the use of non-minsafe AngularJS files. Automatically makes it
    // minsafe compatible so Uglify does not destroy the ng references
    ngmin: {
      dist: {
        files: [{
          expand: true,
          cwd: '.tmp/concat/scripts',
          src: '*.js',
          dest: '.tmp/concat/scripts'
        }]
      }
    },

    // Copies remaining files to places other tasks can use
    copy: {
      dist: {
        files: [{
          expand: true,
          dot: true,
          cwd: '<%= app.source %>',
          dest: '<%= app.dist %>',
          src: [
            '*.{ico,png,txt}',
            'app/{,*/}*.html',
            '../bower_components/**/*',
            'img/*',
            'fonts/*'
          ]
        }, {
          expand: true,
            cwd: '.tmp/img',
            dest: '<%= app.dist %>/img',
            src: ['generated/*']
          }, {
            expand: true,
            flatten: true,
            dest: '<%= app.dist %>',
            src: '<%= app.index %>'
          }]
      }
    },
    // Renames files for browser caching purposes
    rev: {
      dist: {
        files: {
          src: [
            '<%= app.dist %>/scripts/{,*/}*.js',
            '<%= app.dist %>/styles/{,*/}*.css',
            '<%= app.dist %>/img/*',
            '<%= app.dist %>/fonts/*'
          ]
        }
      }
    },

    // Performs rewrites based on rev and the useminPrepare configuration
    usemin: {
      html: ['<%= app.dist %>/{,*/}*.html'],
      css: ['<%= app.dist %>/styles/{,*/}*.css'],
      // options: {
      //   assetsDirs: ['<%= app.dist %>']
      // }
    },

    htmlmin: {
      dist: {
        options: {
          collapseWhitespace: true,
          collapseBooleanAttributes: true,
          removeCommentsFromCDATA: true,
          removeOptionalTags: true
        },
        files: [{
          expand: true,
          cwd: '<%= app.index %>',
          src: ['*.html', 'partials/{,*/}*.html'],
          dest: '<%= app.dist %>'
        }]
      }
    },
    uncss: {
    dist: {
      files: [
        { src: ['<%= app.index %>', '<%= app.source%>/app/partials/*.html'], dest: '<%= app.dist %>/styles/style.css'}
      ]
      },
      options: {
        compress:true
      }
    }

  });


};
