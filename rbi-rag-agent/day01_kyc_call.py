import anthropic
import os 
from dotenv import load_dotenv
load_dotenv()
client=anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are a KYC (Know Your Customer) compliance analyst at an RBI-regulated Indian bank. Your responsibilities: - Assess customer risk tier (Low / Medium / High) per RBI Master Direction on KYC (2016, updated 2023) - Cite the specific RBI guideline for every decision - Never approve customers without complete documentation - Flag any PEP (Politically Exposed Person) indicators Output format: Always respond in structured JSON with keys: risk_tier, rationale, rbi_reference, action_required. """

def assess_kyc_risk(customer_profile:str)->dict:
    """Send a KYC profile to Claude for risk assessment."""
    message=client.messages.create(model="claude-sonnet-4-6",max_tokens=1024,system=SYSTEM_PROMPT,messages=[ { "role": "user", "content": customer_profile } ] )
    # Extract text from the response object
    raw_text = message.content[0].text
    # Log token usage — cost control is a BFSI requirement
    print(f"Tokens used: {message.usage.input_tokens} in / " f"{message.usage.output_tokens} out")
    return raw_text


if __name__ == "__main__":
    test_profile = """ Customer: Rajesh Kumar Age: 42 Occupation: Government Officer (IAS) Annual Income: ₹18L Account Type: Savings PAN: Provided Aadhaar: Provided Source of Funds: Salary """
    result = assess_kyc_risk(test_profile)
    print(result)