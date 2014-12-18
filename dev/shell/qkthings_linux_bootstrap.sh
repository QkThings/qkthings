#!/bin/bash
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
  if test "$(ls -A "$1/$2" 2>/dev/null)"; then
    echo "! $2 already cloned"
  else
    cd $1
    git clone http://github.com/qkthings/$2
  fi
}

append_to_file () {
  if test "$(cat $1 | grep "$2" 2>/dev/null)" ; then
    echo -e "$2 is already in $1"
  else
    echo -e "Setting $2 in $1"
    echo $2 >> $1
  fi
}

if [ -z $1 ]; then
  ROOT_DIR=/home/$SUDO_USER
else
  ROOT_DIR=$1
fi

echo -e "\nBootstrap QkThings here: $ROOT_DIR"
if ! confirm ; then
  echo "Aborted"
  return
elif [ ! -d "$ROOT_DIR" ]; then
  mkdir -p $ROOT_DIR
fi

QKTHINGS_DIR=$ROOT_DIR/qkthings
QKTHINGS_LOCAL=/home/$SUDO_USER/qkthings_local
DEV_DIR=$QKTHINGS_DIR/dev
TOOLCHAIN_DIR=$QKTHINGS_LOCAL/toolchain

echo QKTHINGS_DIR=$QKTHINGS_DIR
echo QKTHINGS_LOCAL=$QKTHINGS_LOCAL

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
install_package qtchooser

clone_repo $ROOT_DIR qkthings

clone_repo $QKTHINGS_DIR embedded
clone_repo $QKTHINGS_DIR/embedded qkprogram
clone_repo $QKTHINGS_DIR/embedded qkperipheral
clone_repo $QKTHINGS_DIR/embedded qkdsp

clone_repo $QKTHINGS_DIR/embedded/board comm_bt_2_0

clone_repo $QKTHINGS_DIR software
clone_repo $QKTHINGS_DIR/software qkcore
clone_repo $QKTHINGS_DIR/software qkwidget
clone_repo $QKTHINGS_DIR/software qkapi
clone_repo $QKTHINGS_DIR/software qkdaemon
clone_repo $QKTHINGS_DIR/software qkide
clone_repo $QKTHINGS_DIR/software qkloader

mkdir -p $ROOT_DIR/specs
clone_repo $ROOT_DIR/specs spec_qkprotocol


cd $DEV_DIR
echo "Installing/checking embedded toolchain"
sudo python python/qkthings/toolman.py -t arduino -r $TOOLCHAIN_DIR --dist=linux
sudo python python/qkthings/toolman.py -t efm32 -r $TOOLCHAIN_DIR --dist=linux

cd $DEV_DIR/python
echo "Installing Python tools"
sudo python setup.py install

cd ~/Downloads
wget $QTSDK_URL --timestamp --ignore-length
chmod +x $QTSDK_RUN
./$QTSDK_RUN

echo "Setting up Qt"
QTCHOOSER_DIR=/usr/lib/i386-linux-gnu/qtchooser/
cd $QTCHOOSER_DIR
rm qt5.conf
echo -e "/opt/Qt5.3.2/5.3/gcc/bin/\n/opt" >> qt5.conf
cp qt5.conf default.conf

adduser $SUDO_USER dialout

chown -R $SUDO_USER /home/$SUDO_USER/.config
chown -R $SUDO_USER $QKTHINGS_DIR
chown -R $SUDO_USER $QKTHINGS_LOCAL

append_to_file ~/.bashrc "alias make=colormake"
append_to_file ~/.profile "export QKTHINGS_DIR=$QKTHINGS_DIR"
append_to_file ~/.profile "export QKTHINGS_LOCAL=$QKTHINGS_LOCAL"

source ~/.profile

echo -e QKTHINGS_DIR=$QKTHINGS_DIR
echo -e QKTHINGS_LOCAL=$QKTHINGS_LOCAL
echo -e "You should re-login."

echo -e "\nDone! Now what?"
echo -e "Building instructions: http://discourse.qkthings.com/t/building-instructions/20"
echo -e "Give feedback, don't hesitate to get in touch. Happy hacking!"
