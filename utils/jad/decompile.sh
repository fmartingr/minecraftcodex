#!/bin/bash

# Remove old
rm -rf ./jarfile ./classes

# Create directories
mkdir jarfile
mkdir classes

# Decompress the jarfile into the jarfile folder
unzip jarfile.jar -d ./jarfile

# Find all the classes and pass then through JAD
#find . -type d -name *.class -exec rm -rf {} \;
ls ./jarfile/*.class | xargs -n1 ./jad -sjava -dclasses 

# Remove classfiles and left only other files
rm ./jarfile/*.class
