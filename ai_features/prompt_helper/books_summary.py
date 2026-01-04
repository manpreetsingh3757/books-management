from books.models import Book

class PromptHelper:
    """
    Helper class to provide prompt for book summary.
    """


    def get_system_prompt(self):
        """"
        Create a system prompt for book summary.
        """

        return  {
                    "role": "system",
                    "content": (
                        "You are an AI assistant that generates concise, neutral book summaries "
                        "for readers. "
                        "Your task is to summarize what the book is about and reflect overall "
                        "reader sentiment based on reviews and ratings.\n\n"
                        "Rules:\n"
                        "- Return ONLY the summary text.\n"
                        "- Do NOT include headings, bullet points, or explanations.\n"
                        "- Do NOT mention that you are an AI.\n"
                        "- Do NOT repeat ratings numerically unless relevant.\n"
                        "- Keep the tone informative and balanced.\n"
                        "- Limit the output to 3–4 sentences.\n"
                        "- If there are no reviews, summarize based only on book details."

                    )
                }
    
    def get_user_prompt(self, book: Book, formatted_reviews: str, average_rating, total_reviews):
        """"
        Create a prompt for generating a book summary.
        Includes the book's title, author, genre, publish year, average rating,
        total reviews, and formatted user reviews.
        """

        return {
            "role": "user",
            "content": f"""
                    Book Information:
                    Title: {book.title}
                    Author: {book.author}
                    Genre: {book.genre}
                    Year Published: {book.year_published}

                    Aggregated Rating:
                    Average Rating: {average_rating}
                    Total Reviews: {total_reviews}

                    User Reviews:
                    {formatted_reviews}

                    Generate a short summary that helps a reader understand what this book is about
                    and whether it is generally considered worth reading.
                    """
        }
    
    def get_prompt_message(self, book: Book, formatted_reviews: str, average_rating, total_reviews):
        """
        Get system and user prompt and return to the service as message.
        """

        system_prompt = self.get_system_prompt()
        user_prompt = self.get_user_prompt(book, formatted_reviews, average_rating, total_reviews)
        return [system_prompt, user_prompt]