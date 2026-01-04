from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field


# --- Define Input Schema ---
# class EmailRequest(BaseModel):
#     recipient: str = Field(
#         description="The name or role of the email recipient (e.g., 'Project Manager', 'Client')."
#     )
#     purpose: str = Field(
#         description="The main purpose of the email (e.g., 'requesting information', 'scheduling a meeting')."
#     )
#     tone: str = Field(
#         description="The desired tone of the email (e.g., 'formal', 'friendly', 'urgent')."
#     )


# --- Define Output Schema ---
class EmailContent(BaseModel):
    subject: str = Field(
        description="The subject line of the email. Should be concise and descriptive."
    )
    body: str = Field(
        description="The main content of the email. Should be well-formatted with proper greeting, paragraphs, and signature."
    )


# --- Create Email Generator Agent ---
root_agent = LlmAgent(
    name="email_agent",
    model="gemini-2.0-flash",
    description="Generates professional emails with structured subject and body",
    instruction="""
        You are an Email Generation Assistant.
        Your task is to generate a professional email based on the user's request.

        GUIDELINES:
        - Create an appropriate subject line (concise and relevant)
        - Write a well-structured email body with:
            * Professional greeting
            * Clear and concise main content
            * Appropriate closing
            * Your name as signature
        - Suggest relevant attachments if applicable (empty list if none needed)
        - Email tone should match the purpose (formal for business, friendly for colleagues)
        - Keep emails concise but complete

        IMPORTANT: Your response MUST be valid JSON matching this structure:
        {
            "subject": "Subject line here",
            "body": "Email body here with proper paragraphs and formatting",
        }

        DO NOT include any explanations or additional text outside the JSON response.
    """,
    # input_schema=EmailRequest,
    output_schema=EmailContent,
    output_key="email",
)
