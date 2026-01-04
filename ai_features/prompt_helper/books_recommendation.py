from ai_features.schemas import UserPreferenceBook, RecommendedBooks

class RecommendedPromptHelper:
    """
    Helper class to provide prompt for book recommendation.
    """

    def get_system_prompt(self):
        """
        This function provides a system prompt for model. Which describe the role and rules to the model.
        For book recommendation
        """
        return  {
                    "role": "system",
                    "content": (
                        "You are a book recommendation engine.\n"
                        "Your task is to recommend books based on a user's past reviews.\n\n"
                        "Rules:\n"
                        "- Infer the user's reading preferences from their reviews.\n"
                        "- Recommend ONLY from the provided list of available books.\n"
                        "- Use ONLY the provided available_books data as your knowledge source; do NOT infer, invent, or reference any books outside this data.\n"
                        "- Do NOT recommend books the user has already read.\n"
                        "- Do NOT add explanations, introductions, or extra text.\n"
                        "- Output must be concise and reader-friendly.\n"
                        "- Limit recommendations to the most relevant books.\n"
                        "- Follow the exact output format specified by the user."
                    )
                    }

    
    def get_user_prompt(self, user_review_books, available_books):
        """
        Generate a prompt for the AI model based on user reviews.

        The prompt helps the model suggest books from available options 
        based on the user's reviews of other books.
        """

        return {
                "role": f"""user,
                content: (
                    User Reviews (books already read, including title, genre, and review):\n
                    {user_review_books}\n\n
                    Available Books (candidates for recommendation):\n
                    {available_books}\n\n
                    Task:\n
                    - Infer the user's reading preferences from their reviews.\n
                    - Select the best matching books from the available list.\n\n
                    Output Format:\n
                    - Book Title: One concise reason for recommendation (mention genre or key theme)\n\n
                    Constraints:\n
                    - Return ONLY bullet points.\n
                    - Do NOT include explanations, headings, or extra text.\n
                    - Do NOT repeat books the user has already read.
                )"""
        }

    
    def get_prompt_message(self, user_review_books: UserPreferenceBook, available_books: RecommendedBooks):
        """
        Get system and user prompt and return to the service as message.
        """

        system_prompt = self.get_system_prompt()
        user_prompt = self.get_user_prompt(user_review_books, available_books)
        return [system_prompt, user_prompt]