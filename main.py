from trainer import Trainer

# Example usage:
trainer = Trainer()  # Initialize without a token
# Authenticate later using a personal access token
with open("lichess_token.txt", "r") as file:
    token = file.read()
    trainer.set_personal_token(token)

# Ask the user for inputs interactively
valid_username = input("Enter a valid Lichess username: ")
study_list_result = trainer.fetch_studies(valid_username)
print(study_list_result)

names = trainer.list_study_names()
print(names)

# trainer.set_crnt_study("[Repertoire] Accelerated Dragon")
trainer.set_crnt_study("[Repertoire] Sicilian Sidelines")

# board = trainer.get_position()
# i = 0
# while board:
#     i += 1
#     print(i)
#     print(board)
#     board = trainer.get_position()

trainer.training()