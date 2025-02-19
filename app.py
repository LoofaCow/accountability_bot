import streamlit as st
from apscheduler.schedulers.background import BackgroundScheduler
import datetime

# Function to simulate sending a daily check-in
def send_daily_checkin():
    # For now, just print a check-in message to your console (hello, nostalgia!)
    print(f"Check-in at {datetime.datetime.now()}: Remember to review your tasks!")

# Initialize the scheduler only once using st.session_state
if "scheduler" not in st.session_state:
    scheduler = BackgroundScheduler()
    # Schedule the job to run every day at 9:00 AM and 5:00 PM
    scheduler.add_job(send_daily_checkin, 'cron', hour='9,17')
    scheduler.start()
    st.session_state["scheduler"] = scheduler

# Main UI of your Streamlit app
st.title("Daily Check-In App")
st.write("Welcome! The daily check-in scheduler is running in the background.")
st.write("Check your console for the check-in messages at 9:00 AM and 5:00 PM!")
