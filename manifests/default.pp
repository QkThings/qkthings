exec { 'sudo apt-get update':
    path => '/usr/bin/' }

package { 'qt5-default': }
package { 'qtcreator': }
package { 'libqt5serialport5-dev': }
