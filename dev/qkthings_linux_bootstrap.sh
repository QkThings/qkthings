#!/bin/sh
#set -x

QKTHINGS_DIR=~/qkthings
DEV_DIR=$QKTHINGS_DIR/dev

TOOLCHAIN_DIR=$QKTHINGS_DIR/embedded/shared/toolchain

QTSDK_URL=http://download.qt-project.org/archive/qt/5.1/5.1.1/qt-linux-opensource-5.1.1-x86-offline.run
QTSDK_RUN=qt-linux-opensource-5.1.1-x86-offline.run

if [ $(/usr/bin/id -u) -ne 0 ]; then
    echo "Please run this script as sudo"
    return
fi

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

install_package git
install_package git-cola
install_package meld
install_package build-essential
install_package colormake
install_package doxygen
install_package freeglut3-dev
install_package libusb-dev

if [ ! -d "$QKTHINGS_DIR" ]; then
  cd ~
  git clone https://github.com/qkthings/qkthings
  chown -R $SUDO_USER $QKTHINGS_DIR
fi

clone_repo $QKTHINGS_DIR/embedded/ qkprogram
clone_repo $QKTHINGS_DIR/embedded/ qkperipheral
clone_repo $QKTHINGS_DIR/embedded/ qkdsp

clone_repo $QKTHINGS_DIR/software/ qkcore
clone_repo $QKTHINGS_DIR/software/ qkwidget
clone_repo $QKTHINGS_DIR/software/ qkapi
clone_repo $QKTHINGS_DIR/software/ qkdaemon
clone_repo $QKTHINGS_DIR/software/ qkide
clone_repo $QKTHINGS_DIR/software/ qkloader

cd $DEV_DIR
echo "Installing/checking embedded toolchain"
sudo python toolman.py -t arduino -r $TOOLCHAIN_DIR --dist=linux
sudo python toolman.py -t efm32 -r $TOOLCHAIN_DIR --dist=linux

cd ~/Downloads
wget $QTSDK_URL --timestamp --ignore-length
chmod +x $QTSDK_RUN
./$QTSDK_RUN

chown -R $SUDO_USER ~/.config

adduser $SUDO_USER dialout

if test "$(cat ~/.bashrc | grep "make=colormake" 2>/dev/null)" ; then
echo "make is already colormake"
else
echo "alias make=colormake" >> ~/.bashrc
fi

echo "\nDone! Now what?"
echo "Building instructions: http://discourse.qkthings.com/t/building-instructions/20"
echo "Give feedback, don't hesitate to get in touch. Happy hacking!"




