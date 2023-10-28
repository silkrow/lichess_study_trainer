from trainer import Trainer

# Example usage:
study = Trainer()  # Initialize without a token
# Authenticate later using a personal access token
with open("lichess_token.txt", "r") as file:
    token = file.read()
    study.set_personal_token(token)

# Ask the user for inputs interactively
valid_username = input("Enter a valid Lichess username: ")
study_list_result = study.fetch_studies(valid_username)
print(study_list_result)

valid_study_id = input("Enter a valid study ID: ")
info_parts, pgn_moves = study.get_study_pgn(valid_study_id)

print("Information Parts:")
print(info_parts)
print("\nPGN Moves:")
print(pgn_moves)

# Analyze and display the board for the first game in the study
if pgn_moves:
    board = study.display_lines(pgn_moves[0])
