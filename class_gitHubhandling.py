import os
from git import Repo

class class_gitHubUpload():

    # Set your GitHub username and repository name
    USERNAME = "aaronshi2017"
    REPO_NAME = "https://github.com/aaronshi2017/TM500_Automation_New"
    # Set the directory where your files are located
    FILES_DIR = "/home/rantechdev/TM500_Automation/TM500Automation"
    # Set the branch name
    BRANCH_NAME = "newbranch"
    #Set your commit message
    COMMIT_MESSAGE = "5-17-test"

    def __init__(self,project):
        self.COMMIT_MESSAGE=project

    def github_upload(self):

        # Initialize the repository object
        repo = Repo.init(self.FILES_DIR)

        # Add all files to the repository
        repo.index.add("*")

        # Commit changes
        repo.index.commit(self.COMMIT_MESSAGE)

        # Get the origin remote
        origin = repo.create_remote("origin", url=f"git@github.com:{self.USERNAME}/{self.REPO_NAME}.git")

        # Push changes to the remote repository
        origin.push(refspec=f"HEAD:{self.BRANCH_NAME}")

        print("Files uploaded successfully!")
    
if __name__ == "__main__":
    github=class_gitHubUpload("Project_Test")
    github.github_upload()

