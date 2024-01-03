#!/bin/bash

# This script will install and upgrade various Python packages and setup Discord bot configuration

# ANSI escape code for green text
GREEN='\033[0;32m'
# ANSI escape code to reset text color
NC='\033[0m' # No Color

# Upgrade pip
pip3 install --upgrade pip

# Install discord.py
pip3 install discord.py

# Install python-dotenv
pip3 install python-dotenv

# Install Flask
pip3 install Flask

# Upgrade certifi
pip3 install --upgrade certifi

# Install node modules 
cd client && npm install
cd ..

# Compile the c program
gcc -o run run.c 

echo -e "${GREEN}Installation and upgrades complete!${NC}"

# Prompt user for Discord channel ID and bot token
read -p "Enter your Discord channel ID: " channel_id
read -p "Enter your Discord bot token: " bot_token

# Write these values to a .env file
echo "DISCORD_BOT_TOKEN=$bot_token" > flask-backend/.env
echo "CHANNEL_ID=$channel_id" >> flask-backend/.env

echo -e "${GREEN}Discord configuration saved in .env file${NC}"

