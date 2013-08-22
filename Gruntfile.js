module.exports = function(grunt) {

  // Project configuration.
	grunt.initConfig({
		pkg: grunt.file.readJSON('package.json'), //To read the values of the package.json file
		
		less: {
			compile: {
				options: {
					paths:["./octopusapp/static/less"], //Directory to check for @imports
					yuicompress: true,
					strictImports: true //Force evaluation of imports.
				},
				files: {
					"./octopusapp/static/css/style.css": "./octopusapp/static/less/style.less",
				},

			},
			
			bootstrap: {
				options: {
					paths:["./octopusapp/static/bootstrap/less"],
					yuicompress: true,
					strictImports: true //Force evaluation of imports.
				},
				files: {
					"./octopusapp/static/bootstrap/css/bootstrap.css": "./octopusapp/static/bootstrap/less/bootstrap.less"
				},
			}
		}
	});

	// Load the plugin that provides the "less" task.
	grunt.loadNpmTasks('grunt-contrib-less');

	// Default task(s).
	grunt.registerTask('default', ['less']);

};