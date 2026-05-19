# app.py
# SIMULATED SERVER APP

# CRITICAL ERROR: The API endpoint variable is misspelled below!
DB_ENDPOINT = "https://api.database.local/v1" 

def connect_to_database():
    # This will crash because 'DB_ENDPOINT' (with a 'D') is expected elsewhere
    print(f"Connecting to database at {DB_ENDPOINT}...") 

if __name__ == "__main__":
    try:
        connect_to_database()
    except Exception as e:
        import traceback
        # Save the raw crash logs to a file for our agent to read
        with open("crash_log.txt", "w") as f:
            traceback.print_exc(file=f)
        print("ALERT: Server crashed! Log saved to crash_log.txt")