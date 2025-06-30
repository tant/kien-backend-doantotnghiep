#!/bin/bash

# Function to generate random float in range
random_float() {
    local min=$1
    local max=$2
    local range=$(echo "$max - $min" | bc)
    echo "scale=1; $min + $RANDOM/32768 * $range" | bc
}

# Get current date and time
current_date=$(date +%Y-%m-%d)
current_hour=$(date +%H)
current_hour_rounded=$((current_hour - current_hour % 3))

# Loop through last 10 days
for day in {9..0}; do
    # Get the date for this iteration
    this_date=$(date -d "$current_date -$day days" +%Y-%m-%d)
    
    # Loop through fixed hours of the day
    for hour in 0 3 6 9 12 15 18 21; do
        # Skip future timestamps for current day
        if [ "$this_date" = "$current_date" ] && [ $hour -gt $current_hour_rounded ]; then
            continue
        fi
        
        # Calculate timestamp
        sample_ts=$(date -d "$this_date $hour:00:00" -u +"%Y-%m-%dT%H:%M:%S.000Z")
        
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
            \"description\": \"cayot1\",
            \"soil_moisture\": $soil2,
            \"timestamp\": \"$sample_ts\"
        }"
        echo
        
        # Sleep a bit to avoid overwhelming the server
        sleep 0.5
    done
done

echo "Done creating sample data!"
