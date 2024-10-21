#
# File: WICLY003time_table.py
# Author: Lankani Samurdhika Wickrama Seneviratne
# Student ID: 110404252
# Email ID: WICLY003(wicly003@mymail.unisa.edu.au)
# This is my own work as defined by
# the University's Academic Misconduct Policy.
#

# defining the main function of the program with empty schedule for days of the week and event menu
def main():
    user_input = True
    events = {
    "Mon": [],
    "Tue": [],
    "Wed": [],
    "Thu": [],
    "Fri": [],
    "Sat": [],
    "Sun": [],
    }
    while user_input != 'q':
        user_input = input("""
        ===========================================================
        |                 Event Menu                              |
        |=========================================================|
        |       Press 0 to create an event                        |
        |       Press 1 to update an event                        |
        |       Press 2 to delete an event                        |
        |       Press 3 to display the timetable                  |
        |       Press 4 to display events on a specific date      |      
        |       Press 5 to save the timetable to a file           | 
        |       Press 6 to search scheduled events                |
        |       Press q to exist the programme                    |
        |=========================================================|
        
        Your choice:""")
        if user_input == '0':
            events = create_event(events)
        elif user_input == '1':
            events = update_event(events)
        elif user_input == '2':
            events = delete_event(events)
        elif user_input == '3':
            display_time_table(events)
        elif user_input == '4':
            display_event_on_specific_day(events)
        elif user_input == '5':
            save_time_table_to_file(events)
        elif user_input == '6':
            search_events(events)
        elif user_input.lower() == 'q':
            print('===============quit============')
        else:
            invalid_user_input()


# creating the event with event name, date, start time, end time and location
def create_event(events):
    event_name = input("Enter the name of the event: ")
    event_day = ""
    while not validate_day(event_day):
        event_day = input("Enter the day of the event (e.g., Mon, Tue, Wed, Thu, Fri, Sat, Sun): ")
        if not validate_day(event_day):
            print("Invalid day. Please enter a valid day.")
    event_start_time = ""
    event_start_time = input("Enter the start time of the event (e.g., 10:00 AM): ")
    
    while not validate_time(event_start_time):
        event_start_time = input("Invalid time format. Please enter a valid time (e.g., 10:00 AM): ")
    
    event_end_time = input("Enter the end time of the event (e.g., 12:00 PM): ")
    
    while not validate_time(event_end_time):
        event_end_time = input("Invalid time format. Please enter a valid time (e.g., 12:00 PM): ")

    event_location = input("Enter the location of the event: ")
    new_event  = {
        'name': event_name,
        'day': event_day,
        'start_at': event_start_time,
        'end_at': event_end_time,
        'place': event_location,
    }
    existing_events_on_day = events.get(event_day, [])
    for existing_event in existing_events_on_day:
        existing_start_time = existing_event['start_at']
        existing_end_time = existing_event['end_at']

        if is_time_overlap(existing_start_time, existing_end_time, event_start_time, event_end_time):
            print("Event time conflicts with an existing event. Please choose a different time slot")
            return events

    # If there are no time conflicts, add the new event to the events dictionary
    if event_day not in events:
        events[event_day] = []
    events[event_day].append(new_event)
    print('Event created successfully')
    return events


# updating an event based on the start time of the event
def update_event(events):
    day_to_update = input("Enter the day of the event to update (e.g., Mon, Tue, Wed, Thu, Fri, Sat, Sun): ")
    search_by_field = input("Enter the field name to search by [Name, Place, Start_At]: ")
    search_value = ''
    if search_by_field.lower() == 'name':
        search_value = input("Enter the event name to search the event (e.g., Lecture): ")
    elif search_by_field.lower() == 'place':
        search_value = input("Enter the place name to search the event (e.g., Hall A): ")
    else:
        search_value = input("Enter the start time of the event to update (e.g., 10:00 AM): ")

    if day_to_update in events:
        event_found = False
        for event in events[day_to_update]:
            if event[search_by_field.lower()].lower() == search_value.lower():
                event_found = True

                print(f"Event found: {event['name']}")
                new_event_name = input("Enter the new name of the event (press Enter to keep it unchanged): ")
                new_event_location = input("Enter the new location of the event (press Enter to keep it unchanged): ")

                if new_event_name:
                    event['name'] = new_event_name
                if new_event_location:
                    event['place'] = new_event_location

                print('Event updated successfully')

        if not event_found:
            print("No event found with the specified start time.")
    else:
        print("No events found for the specified day.")

    return events


# deleting an event
def delete_event(events):
    day_to_delete = input("Enter the day of the event to delete (e.g., Mon, Tue, Wed, Thu, Fri, Sat, Sun): ")
    search_by_field = input("Enter the field name to search by [Name, Place, Start_At]: ")
    search_value = ''
    if search_by_field.lower() == 'name':
        search_value = input("Enter the event name to search the event (e.g., Lecture): ")
    elif search_by_field.lower() == 'place':
        search_value = input("Enter the place name to search the event (e.g., Hall A): ")
    else:
        search_value = input("Enter the start time of the event (e.g., 10:00 AM): ")

    if day_to_delete in events:
        event_found = None
        for event in events[day_to_delete]:
            if event[search_by_field.lower()].lower() == search_value.lower():
                event_found = event

        if event_found is not None:
            print(f"Event found: {event_found['name']}")
            confirmation = input("Are you sure you want to delete this event? (Enter 'yes' to confirm): ")

            if confirmation.lower() == 'yes':
                events[day_to_delete].remove(event_found)
                print('Event deleted successfully')
            else:
                print('Event not deleted.')

        if event_found is None:
            print("No event found with the specified start time.")
    else:
        print("No events found for the specified day.")

    return events


# searching an event
def search_events(events):
    search_by = input("Search Events by [Name, Place]: ")
    search_key = input("Enter search key: ")
    filtered_events = {"Mon":[], "Tue":[],    "Wed": [], "Thu": [],"Fri": [], "Sat": [], "Sun": []}
    days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    sort_events_by_start_time(events)
    for day in days_of_week:
        for event in events[day]:
            if search_by.lower() in event and event[search_by.lower()] == search_key.lower():
                filtered_events[day].append(event)
    for day in days_of_week:
        if len(filtered_events[day]) > 0:
            print("="*30)
            print(day)
            print()
            for event in filtered_events[day]:
                print(f"Event Name: {event['name']}")
                print(f"Start Time: {event['start_at']}")
                print(f"End Time: {event['end_at']}")
                print(f"Location: {event['place']}")
                print('-' * 30)


#sorting the events
def sort_events_by_start_time(events):
    for day in events:
        events[day] = sorted(events[day], key=lambda event: event['start_at'])
    return events    


#displaying the time table
def display_time_table(events):
    sort_events_by_start_time(events)
    first_day = input("What should be the first day of the week (Mon / Sun)? ")
    # Define the days of the week
    days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    if first_day == 'Mon':
      days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    elif first_day == 'Sun':
      days_of_week = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]    

    # Print the table header with days of the week
    print(f"{'Time Slot':<20}|", end="")

    for day in days_of_week:
        print(f"{day:<15}|", end="")

    print()
    before_events = get_events_before_9am(events)
    now_events = get_event_between_9am_5pm(events)
    after_events = get_event_after_5pm(events)
    before_time = get_time_slots_before_9am(before_events)
    after_time = get_time_slots_after_5pm(after_events)

    time_slots = [
        "09:00 AM - 10:00 AM",
        "10:00 AM - 11:00 AM",
        "11:00 AM - 12:00 PM",
        "12:00 PM - 01:00 PM",
        "01:00 PM - 02:00 PM",
        "02:00 PM - 03:00 PM",
        "03:00 PM - 04:00 PM",
        "04:00 PM - 05:00 PM",
    ]
    print('-'* 135)
    for before_slot in before_time:
        print(f"{before_slot:<20}|", end="")
        for x in range(2):
            if x == 1:
               print(f"{' ':<20}|", end="") 
            for day in days_of_week:
                events_on_day = before_events[day]
                if len(events_on_day) == 0:
                    print(f"{' ':<15}|", end="")
                for event in events_on_day:
                    if event['end_at'] > before_slot:
                        if event['start_at'] <= before_slot:
                            if x == 0:
                                if len(event['name']) > 15:
                                    print(f"{(event['name'][:12]+ '...'):<15}|", end="")
                                else:
                                    print(f"{event['name']:<15}|", end="") 
                            else:
                                if len(event['place']) > 15:
                                    print(f"{(event['place'][:12]+ '...'):<15}|", end="")
                                else:
                                    print(f"{event['place']:<15}|", end="") 
                        else:
                            print(f"{' ':<15}|", end="")
                    else:
                        print(f"{' ':<15}|", end="")
            print()
        print('-'* 135)
    
    for slot in time_slots:
        print(f"{slot:<20}|", end="")
        for y in range(2):
            if y == 1:
               print(f"{' ':<20}|", end="") 
            for day in days_of_week:
                events_on_day = now_events[day]
                if len(events_on_day) == 0:
                    print(f"{' ':<15}|", end="")
                for event in events_on_day:
                    if event['end_at'] > slot:
                        if event['start_at'] <= slot:
                            if y == 0:
                                if len(event['name']) > 15:
                                    print(f"{(event['name'][:12]+ '...'):<15}|", end="")
                                else:
                                    print(f"{event['name']:<15}|", end="")
                            else:
                                if len(event['place']) > 15:
                                    print(f"{(event['place'][:12]+ '...'):<15}|", end="")
                                else:
                                    print(f"{event['place']:<15}|", end="")  
                        else:
                            print(f"{' ':<15}|", end="")
                    else:
                        print(f"{' ':<15}|", end="")
            print()
        print('-'* 135)
    
    for after_slot in after_time:
        print(f"{after_slot:<20}|", end="")
        for z in range(2):
            if z == 1:
               print(f"{' ':<20}|", end="") 
            for day in days_of_week:
                events_on_day = after_events[day]
                if len(events_on_day) == 0:
                    print(f"{' ':<15}|", end="")
                for event in events_on_day:
                    if event['end_at'] > after_slot:
                        if event['start_at'] <= after_slot:
                            if z == 0:
                                if len(event['name']) > 15:
                                    print(f"{(event['name'][:12]+ '...'):<15}|", end="")
                                else:
                                    print(f"{event['name']:<15}|", end="")
                            else:
                                if len(event['place']) > 15:
                                    print(f"{(event['place'][:12]+ '...'):<15}|", end="")
                                else:
                                    print(f"{event['place']:<15}|", end="") 
                        else:
                            print(f"{' ':<15}|", end="")
                    else:
                        print(f"{' ':<15}|", end="")
            print()
        print('-'* 135)


#Scheduling events outside work hours
def get_events_before_9am(events):
    days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    filtered_events = { "Mon": [],"Tue": [],"Wed": [],"Thu": [],"Fri": [],"Sat": [],"Sun": [],}
    for day in days_of_week:
        filtered_day_events = []
        for event in events[day]:
            start_time = event['start_at']
            start_hour = int(start_time.split(':')[0])
            am_pm = start_time.split()[-1]
            if am_pm == 'AM' or  am_pm == 'am':
                if start_hour < 9:
                    filtered_day_events.append(event)
        if filtered_day_events:
            filtered_events[day] = filtered_day_events
    return filtered_events

def get_event_between_9am_5pm(events):
    days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    filtered_events = { "Mon": [],"Tue": [],"Wed": [],"Thu": [],"Fri": [],"Sat": [],"Sun": [],}
    for day in days_of_week:
        filtered_day_events = []
        for event in events[day]:
            start_time = event['start_at']
            start_hour = int(start_time.split(':')[0])
            am_pm = start_time.split()[-1]
            if am_pm == 'AM' or  am_pm == 'am':
                if start_hour >= 9:
                    filtered_day_events.append(event)
            else:
                if start_hour < 5:
                    filtered_day_events.append(event)
        if filtered_day_events:
            filtered_events[day] = filtered_day_events
    return filtered_events


def get_event_after_5pm(events):
    days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    filtered_events = { "Mon": [],"Tue": [],"Wed": [],"Thu": [],"Fri": [],"Sat": [],"Sun": [],}
    for day in days_of_week:
        filtered_day_events = []
        for event in events[day]:
            start_time = event['start_at']
            start_hour = int(start_time.split(':')[0])
            am_pm = start_time.split()[-1]
            if am_pm == 'PM' or  am_pm == 'pm':
                if start_hour != 12:
                    start_hour = start_hour + 12
                    if start_hour >= 17:
                        filtered_day_events.append(event)
        if filtered_day_events:
            filtered_events[day] = filtered_day_events
    return filtered_events

def get_time_slots_before_9am(events):
    time_slots = []
    hours = []
    days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for day in days_of_week:
        for event in events[day]:
            start_hour = int(event['start_at'].split(':')[0])
            if start_hour not in hours:
                hours.append(start_hour)
    sorted_hours =  sorted(hours)
    for time in sorted_hours:
        start_hour = time
        end_hour = time + 1
        time_slot = "0"+ str(start_hour) +":00 AM - " +"0"+ str(end_hour)+ ":00 AM"
        time_slots.append(time_slot)
    return time_slots

def get_time_slots_after_5pm(events):
    time_slots = []
    hours = []
    days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for day in days_of_week:
        for event in events[day]:
            start_hour = int(event['start_at'].split(':')[0])
            if start_hour not in hours:
                hours.append(start_hour)
            end_hour = int(event['end_at'].split(':')[0])
            if end_hour not in hours:
                    hours.append(end_hour)
    sorted_hours =  sorted(hours)
    for time in sorted_hours:
        start_hour = time
        end_hour = 0
        if time == 12:
            end_hour = time
        else:
            end_hour = time + 1

        if len(str(start_hour)) == 1:
            time_slot = "0"+ str(start_hour) +":00 PM - " +"0"+ str(end_hour)+ ":00 PM"
            time_slots.append(time_slot)
        else:
            if end_hour == 12:
                time_slot = str(start_hour) +":00 PM - " + str(end_hour)+ ":00 AM"
                time_slots.append(time_slot)
            else:
                time_slot = str(start_hour) +":00 PM - " + str(end_hour)+ ":00 PM"
                time_slots.append(time_slot)
    return time_slots


# displaying an event on a specific day
def display_event_on_specific_day(events):
    sort_events_by_start_time(events)
    day_to_display = input("Enter the day to display events (e.g., Mon, Tue, Wed, Thu, Fri, Sat, Sun): ")
    
    if day_to_display in events:
        print(f"Events on {day_to_display}:")
        events_on_day = events[day_to_display]
        
        if not events_on_day:
            print("No events scheduled for this day.")
        else:
            for event in events_on_day:
                print(f"Event Name: {event['name']}")
                print(f"Start Time: {event['start_at']}")
                print(f"End Time: {event['end_at']}")
                print(f"Location: {event['place']}")
                print('-' * 30)
    else:
        print(f"No events found for {day_to_display}.")


# saving the time table to file
def save_time_table_to_file(events):
    sort_events_by_start_time(events)
    file_name = input("Enter the name of the file to save the time table: ")

    first_day = input("What should be the first day of the week (Mon / Sun)?")
    # Define the days of the week
    days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    if first_day == 'Mon':
      days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    elif first_day == 'Sun':
      days_of_week = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]    

    try:
        with open(file_name, "w") as file:
            file.write(f"{'Time Slot':<20}|")

            for day in days_of_week:
                file.write(f"{day:<15}|")

            file.write("\n")
            file.write('-' * 135 + "\n")

            before_events = get_events_before_9am(events)
            after_events = get_event_after_5pm(events)
            now_events = get_event_between_9am_5pm(events)
            before_time = get_time_slots_before_9am(before_events)
            after_time = get_time_slots_after_5pm(after_events)

            time_slots = [
                "09:00 AM - 10:00 AM",
                "10:00 AM - 11:00 AM",
                "11:00 AM - 12:00 PM",
                "12:00 PM - 01:00 PM",
                "01:00 PM - 02:00 PM",
                "02:00 PM - 03:00 PM",
                "03:00 PM - 04:00 PM",
                "04:00 PM - 05:00 PM",
            ]
            for before_slot in before_time:
                file.write(f"{before_slot:<20}|")
                for x in range(2):
                    if x == 1:
                        file.write(f"{' ':<20}|") 
                    for day in days_of_week:
                        events_on_day = before_events[day]
                        if len(events_on_day) == 0:
                            file.write(f"{' ':<15}|")
                        for event in events_on_day:
                            if event['end_at'] > before_slot:
                                if event['start_at'] <= before_slot:
                                    if x == 0:
                                        if len(event['name']) > 15:
                                            file.write(f"{(event['name'][:12]+ '...'):<15}|")
                                        else:
                                            file.write(f"{event['name']:<15}|") 
                                    else:
                                        if len(event['place']) > 15:
                                            file.write(f"{(event['place'][:12]+ '...'):<15}|")
                                        else:
                                            file.write(f"{event['place']:<15}|") 

                                else:
                                    file.write(f"{' ':<15}|")
                            else:
                                file.write(f"{' ':<15}|")
                    file.write("\n")
                file.write('-'* 135+ "\n")

            for slot in time_slots:
                file.write(f"{slot:<20}|")
                for x in range(2):
                    if x == 1:
                        file.write(f"{' ':<20}|") 
                    for day in days_of_week:
                        events_on_day = now_events[day]
                        if len(events_on_day) == 0:
                            file.write(f"{' ':<15}|")
                        for event in events_on_day:
                            if event['end_at'] > slot:
                                if event['start_at'] <= slot:
                                    if x == 0:
                                        if len(event['name']) > 15:
                                            file.write(f"{(event['name'][:12]+ '...'):<15}|")
                                        else:
                                            file.write(f"{event['name']:<15}|") 
                                    else:
                                        if len(event['place']) > 15:
                                            file.write(f"{(event['place'][:12]+ '...'):<15}|")
                                        else:
                                            file.write(f"{event['place']:<15}|") 
                                else:
                                    file.write(f"{' ':<15}|")
                            else:
                                file.write(f"{' ':<15}|")
                    file.write("\n")
                file.write('-' * 135 + "\n")
            
            for after_slot in after_time:
                file.write(f"{after_slot:<20}|")
                for x in range(2):
                    if x == 1:
                        file.write(f"{' ':<20}|") 
                    for day in days_of_week:
                        events_on_day = after_events[day]
                        if len(events_on_day) == 0:
                            file.write(f"{' ':<15}|")
                        for event in events_on_day:
                            if event['end_at'] > after_slot:
                                if event['start_at'] <= after_slot:
                                    if x == 0:
                                        if len(event['name']) > 15:
                                            file.write(f"{(event['name'][:12]+ '...'):<15}|")
                                        else:
                                            file.write(f"{event['name']:<15}|") 
                                    else:
                                        if len(event['place']) > 15:
                                            file.write(f"{(event['place'][:12]+ '...'):<15}|")
                                        else:
                                            file.write(f"{event['place']:<15}|")
                                else:
                                    file.write(f"{' ':<15}|")
                            else:
                                file.write(f"{' ':<15}|")
                    file.write("\n")
                file.write('-' * 135 + "\n")

        print(f"Time table has been saved to '{file_name}'.")
    except Exception as e:
        print(f"An error occurred while saving the time table: {e}")

# printing error messages for invalid inputs
def invalid_user_input():
    print('invalid_user_input')

def validate_day(day):
    valid_days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    return day in valid_days

def validate_time(time_str):
    # Validate the time format "hh:mm AM/PM"
    if len(time_str) != 8:
        return False

    try:
        # Split the time string into hours, minutes, and AM/PM parts
        hours, minutes, am_pm = time_str.split()[0].split(':') + [time_str.split()[1]]

        hours = int(hours)
        minutes = int(minutes)

        # Check the validity of each part
        if not (1 <= hours <= 12):
            return False
        if not (0 <= minutes <= 59):
            return False
        if am_pm not in ['AM', 'PM']:
            return False

        return True

    except ValueError:
        return False

def is_time_overlap(existing_start_time, existing_end_time, new_start_time, new_end_time):
    # Compare times by converting them into minutes
    existing_start_minutes = time_to_minutes(existing_start_time)
    existing_end_minutes = time_to_minutes(existing_end_time)
    new_start_minutes = time_to_minutes(new_start_time)
    new_end_minutes = time_to_minutes(new_end_time)

    # Check for time overlap
    return (new_start_minutes < existing_end_minutes) and (new_end_minutes > existing_start_minutes)

def time_to_minutes(time_str):
    # Convert time in "hh:mm AM/PM" format to minutes since midnight
    hours, minutes, am_pm = time_str.split()[0].split(':') + [time_str.split()[1]]
    hours = int(hours)
    minutes = int(minutes)

    if am_pm == 'PM':
        hours += 12  # Add 12 hours for PM

    return hours * 60 + minutes

main()
