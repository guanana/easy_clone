import argparse
import os
from pathlib import Path
from importlib.metadata import version
from git import Repo, GitCommandError

base_repo_dir = Path("~/PycharmProjects").expanduser()
pycharm_path = os.getenv("EASY_CLONE_PYCHARM_PATH", "/Applications/PyCharm\ CE.app/Contents/MacOS/pycharm")


def is_repo_ssh(git_url: str):
    if git_url.startswith("git@") or git_url.startswith("gitlab@"):
        return True
    else:
        return False


def git_url_to_dir(git_url: str):
    is_ssh = is_repo_ssh(git_url)
    if is_ssh:
        git_url = git_url.replace("git@", "")
        git_url = git_url.replace("gitlab@", "")
        git_url = git_url.replace(":", "/")
    else:
        git_url = git_url.replace("https://", "")
    git_url = git_url.replace(".git", "")
    return git_url


def clone(git_url, clone_dir=None):
    repo_dir = git_url_to_dir(git_url)
    repo_dir = Path.joinpath(base_repo_dir, repo_dir)
    if clone_dir:
        repo_dir = clone_dir
    print(f"Cloning {git_url} to {repo_dir}")
    try:
        Repo.clone_from(git_url, repo_dir)
    except GitCommandError:
        print("Repository already cloned")

    return repo_dir


def open_repo(repo_dir, binary=pycharm_path):
    print(f"Opening {repo_dir} in IDE")
    os.system(f"{binary} {repo_dir}")


def get_arg_parser():
    """CLI handler"""
    # Main parser
    parser = argparse.ArgumentParser(prog=__file__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-u', '--url',
                       help='Git URL to clone')
    group.add_argument("git_url", nargs='?', help='Git URL to clone')
    parser.add_argument('-d', '--directory',
                        help='Name of the directory to clone to, defaults to ~/PycharmProjects/<<full repo path>>',
                        default=None, required=False)
    parser.add_argument('-o', '--open',
                        help='Open respository on pycharm after cloning, '
                             'override pycharm path with EASY_CLONE_PYCHARM_PATH env var',
                        action=argparse.BooleanOptionalAction,
                        type=bool, default=True, required=False)
    parser.add_argument('-v', '--version', action='version', version=version('easy_clone'))

    return parser


def run():
    args = get_arg_parser().parse_args()
    url = args.url if args.url else args.git_url
    cloned_dir = clone(git_url=url, clone_dir=args.directory)
    if args.open:
        open_repo(cloned_dir)


if __name__ == "__main__":
    run()
