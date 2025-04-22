#!/bin/bash
# stop_web_app.sh: Stop all honcho and related web app processes cleanly
# Usage: ./stop_web_app.sh

set -e

# Find and kill honcho process
HONCHO_PIDS=$(pgrep -f 'honcho')
if [ -n "$HONCHO_PIDS" ]; then
    echo "Killing honcho process(es): $HONCHO_PIDS"
    kill $HONCHO_PIDS
fi

# Give processes a moment to terminate
sleep 2

# Kill any lingering Django, Celery, or Redis processes related to the project
for PROC in 'manage.py runserver' 'celery' 'redis-server'; do
    PIDS=$(pgrep -f "$PROC")
    if [ -n "$PIDS" ]; then
        echo "Killing lingering $PROC process(es): $PIDS"
        kill $PIDS
    fi
    # Give them a moment to terminate
    sleep 1
    # Force kill if still alive
    PIDS=$(pgrep -f "$PROC")
    if [ -n "$PIDS" ]; then
        echo "Force killing $PROC process(es): $PIDS"
        kill -9 $PIDS
    fi
    sleep 1
done

echo "All web app processes stopped."
