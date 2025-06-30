#!/bin/bash

# Function to generate random float in range
random_float() {
    local min=$1
    local max=$2
    local range=$(echo "$max - $min" | bc)
    echo "scale=1; $min + $RANDOM/32768 * $range" | bc
}

# Get current hour and round down to nearest 3-hour mark
current_hour=$(date +%H)
last_3hour_mark=$((current_hour - current_hour % 3))

# Get current date and time in seconds
current_ts=$(date +%s)
current_day_start=$(date -d "@$current_ts" +%Y-%m-%d)
current_day_start_ts=$(date -d "$current_day_start" +%s)

# Loop through last 10 days
for day in {9..0}; do
    # Get start of each day
    day_start_ts=$(date -d "$current_day_start -$day days" +%s)
    
    # For each day, create samples at fixed hours (0,3,6,9,12,15,18,21)
    for hour in {0..21..3}; do
        # Skip future timestamps
        if [ $day -eq 0 ] && [ $hour -gt $last_3hour_mark ]; then
            continue
        fi
        
        # Calculate timestamp
        sample_ts=$(date -d "@$((day_start_ts + hour * 3600))" -u +"%Y-%m-%dT%H:%M:%S.000Z")
        
        # Generate random values
        temp=$(random_float 20 30)    # Temperature between 20-30°C
        humid=$(random_float 60 80)   # Humidity between 60-80%
        press=$(random_float 1010 1015) # Pressure between 1010-1015 hPa
        soil1=$(random_float 35 45)    # Soil moisture between 35-45%
        soil2=$(random_float 40 50)    # Soil moisture between 40-50%
        
        # Create air sample
        curl -X POST "http://localhost:8000/air/samples/with-timestamp/" \
        -H "Content-Type: application/json" \
        -d "{
            \"temperature\": $temp,
            \"humidity\": $humid,
            \"pressure\": $press,
            \"timestamp\": \"$sample_ts\"
        }"
        echo
        
        # Create soil samples for two different locations
        curl -X POST "http://localhost:8000/soil/samples/with-timestamp/" \
        -H "Content-Type: application/json" \
        -d "{
            \"description\": \"bapcai1\",
            \"soil_moisture\": $soil1,
            \"timestamp\": \"$sample_ts\"
        }"
        echo
        
        curl -X POST "http://localhost:8000/soil/samples/with-timestamp/" \
        -H "Content-Type: application/json" \
        -d "{
            \"description\": \"bapcai1\",
            \"soil_moisture\": $soil2,
            \"timestamp\": \"$sample_ts\"
        }"
        echo
        
        # Sleep a bit to avoid overwhelming the server
        sleep 0.5
    done
done

echo "Done creating sample data!"
