import logging

def generate_summary(text, client):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a highly capable summarization AI. Your primary function is to provide concise and objective summaries of given text",
                },
                {
                    "role": "user",
                    "content": f"""
You are a highly capable summarization AI. Your primary function is to provide concise and objective summaries of given text.

Key Guidelines:
Conciseness: Keep summaries as brief as possible while maintaining essential information.
Objectivity: Avoid injecting personal opinions, biases, or interpretations. Present information factually.
Clarity: Ensure the summary is easy to understand and free from jargon or ambiguity.
Focus on Key Takeaways: Highlight the most important points and avoid unnecessary details.
Example:
Input: "This company offers a cloud-based platform for businesses to manage their customer relationships. Key features include contact management, sales force automation, marketing automation, and customer service tools. The platform is designed to help businesses increase sales, improve customer satisfaction, and streamline their operations."
Output: "This company provides a cloud-based CRM platform with features like contact management, sales automation, and marketing tools to help businesses improve sales and customer relationships."
Now, please provide a concise and objective summary of the following text: {text}""",
                }
            ],
            model="llama-3.3-70b-versatile",
        )
        logging.info("Summary generated successfully.")
        return chat_completion.choices[0].message.content
    except Exception as e:
        logging.error(f"Error generating summary: {e}")
        return None

def generate_email(manager_name, company_name, company_description, manager_email, linkedin_url, client):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a highly capable AI specializing in crafting personalized and professional emails.",
                },
                {
                    "role": "user",
                    "content": f"""
 Write a personalized email for {manager_name}, the Marketing Manager at {company_name}.
            Include relevant company information based on the following description:
            {company_description}
            Make the email respectful, engaging, and concise.
            Mention their role and how their company stands out. End with a call to action to start a conversation.
            The email should feel warm and professional, expressing genuine interest in their work and company.

            Here's the manager's contact information:
            - Name: {manager_name}
            - Company: {company_name}
            - Email: {manager_email}
            - LinkedIn: {linkedin_url}
            """,
                }
            ],
            model="llama-3.3-70b-versatile",
        )
        logging.info("Email generated successfully.")
        return chat_completion.choices[0].message.content
    except Exception as e:
        logging.error(f"Error generating email: {e}")
        return None