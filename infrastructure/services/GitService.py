import git
import os
import datetime


class GitService:
    def __init__(self, remote_git: str, local_git: str, branch: str, logger):
        self.__remote_git = remote_git
        self.__local_git = local_git
        self.__branch = branch
        self.__logger = logger

    def clone_repo(self):
        if os.path.exists(self.__local_git):
            raise ValueError(f"Cannot clone {self.__local_git} already exists")

        self.__logger.info("Cloning base repository")
        git.Repo.clone_from(
            self.__remote_git,
            self.__local_git,
            branch=self.__branch,
            env={"GIT_SSH": self.__custom_ssh_path()},
        )

    def commit_and_push(self):
        if self.__contains_changes():
            self.__logger.info("Pushing modified repo")
            repo = git.Repo(self.__local_git)
            repo.git.add(all=True)
            repo.index.commit(f"Portainer check of {datetime.datetime.now()}")
            with repo.git.custom_environment(GIT_SSH=self.__custom_ssh_path()):
                repo.git.pull("origin", self.__branch)
                repo.git.push("origin", self.__branch)

    def __contains_changes(self):
        repo = git.Repo(self.__local_git)
        return repo.is_dirty() or len(repo.untracked_files) > 0

    def __custom_ssh_path(self):
        return os.path.join(
            os.path.abspath(os.getcwd()), "scripting/custom_ssh.sh"
        )
