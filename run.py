import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('ecommerce_feedback_analyser')


class ECommerceAnalyser:
    """
    This class handles the shopping feedback system.
    It sets the rules and connects to the Google sheet.
    """

    def __init__(self):
        self.valid_categories = [
            "Product Search",
            "Checkout",
            "Customer Support",
            "Returns"
        ]
        self.worksheet = SHEET.worksheet("feedback")
        print("Successfully connected to the Google Sheets database!\n")

    def get_user_feedback(self):
        """
        Asks the user to type in their shopping feedback answers
        """
        print("--- Please Provide Your Feedback ---")
        print(f"Available Categories to review: {self.valid_categories}\n")

        category = input("Enter experience category: ").strip()
        ease = input("Rate the ease of use (1-5): ").strip()
        delivery = input("Rate the delivery experience (1-5): ").strip()
        recommend = input("Would you recommend us? (Yes/No): ").strip()

        return {
            "Category": category,
            "Ease": ease,
            "Delivery": delivery,
            "Recommend": recommend
        }


def run_survey_app():
    """
    The starting point that runs the program in the terminal.
    """

    print("========================================\n")
    print(" Online Shopping Feedback Analyser \n")
    print("========================================\n")

    analyser = ECommerceAnalyser()

    user_data = analyser.get_user_feedback()

    print("\n--- Thank you for your feedback! ---")
    print(f"Data received: {user_data}")


if __name__ == "__main__":
    run_survey_app()
