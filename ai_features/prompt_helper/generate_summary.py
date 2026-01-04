
class GenerateSummaryPromptHelper:
    """
    Helper class to provide prompt for generate book summary.
    """
            
    def get_system_prompt(self):
        """"
        Create a system prompt for generating book summary.
        """
        
        return  {
            "role": "system",
            "content": (
                "You are an AI assistant that generates concise book summaries based on the provided content.\n"
                "Rules:\n"
                "- Summarize the book using only the provided content.\n"
                "- Return ONLY the summary text.\n"
                "- Do NOT include headings, bullet points, or explanations.\n"
                "- Do NOT mention that you are an AI.\n"
                "- Keep the tone informative, neutral, and balanced.\n"
                "- Limit the summary to 3–4 sentences."
            )
            }

    
    def get_user_prompt(self, content: str):
        """
        Generate a prompt for the AI model to create a summary based on the given content.
        """
        return {
            "role": "user",
            "content": f"""
            Book Content:
            {content}

            Task:
            Generate a clear and concise summary that helps a reader understand what this book is about. 
            Keep the summary informative, neutral, and limited to 3–4 sentences. Return only the summary text without headings, bullet points, or extra explanations.
            """
        }

    
    def get_prompt_message(self, content: str):
        """
        Get system and user prompt and return to the service as message.
        """
        
        system_prompt = self.get_system_prompt()
        user_prompt = self.get_user_prompt(content)
        return [system_prompt, user_prompt]