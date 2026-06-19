"""
Scheduled Tasks
"""
import schedule
import time
from scraper.futures_scraper import FuturesScraper
from notification.email_service import email_service
from datetime import datetime
import os


def update_daily_data():
    """Task to update daily trade data"""
    print(f"\n{'=' * 60}")
    print(f"Starting daily data update at {datetime.now()}")
    print(f"{'=' * 60}\n")

    try:
        scraper = FuturesScraper()
        results = scraper.fetch_all_main_contracts_daily()

        print(f"\nUpdate completed. Total contracts updated: {len(results)}")

        # Send email notification if configured
        recipients = os.getenv('NOTIFICATION_EMAILS', '').split(',')
        if recipients and recipients[0]:
            email_service.send_daily_report(results, recipients)

    except Exception as e:
        print(f"Error in daily update: {e}")


def run_scheduler():
    """Run the scheduler"""
    schedule.every().day.at("16:00").do(update_daily_data)

    print("Scheduler started. Waiting for 16:00 to update data...")
    print("Press Ctrl+C to stop\n")

    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    run_scheduler()
