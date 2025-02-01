from utils.helper_functions import *
from utils.db import *
from utils.agents import * 
import sqlite3
import logging



logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    try:
        create_database()

        # we want to get 10 marketing managers from the websites lists that we have.
        person_title = "Marketing Manager"

        tech_company_urls = [
            "figma.com",
            "notion.so",
            "linear.app",
            "vercel.com",
            "sentry.io",
            "datadog.com",
            "twilio.com",
            "plaid.com",
            "superhuman.com",
            "buttercms.com",
        ]

        # running the scraping loop to get marketing managers of the list of 50 marketing managers of the companies above using Apollo API  
        scraped_content = scrape_apollo(person_title, tech_company_urls)
        logging.info("Scraped content successfully.")

        # this function will extract the names and linkedin profiles of managers
        contact = extract_contact_info(scraped_content)
        save_contact_info(contact)
        logging.info("Contact information extracted and saved successfully.")

        # running the summary agent to summarize the content of the websites
        summarized_texts = scrape_and_summarize(tech_company_urls)
        logging.info("Content summarized successfully.")

        # running the summary agent to summarize the content of the websites    
        emails = generate_personalized_email(contact, summarized_texts)
        save_emails(emails)
        logging.info("Personalized emails generated and saved successfully.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()