#!/bin/sh

# Syncronizing the database to our local copy of it
local_folder="/home/juan/Desktop/database_migration/caco_run_information"
printf "Syncronizing the CaCo runs information to: "
rsync lst101:/var/log/lst-camera/Caco/run_information/* $local_folder

# Connecting to the databases IPs
# TCU database
gnome-terminal -- ssh lst101 -L27017:127.0.0.1:27017
# CaCo database
gnome-terminal -- ssh lst101 -L27018:127.0.0.1:27018


