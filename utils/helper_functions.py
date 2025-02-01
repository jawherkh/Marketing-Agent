import logging
from agents import generate_summary, generate_email
import requests
from bs4 import BeautifulSoup
import json

def scrape_website(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        text = ""
        for paragraph in soup.find_all("p"):
            text += paragraph.get_text() + "\n"

        logging.info(f"Scraped website content from {url} successfully.")
        return text

    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching URL: {e}")
        return None

def scrape_and_summarize(companies):
    summaries = []

    for company in companies:
        company_name = company["company_name"]
        url = company["url"]
        text = scrape_website(url)

        if text:
            res = generate_summary(text)
            if res:
                summaries.append({
                    "company_name": company_name,
                    "summary": res
                })
            else:
                logging.error(f"Failed to generate summary for {company_name}")

    return summaries

def scrape_apollo(title, tech_company_urls):
    person_titles = title
    scraped_content = []
    for company_website in tech_company_urls:
        url = f"https://api.apollo.io/api/v1/mixed_people/search?person_titles[]={person_titles}&q_organization_domains={company_website}&page=1&per_page=10"

        headers = {
            "accept": "application/json",
            "Cache-Control": "no-cache",
            "Content-Type": "application/json",
            "x-api-key": "Apollo-API-Here"
        }

        try:
            response = requests.post(url, headers=headers)
            response.raise_for_status()
            scraped_content.append(response.text)
            logging.info(f"Scraped content from Apollo for {company_website} successfully.")
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching data from Apollo for {company_website}: {e}")

    return scraped_content

def extract_contact_info(data_list):
    contacts = []

    for data in data_list:
        try:
            parsed_data = json.loads(data)
            people = parsed_data.get("people", [])

            for person in people:
                current_company = None
                for job in person.get("employment_history", []):
                    if job.get("current"):
                        current_company = job.get("organization_name")
                        break

                contact_info = {
                    "name": person.get("name"),
                    "email": person.get("email"),
                    "linkedin_url": person.get("linkedin_url"),
                    "company_name": current_company
                }
                contacts.append(contact_info)
            logging.info("Contact information extracted successfully.")
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON data: {e}")

    return contacts

def generate_personalized_email(contact_info, company_descriptions):
    personalized_emails = []

    company_description_map = {company['company_name']: company['summary'] for company in company_descriptions}

    for manager in contact_info:
        manager_name = manager['name']
        company_name = manager['company_name']
        manager_email = manager['email']
        linkedin_url = manager['linkedin_url']

        company_description = company_description_map.get(company_name, "No description available")

        res = generate_email(manager_name, company_name, company_description, manager_email, linkedin_url)
        if res:
            personalized_emails.append({
                "name": manager_name,
                "email": manager_email,
                "company_name": company_name,
                "linkedin_url": linkedin_url,
                "personalized_email": res
            })
            logging.info(f"Personalized email generated for {manager_name} at {company_name}.")
        else:
            logging.error(f"Failed to generate email for {manager_name} at {company_name}.")

    return personalized_emails