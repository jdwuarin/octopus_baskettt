module.exports = function(grunt) {

  // Project configuration.
	grunt.initConfig({
		pkg: grunt.file.readJSON('package.json'), //To read the values of the package.json file
		
		less: {
			compile: {
				options: {
					paths:["project/octopusProducts/static/less"], //Directory to check for @imports
					yuicompress: true,
					strictImports: true //Force evaluation of imports.
				},
				files: {
					"project/octopusProducts/static/css/style.css": "project/octopusProducts/static/less/style.less",
				},

			},
			
			bootstrap: {
				options: {
					paths:["project/octopusProducts/static/bootstrap/less"],
					yuicompress: true,
					strictImports: true //Force evaluation of imports.
				},
				files: {
					"project/octopusProducts/static/bootstrap/css/bootstrap.css": "project/octopusProducts/static/bootstrap/less/bootstrap.less"
				},
			}
		}
	});

	// Load the plugin that provides the "less" task.
	grunt.loadNpmTasks('grunt-contrib-less');

	// Default task(s).
	grunt.registerTask('default', ['less']);

};