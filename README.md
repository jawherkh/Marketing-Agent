# Marketing Agent

## Overview
This project is a marketing agent that scrapes the contact information of marketing managers from various tech company websites, summarizes the content of these websites, and generates personalized emails for the marketing managers. (PS: You can change the title of the managers, not just marketing)

## Project Structure
- `main.py`: The main script that orchestrates the entire process.
- `utils/db.py`: Contains functions to create the database and save contact information and emails.
- `utils/helper_functions.py`: Contains helper functions for web scraping, summarizing content, and generating personalized emails.
- `utils/agents.py`: Contains functions to generate summaries and emails using an AI model.
- `Dockerfile`: Docker file to containerize the application, making it easier to deploy and run in different environments.

## Setup
1. **Clone the repository:**
    ```sh
    git clone https://github.com/jawherkh/Marketing-Agent.git
    cd Marketing-Agent
    ```

2. **Install dependencies:**
    Ensure you have Python installed. Then, install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

3. **Set up Apollo API Key:**
    Replace `"Apollo-API-Here"` in [helper_functions.py](http://_vscodecontentref_/0) with your actual Apollo API key.

4. **Set up Groq API Key:**
    Export your Groq API key as an environment variable:
    ```sh
    export GROQ_API_KEY="your_groq_api_key"
    ```

## Running the Project
1. **Run the main script:**
    ```sh
    python main.py
    ```

## Explanation of [main.py](http://_vscodecontentref_/1)
- **Imports:**
    ```python
    from utils.helper_functions import *
    from utils.db import *
    import sqlite3
    ```

- **Database Functions:**
    - `create_database()`: Creates the database and tables if they do not exist.
    - `save_contact_info(contact)`: Saves contact information to the database.
    - `save_emails(emails)`: Saves generated emails to the database.

- **Main Function:**
    ```python
    def main():
        try:
            create_database()

            person_title = "Marketing Manager"
            tech_company_urls = [
                "figma.com", "notion.so", "linear.app", "vercel.com",
                "sentry.io", "datadog.com", "twilio.com", "plaid.com",
                "superhuman.com", "buttercms.com",
            ]

            scraped_content = scrape_apollo(person_title, tech_company_urls)
            contact = extract_contact_info(scraped_content)
            save_contact_info(contact)

            summarized_texts = scrape_and_summarize(tech_company_urls)
            emails = generate_personalized_email(contact, summarized_texts)
            save_emails(emails)
        except Exception as e:
            print(f"An error occurred: {e}")
    ```


## Error Handling
- The code includes error handling for database operations and web scraping to ensure the program continues running even if an error occurs.

## Notes
- Please ensure you have a stable internet connection as the script involves web scraping and API calls.
- The database `marketing_agent.db` will be created in the same directory as the script if it does not exist.
