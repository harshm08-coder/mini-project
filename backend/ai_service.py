import os
from dotenv import load_dotenv
from openai import OpenAI  # still using the OpenAI-compatible client

load_dotenv()

# Initialize the client with GROQ API key and base URL
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"  # Groq endpoint
)

def analyze_resume(resume_text: str):
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",  # use a Groq-supported model
        messages=[
            {"role": "system", "content": "You are a professional HR recruiter."},
            {"role": "user", "content": f"""
Analyze the resume and provide:
1. Strengths
2. Weaknesses
3. Missing technical skills
4. Suggestions for improvement

Resume:
{resume_text}
"""}
        ]
    )

    # Access the message content in the same way
    return response.choices[0].message.content

# Example usage
if __name__ == "__main__":
    sample_resume = """
John Doe
Software Engineer with 3 years of experience in Python and React.
"""
    print(analyze_resume(sample_resume))