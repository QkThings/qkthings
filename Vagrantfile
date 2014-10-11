# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.box = "ubuntu/trusty32"
  config.vm.network "forwarded_port", guest: 80, host: 8080
  
  config.vm.provider "virtualbox" do |vb|
	vb.customize ['modifyvm', :id, '--usb', 'on']
    vb.customize ["setextradata", :id, "VBoxInternal2/SharedFoldersEnableSymlinksCreate/v-root", "1"]
  end
  
  config.vm.provision :shell, :path => "dev/shell/bootstrap.sh"
  
  config.vm.provision :puppet do |puppet|
    puppet.manifests_path = "dev/puppet/manifests"
    puppet.manifest_file  = "main.pp"
  end
end
