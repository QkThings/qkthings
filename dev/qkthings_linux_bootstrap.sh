#!/bin/sh
#set -x

if [ $(/usr/bin/id -u) -ne 0 ]; then
    echo "Please run this script as sudo"
    return
fi

confirm () {
while true; do
    read -p "Do you confirm? [y/n] " yn
    case $yn in
        [Yy]* ) return 0;;
        [Nn]* ) return 1;;
        * ) echo "Please answer yes or no";;
    esac
done
}

install_package () {
  if [ $(dpkg-query -W -f='${Status}' $1 2>/dev/null | grep -c "ok installed") -eq 0 ]; then
    apt-get -y install $1
  else
    echo "! $1 already installed"
  fi
}

clone_repo () {
  if test "$(ls -A "$1$2" 2>/dev/null)"; then
    echo "! $2 already cloned"
  else
    cd $1
    git clone http://github.com/qkthings/$2
  fi
}

if [ -z $1 ]; then
  ROOT_DIR=/home/$SUDO_USER/
else
  ROOT_DIR=$1

  echo "\nBootstrap QkThings here: $ROOT_DIR"
  if ! confirm ; then
    echo "Aborted"
    return
  else
    if [ ! -d "$ROOT_DIR" ]; then
      mkdir -p $ROOT_DIR
    fi
  fi
fi

QKTHINGS_DIR=$ROOT_DIR/qkthings
QKTHINGS_LOCAL=/home/$SUDO_USER
DEV_DIR=$QKTHINGS_DIR/dev
TOOLCHAIN_DIR=$QKTHINGS_LOCAL/qkthings_local/toolchain

QTSDK_URL=http://download.qt-project.org/archive/qt/5.3/5.3.2/qt-opensource-linux-x86-5.3.2.run
QTSDK_RUN=qt-opensource-linux-x86-5.3.2.run

install_package git
install_package git-cola
install_package meld
install_package build-essential
install_package colormake
install_package doxygen
install_package freeglut3-dev
install_package libusb-dev
install_package openssh-server

if [ ! -d "$QKTHINGS_DIR" ]; then
#  cd $ROOT_DIR
  #git clone https://github.com/qkthings/qkthings
  clone_repo $ROOT_DIR qkthings

  clone_repo $QKTHINGS_DIR/embedded/ qkprogram
  clone_repo $QKTHINGS_DIR/embedded/ qkperipheral
  clone_repo $QKTHINGS_DIR/embedded/ qkdsp

  clone_repo $QKTHINGS_DIR/software/ qkcore
  clone_repo $QKTHINGS_DIR/software/ qkwidget
  clone_repo $QKTHINGS_DIR/software/ qkapi
  clone_repo $QKTHINGS_DIR/software/ qkdaemon
  clone_repo $QKTHINGS_DIR/software/ qkide
  clone_repo $QKTHINGS_DIR/software/ qkloader
else
  echo "! $QKTHINGS_DIR already exists (repos won't be cloned)"
fi

cd $DEV_DIR
echo "Installing/checking embedded toolchain"
sudo python toolman.py -t arduino -r $TOOLCHAIN_DIR --dist=linux
sudo python toolman.py -t efm32 -r $TOOLCHAIN_DIR --dist=linux

cd ~/Downloads
wget $QTSDK_URL --timestamp --ignore-length
chmod +x $QTSDK_RUN
./$QTSDK_RUN

adduser $SUDO_USER dialout

chown -R $SUDO_USER /home/$SUDO_USER/.config
chown -R $SUDO_USER $QKTHINGS_DIR
chown -R $SUDO_USER $QKTHINGS_LOCAL

if test "$(cat ~/.bashrc | grep "make=colormake" 2>/dev/null)" ; then
echo "make is already colormake"
else
echo "alias make=colormake" >> ~/.bashrc
fi

echo "\nDone! Now what?"
echo "Building instructions: http://discourse.qkthings.com/t/building-instructions/20"
echo "Give feedback, don't hesitate to get in touch. Happy hacking!"
