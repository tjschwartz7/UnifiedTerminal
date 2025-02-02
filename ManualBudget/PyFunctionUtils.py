def select_state():
    states = [
        "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware",
        "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky",
        "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi",
        "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico",
        "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania",
        "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont",
        "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"
    ]

    print("\nSelect a state by number:")
    for i, state in enumerate(states, start=1):
        print(f"{i}. {state}")

    while True:
        try:
            choice = int(input("\nEnter the number of your chosen state: "))
            if 1 <= choice <= len(states):
                print(f"You selected: {states[choice - 1]}")
                return states[choice - 1]
            else:
                print("Invalid number. Please select a number from the list.")
        except ValueError:
            print("Invalid input. Please enter a number.")


from datetime import datetime
def date_input():
    while True:
            date_input = input("Enter the date (YYYY-MM-DD): ")
            try:
                selected_date = datetime.strptime(date_input, "%Y-%m-%d")
                print(f"You selected: {selected_date.strftime('%A, %d %B %Y')}")
                return selected_date
            except ValueError:
                print("Invalid date format. Please try again.")