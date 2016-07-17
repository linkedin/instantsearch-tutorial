# Assignment 0

The goal of this assignment is get your system in shape to build and run the instantsearch tutorial. We list out the dependencies and provide step by step instructions on setting them up for different platforms.

### Requirements
- [Java 8](http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html)
- [Elasticsearch 2.3.4](https://www.elastic.co/downloads/elasticsearch)
- [Python 2.7](https://www.python.org/downloads/)
- [Pycharm IDE](https://www.jetbrains.com/pycharm/download/) (*optional*)
- [VirtualBox](https://www.virtualbox.org/wiki/Downloads) (*if using virtual machine*)

### Mac and Linux
Run the following commands to setup the python environment and run elasticsearch on your machine.

```sh
$ mkdir ~/workspace
$ cd ~/workspace
$ git clone https://github.com/linkedin/instantsearch-tutorial.git
$ cd ~/workspace/instantsearch-tutorial/instantsearch-assignments/assigment0/exercise
$ sudo easy_install pip
$ sudo pip install -r requirements.txt
$ unzip elasticsearch-2.3.4.zip -d ~/workspace/instantsearch-tutorial
$ ~/workspace/instantsearch-tutorial/elasticsearch-2.3.4/bin/elasticsearch
```

### Ubuntu Virtual Machine
The virtual machine is currently running Ubuntu and has all the dependencies setup for you. This is a good option if you do not want to corrupt or change things in *python* installed on your machine. 
* [Virtual Box VM Download](https://drive.google.com/open?id=0B1eBBrAnKVJlbnVCZ2wwbWxqS2c)

**Username**: instantsearch 
**Password**:1

### End Result
At the end of this assignment you should have your python enviroment ready and elasticsearch running on port 9200. 
