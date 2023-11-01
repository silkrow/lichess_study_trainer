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

print(f"{valid_username} has following studies: ")
for i in range(len(names)):
    print(f"{i+1:3}: {names[i]}")

number = input("Please input the index of the study you want to train on: ")

trainer.set_crnt_study(names[int(number) - 1])

trainer.training()