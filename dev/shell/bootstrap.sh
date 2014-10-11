#!/bin/sh

DEV_DIR=/vagrant/dev
PUPPET_DIR=/etc/puppet/

TOOLCHAIN_TAR=toolchain.tar.bz2
TOOLCHAIN_URL=http://qkthings.com/files/shared/$TOOLCHAIN_TAR
TOOLCHAIN_DIR=/home/vagrant/local/toolchain

install_package () {
  if [ $(dpkg-query -W -f='${Status}' $1 2>/dev/null | grep -c "ok installed") -eq 0 ]; then
    apt-get -y install $1
  else
    echo "$1 is already installed."
  fi
}

install_package git
install_package build-essential
install_package ruby-dev

if [ ! -d "$PUPPET_DIR" ]; then
  mkdir -p $PUPPET_DIR
fi
cp /vagrant/dev/puppet/Puppetfile $PUPPET_DIR

if [ "$(gem list -i '^librarian-puppet$')" = "false" ]; then
  gem install librarian-puppet
  cd $PUPPET_DIR && librarian-puppet install --clean
else
  cd $PUPPET_DIR && librarian-puppet update
fi

cd $DEV_DIR
echo "Installing/checking embedded toolchain"
sudo python toolman.py -t arduino -r $TOOLCHAIN_DIR --dist=linux
sudo python toolman.py -t efm32 -r $TOOLCHAIN_DIR --dist=linux

