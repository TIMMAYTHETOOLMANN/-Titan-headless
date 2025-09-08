#!/bin/bash

# Function to validate and log errors
validate_and_log() {
    echo "Validating setup..."
    python titan_headless_bot.py --validate
    if [ $? -ne 0 ]; then
        echo "Validation failed. Check the logs for details."
        exit 1
    else
        echo "Validation successful."
    fi
}

# Function to check and update configuration files
check_config_files() {
    if [ ! -f "enhanced_nexus_config.yaml" ]; then
        echo "enhanced_nexus_config.yaml not found. Please ensure it exists and is correctly configured."
        exit 1
    fi

    if [ ! -f "proxies.txt" ]; then
        echo "proxies.txt not found. Please ensure it exists and contains valid proxies."
        exit 1
    fi
}

# Function to run the bot with specific configurations
run_bot() {
    echo "Running the bot with specified configurations..."
    python titan_headless_bot.py --youtube 25 --twitch 20 --kick 15 --run
}

# Function to update stream URLs and viewer counts
update_stream_urls() {
    echo "Updating stream URLs and viewer counts..."
    python titan_headless_bot.py --youtube 50 --youtube-url "https://youtube.com/live/new-stream" --twitch 30 --twitch-url "https://twitch.tv/yourstream" --kick 20 --kick-url "https://kick.com/yourstream" --run
}

# Function to check the current status
check_status() {
    echo "Checking current status..."
    python titan_headless_bot.py --status
}

# Main script execution
validate_and_log
check_config_files
run_bot
update_stream_urls
check_status

echo "Optimization script completed."