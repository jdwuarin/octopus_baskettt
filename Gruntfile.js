module.exports = function(grunt) {

  // Load grunt tasks automatically
  require('load-grunt-tasks')(grunt);

  // Shows execution time
  require('time-grunt')(grunt);

  // Default task(s).
  grunt.registerTask('test-watch', ['karma:watch']);
  grunt.registerTask('test', ['karma:unit']);
  grunt.registerTask('production',[
    'clean:dist',
    'copy:dist',
    'useminPrepare',
    'less',
    'concat',
    'ngmin',
    'copy:dist',
    'uglify',
    'usemin',
    'busting'
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
      index: 'octopus_groceries/templates/products/index_dev.html',
      indexFolder: 'octopus_groceries/templates/products/',
      source: 'assets',
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
            '<%= app.dist %>/fonts/*',
            '<%= app.dist %>/app/*'
          ]
        }]
      }
    },

    // Reads HTML for usemin blocks to enable smart builds that automatically
    // concat, minify and revision files. Creates configurations in memory so
    // additional tasks can operate on them
    useminPrepare: {
      html: '<%= app.indexFolder %>/index_prod.html',
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
          cwd: '.tmp/concat/static/scripts',
          src: '*.js',
          dest: '.tmp/concat/static/scripts'
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
            dest: 'octopus_groceries/templates/products/',
            src: '<%= app.index %>',
            rename: function(dest, src) {
              return dest+'index_prod.html';
            }
          }]
      }
    },

    // Performs rewrites based on rev and the useminPrepare configuration
    usemin: {
      html: ['<%= app.indexFolder %>/index_prod.html'],
      css: ['<%= app.dist %>/styles/{,*/}*.css'],
    },

    busting: {
      dist:{
        html: '<%= app.indexFolder %>index_prod.html',
        dest: '<%= app.dist %>',
        assetsList : [
        'static/scripts/scripts.js',
        'static/scripts/vendor.js',
        'static/styles/style.css']
      }
    },
    watch: {
      scripts: {
        files: ['**/*.js','**/*.less'],
        tasks: ['reload'],
        options: {
          spawn: false,
        },
      },
    },
    reload: {
        port: 6001,
        proxy: {
            host: 'localhost'
        }
    }

  });

  grunt.task.registerMultiTask('busting', 'Cache busting',
    function() {

      var crypto = require('crypto'),
       fs = require('fs'),
       path = require('path');

      var htmlFile = this.data.html,
      destFolder = this.data.dest,
      assetsList = this.data.assetsList,
      newFilepath = [],
      htmlPath;

      // Rename the files
      assetsList.forEach(function(filepath){

        htmlPath = path.resolve(path.dirname(filepath), htmlFile);
        var hash = crypto.createHash('md5');

        hash.update(grunt.file.read(filepath), 'utf8');

        var hash_temp = hash.digest('hex'),
        prefix = hash_temp.slice(0, '8'),
        renamed = [prefix, path.basename(filepath)].join('.'),
        outPath = path.resolve(path.dirname(filepath), renamed);

        if(path.extname(renamed) === ".css"){
           newFilepath.push({src: filepath, dest: destFolder + '/styles/' + renamed});
        } else if(path.extname(renamed) === ".js"){
           newFilepath.push({src: filepath, dest: destFolder + '/scripts/' + renamed});
        } else {
          grunt.log.writeln("Invalid file format");
        }

        grunt.log.writeln("Rename " + filepath + " to " + outPath);

        fs.renameSync(filepath, outPath);
      });

      var text = fs.readFileSync(htmlFile,'utf8'),
      result;

      newFilepath.forEach(function(obj){

        result = text.replace(obj.src, obj.dest ,"gi");
        text = result;
        grunt.log.writeln("Replace " + obj.src + " to " + obj.dest);
      });

      fs.writeFileSync(htmlFile,result, 'utf8', function(err){

        if (err) return console.log(err);
       });

  });

};
