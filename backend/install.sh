#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Updating system packages..."
sudo apt-get update

echo "Installing required system dependencies..."
sudo apt-get install -y \
    libreoffice \
    poppler-utils \
    ffmpeg
