from github import Github
import os

# Replace with your GitHub personal access token and repository details
GITHUB_TOKEN = 'your_github_token'
REPO_NAME = 'your_github_username/your_repo_name'

def upload_file_to_github(token, repo_name, file_path, commit_message):
    g = Github(token)
    repo = g.get_repo(repo_name)

    with open(file_path, 'r') as file:
        content = file.read()

    try:
        # Check if the file already exists in the repository
        contents = repo.get_contents(file_path)
        repo.update_file(contents.path, commit_message, content, contents.sha)
        print(f"File '{file_path}' updated successfully in GitHub repository '{repo_name}'.")
    except:
        repo.create_file(file_path, commit_message, content)
        print(f"File '{file_path}' created successfully in GitHub repository '{repo_name}'.")

if __name__ == "__main__":
    file_path = 'test_example.py'
    commit_message = 'Add auto-generated pytest file'

    # Generate the pytest file
    os.system('python3 generate_pytest.py')

    # Upload the pytest file to GitHub
    upload_file_to_github(GITHUB_TOKEN, REPO_NAME, file_path, commit_message)
