import requests

class Study:
    def __init__(self, personal_token=None):
        self.base_url = "https://lichess.org/api/"
        self.headers = {
            "Accept": "application/json",
        }
        if personal_token:
            self.set_personal_token(personal_token)

    def set_personal_token(self, personal_token):
        self.headers["Authorization"] = f"Bearer {personal_token}"

    def list_studies(self, username):
        studies_url = f"{self.base_url}study/by/{username}"
        response = requests.get(studies_url, headers=self.headers)

        if response.status_code == 200:
            print(response.text)  # Print the response content
        else:
            print(f"Failed to list studies. Status Code: {response.status_code}")

    def get_study_pgn(self, study_id):
        study_url = f"{self.base_url}study/{study_id}.pgn"
        response = requests.get(study_url, headers=self.headers)

        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to retrieve PGN for study {study_id}. Status Code: {response.status_code}")
            return None

# Example usage:
study = Study()  # Initialize without a token
# Authenticate later using a personal access token
personal_token = "lip_EOEhmhXG2MsPWuBiDFI7"
study.set_personal_token(personal_token)

valid_username = "failedtofindaname"
study.list_studies(valid_username)

valid_study_id = "OS94SFrY"
pgn = study.get_study_pgn(valid_study_id)
print(pgn)
