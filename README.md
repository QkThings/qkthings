# QkThings

![](/logo.png "QkThings")

QkThings is both a **framework** and a **modular prototyping platform** for **smart devices**. 

This is the main git repository of QkThings. This is also a private repo and since you are able to read this text, I guess you are a very important person. Feel free to contribute and share your opinions.


----
## Development Guidelines

QkThings is divided into three main components:

* **hardware**: schematic and layout files (the physical boards)
* **embedded**: firmware that runs inside the microcontrollers (low level stuff)
* **software**: high level applications that interact with the boards (graphical user interfaces, easy-to-use APIs...)

Each one of these components may include several projects, each one containing its own git repository. To keep things organized and easier to maintain, when cloning those repositories you should keep the following structure:

	qkthings
	    embedded
	        shared
	        (repos)
	    software
	        shared
	        (repos)
	    hardware  

This is specially important if you need to compile a project that expects to find some files in a specific relative path inside the *shared* folder. *shared* folder is used to store common files (e.g. executables, libraries, toolchains)

If some of the described folders doesn't exists in this repo, that means it is currently empty.

----
## Tools / Requirements

You may use Eclipse with projects inside *embedded* folder. GUI applications, inside *software* folder, are developed with Qt 5.1. Other specific requirements may be described in the project repo.

* Git
* [Eclipse IDE for C/C++ Developers](http://www.eclipse.org/downloads/packages/eclipse-ide-cc-developers/keplersr1)
* [Qt 5.1](http://qt-project.org/downloads)


----
### Additional Downloads

* [embedded_toolchain.zip](https://copy.com/hFc4tfrb2kdtUuDe): required by embedded projects, must be extracted to *embedded/shared* folder, contains toolchain for ARM and Arduino
