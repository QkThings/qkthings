exec { 'sudo apt-get update':
    path => '/usr/bin/' }

package { 'git': }
package { 'qt5-default': }
package { 'qtcreator': }
package { 'libqt5serialport5-dev': }
	
$embedded_repos = [ qkprogram, qkperipheral, qkdsp ]
define clone_embedded_repo {
	vcsrepo { "/vagrant/embedded/$name":
		ensure => present,
		provider => git,
		source=> "git://github.com/qkthings/$name.git",
	}
}
clone_embedded_repo { $embedded_repos: }	

$software_repos = [ qkcore, qkwidget, qkide, qkdaemon ]
define clone_software_repo {
	vcsrepo { "/vagrant/software/$name":
		ensure => present,
		provider => git,
		source=> "git://github.com/qkthings/$name.git",
	}
}
clone_software_repo { $software_repos: }
