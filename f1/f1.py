from tabulate import tabulate as tb  #for displaying data in a tabular format

# global variables to store driver and lap data
driver_data = []  # list to store lap data for all drivers
racer_info = {}  # dictionary to store driver details (code, name, and team)

# function to read driver data from a file and store it in racer_info
def racer_data(file):   
    with open(file, "r") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) == 4:  # ensure the line has all required fields
                code, full_name, team = parts[1], parts[2], parts[3]
                racer_info[code] = {"name": full_name, "team": team}

# function to read and store lap data from a file
def lap_data_store(lap_file, lap_no):
    with open(lap_file, 'r') as lap:
        next(lap)  # skip the first line (location info)
        for line in lap:
            driver_code = line[:3]  # extract driver code (first 3 characters)
            speed = float(line[3:].strip())  # extract speed and convert to float
            if driver_code in racer_info:  # check if driver exists in racer_info
                full_name = racer_info[driver_code]["name"]
                team = racer_info[driver_code]["team"]
            else:
                full_name = "unknown"  # handle unknown drivers
                team = "unknown"
            # append driver details and speed to driver_data
            driver_data.append({"driver": driver_code,
                                "full name": full_name,
                                "team": team,
                                "car speed": speed,
                                "lap": lap_no})

# function to display race location
def race_name(lap_file, lap_no):
    """
    Reads the first line of the lap file to determine the race location.
    """
    with open(lap_file, 'r') as f:
        location = f.readline().strip() # Read the first line as the location
        print(f"Lap {lap_no} race is in {location}.")

# function to find the fastest racer in a given lap
def fastest_racer(lap_no):
    """
    Identifies the fastest racer for the specified lap based on speed.
    """
    lap_data = [entry for entry in driver_data if entry["lap"] == lap_no]
    fastest = max(lap_data, key=lambda x: x["car speed"])
    print(f"the fastest racer in lap {lap_no}:")
    print(
        f"Driver: {fastest['full name']} ({fastest['driver']}), team: {fastest['team']}, speed: {fastest['car speed']:.3f}")

# function to display each driver's fastest lap
def fast_individual_racer():
    """
    Finds the fastest lap time for each driver and displays it in a table.
    """
    individual_drive_speed = {}
    for entry in driver_data:
        driver = entry["driver"]
        speed = float(entry["car speed"])
        # Store the fastest speed for each driver
        if driver not in individual_drive_speed or speed < individual_drive_speed[driver]["speed"]:
            individual_drive_speed[driver] = {
                "full name": entry["full name"],
                "team": entry["team"],
                "speed": speed
            }
    # Create a table for the data
    table = [{"driver": info["full name"], "Team": info["team"], "fastest time": info["speed"]}
             for info in individual_drive_speed.values()]
    print("individual fastest time of every racer:")
    print(tb(table, headers="keys", tablefmt="fancy_grid"))

# function to display drivers' fastest laps in descending order
def fast_individual_racer_descending():
    """
    Displays the fastest lap times for all drivers in descending order.
    """
    individual_drive_speed_descend = {}
    for entry in driver_data:
        driver = entry["driver"]
        speed = float(entry["car speed"])
        # Store the fastest speed for each driver
        if driver not in individual_drive_speed_descend or speed < individual_drive_speed_descend[driver]["speed"]:
            individual_drive_speed_descend[driver] = {
                "full name": entry["full name"],
                "team": entry["team"],
                "speed": speed
            }
    # Prepare table sorted in descending order
    table = [{"driver": info["full name"], "Team": info["team"], "fastest time": info["speed"]}
             for info in individual_drive_speed_descend.values()]
    table.sort(key=lambda x: x["fastest time"], reverse=True)   # Sort the table by fastest time in descending order
    print("individual fastest time of every racer(in descending order):")
    print(tb(table, headers="keys", tablefmt="fancy_grid"))

# Function to calculate and print the average speed of all racers
def average_speed_racers():
    total_speed = sum(entry["car speed"] for entry in driver_data)
    total_driver = len(driver_data)
    if total_driver:    # Calculate average speed and handle the case with no data
        average_time = total_speed / total_driver
        print(f"the average time of overall racers is: {average_time:.2f}")
    else:
        print("no data on driver.")

# Function to calculate and display each driver's average speed
def average_speed_individual():
    """
    Calculates and displays the average speed for each driver across all laps.
    """
    racer_average = {}
    for entry in driver_data:
        driver = entry["driver"]
        speed = float(entry["car speed"])
        if driver not in racer_average: # Aggregate speed data for each driver
            racer_average[driver] = {"total time": 0, "count": 0, "full name": entry["full name"],
                                     "team": entry["team"]}
        racer_average[driver]["total time"] += speed
        racer_average[driver]["count"] += 1
    # Calculate average speed for each driver
    average = [{"driver": data["full name"], "team": data["team"],
                "average time": data["total time"] / data["count"]}
               for data in racer_average.values()]
    # Sort the data by average time in descending order
    average.sort(key=lambda x: x["average time"], reverse=True)
    print("average speed of every racer:")
    print(tb(average, headers="keys", tablefmt="fancy_grid"))

# Main menu function to interact with the user
def option():
    print("Made By: Amit Chaudhary")
    while True:
        print("menu")
        print("1. lap1")
        print("2. lap2")
        print("3. lap3")
        print("4. exit")
        choice = input("choose a lap:")

        # Handle invalid input
        if choice not in ["1", "2", "3", "4"]:
            print("invalid choice, please try again.")
            continue
        elif choice == "4":
            print("exiting the data.")
            break
        else:
            lap_no = int(choice)
            race_name(f"project1/lap_times_{lap_no}.txt", lap_no)

            # Submenu for lap-specific options
            while True:
                print(f"lap{lap_no} option:")
                print("1. fastest Racer:")
                print("2. individual speed list")
                print("3. individual speed list(descending)")
                print("4. average speed")
                print("5. individual average list")
                print("6. back to main menu")
                sub_choice = input("choose the option:")

                # Handle user choices
                if sub_choice == "1":
                    fastest_racer(lap_no)

                elif sub_choice == "2":
                    fast_individual_racer()

                elif sub_choice == "3":
                    fast_individual_racer_descending()

                elif sub_choice == "4":
                    average_speed_racers()

                elif sub_choice == "5":
                    average_speed_individual()

                elif sub_choice == "6":
                    break

                else:
                    print("invalid choice. please enter again.")

# Load driver and lap data
racer_data("project1/f1_drivers.txt")
lap_data_store("project1/lap_times_1.txt", 1)
lap_data_store("project1/lap_times_2.txt", 2)
lap_data_store("project1/lap_times_3.txt", 3)
# Start the menu
option()
