import os
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

from backend.app.config import settings

class LLMClient:
    """Unified LLM provider adapter for OpenAI, Gemini, or mock/local development."""

    def __init__(self):
        self.provider = settings.LLM_PROVIDER.lower()
        self.api_key = settings.LLM_API_KEY
        self.model = settings.LLM_MODEL

    def generate(self, prompt: str) -> str:
        if not self.api_key or self.api_key == "mock-key-for-dev":
            return self._mock_response(prompt)

        if self.provider == "openai":
            try:
                import openai
                client = openai.OpenAI(api_key=self.api_key)
                response = client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.1
                )
                return response.choices[0].message.content
            except Exception as e:
                return f"Error calling OpenAI API: {str(e)}"

        elif self.provider in ["gemini", "google"]:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                model = genai.GenerativeModel(self.model)
                response = model.generate_content(prompt)
                return response.text
            except Exception as e:
                return f"Error calling Gemini API: {str(e)}"
        else:
            return self._mock_response(prompt)

    def _mock_response(self, prompt: str) -> str:
        return (
            "### 📌 Response (Dev Mode / Mock LLM Adapter)\n\n"
            "Based on your retrieved study materials, here is the explanation:\n\n"
            "• **Key Concept**: The retrieved documents provide foundational definitions for your query.\n"
            "• **Details**: All concepts were extracted page-by-page from your uploaded textbook/notes.\n\n"
            "---\n"
            "📄 **Source Citation:**\n"
            "• Document: Sample_Document.pdf | Page Number: 1"
        )

llm_client = LLMClient()
