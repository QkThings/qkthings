#!/bin/sh

PUPPET_DIR=/etc/puppet/
EMB_SHARED_DIR=/vagrant/embedded/shared
TOOLCHAIN_TAR=toolchain.tar.gz
TOOLCHAIN_URL=http://qkthings.com/files/shared/$TOOLCHAIN_TAR

apt-get -q -y update

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

if [ ! -d "$EMB_SHARED_DIR" ]; then
  mkdir -p $EMB_SHARED_DIR
fi

if [ ! -d "$EMB_SHARED_DIR/toolchain" ]; then
  cd $EMB_SHARED_DIR
  echo "Downloading $TOOLCHAIN_URL"
  wget $TOOLCHAIN_URL -q --timestamp --ignore-length
  echo "Extracting $TOOLCHAIN_TAR"
  tar xf $TOOLCHAIN_TAR
fi

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

