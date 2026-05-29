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
            "Product Search", "Checkout", "Customer Support", "Returns"
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

    def validate_feedback(self, data):
        """
        Checks if user input is valid and meets the criteria.
        """

        if data["Category"] not in self.valid_categories:
            print("Invalid category!")
            print(f"Please choose from: {self.valid_categories}")
            return False

        try:
            ease_rating = int(data["Ease"])
            delivery_rating = int(data["Delivery"])
            if not (1 <= ease_rating <= 5) or not (1 <= delivery_rating <= 5):
                print("Ratings must be between 1 and 5!")
                return False
        except ValueError:
            print("Ratings must be numeric!")
            return False

        if data["Recommend"].lower() not in ["yes", "no"]:
            print("Recommend must be 'Yes' or 'No'!")
            return False

        return True

    def upload_feedback(self, data):
        """
        Converts the feedback dictionary to a list
        and uploads it to the Google sheet.
        """
        print("Uploading feedback to the database...")

        row_to_insert = [
            data["Category"],
            data["Ease"],
            data["Delivery"],
            data["Recommend"]
        ]
        self.worksheet.append_row(row_to_insert)
        print("Upload successful! Google Sheet updated.\n")


def run_survey_app():
    """
    The starting point that runs the program in the terminal.
    """

    print("========================================\n")
    print(" Online Shopping Feedback Analyser \n")
    print("========================================\n")

    analyser = ECommerceAnalyser()

    while True:
        """
        Gets user feedback and validates it.
        If valid, it breaks the loop and ends the program.
        """
        user_data = analyser.get_user_feedback()

        if analyser.validate_feedback(user_data):
            print("\n--- Input Successful! ---")
            break

        print("Please enter feedback again.\n")

    analyser.upload_feedback(user_data)

    print("\n--- Thank you for your feedback! ---")
    print(f"Data received: {user_data}")


if __name__ == "__main__":
    run_survey_app()
