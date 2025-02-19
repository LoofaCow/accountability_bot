from flask import Flask, render_template
from apscheduler.schedulers.background import BackgroundScheduler
import datetime

app = Flask(__name__)

# Function to simulate sending a daily check-in
def send_daily_checkin():
    # For now, just print a check-in message
    print(f"Check-in at {datetime.datetime.now()}: Remember to review your tasks!")

# Set up the scheduler to run every day at 9:00 AM and 5:00 PM
scheduler = BackgroundScheduler()
scheduler.add_job(send_daily_checkin, 'cron', hour='9,17')
scheduler.start()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
