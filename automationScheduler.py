import time
import datetime
import automation
from apscheduler.schedulers.background import BackgroundScheduler
import bootstrap

bootstrap.main()
def test_scheduler():
    print "Runing"

test_scheduler()
scheduler = BackgroundScheduler()

scheduler.start()

scheduler.add_job(automation.main, 'cron', day_of_week='mon-fri', hour=15, minute=30, timezone='US/Eastern') 
scheduler.add_job(automation.main, 'cron', day_of_week='sat-sun', hour=12, minute=30, timezone='US/Eastern') 

try:
    while True:
        time.sleep(2)
except (KeyboardInterrupt, SystemExit):
    # Not strictly necessary if daemonic mode is enabled but should be done if possible
    scheduler.shutdown()
