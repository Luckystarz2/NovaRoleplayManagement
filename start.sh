#!/bin/bash

echo "Starting NovaRoleplayManagement..."

# start dashboard in background
python dashboard/app.py &

# start bot in foreground
python bot/main.py