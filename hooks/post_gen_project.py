import os
import pathlib
import subprocess
import sys

path_conda_executable = pathlib.Path(os.environ["CONDA_EXE"])
path_mamba_executable = path_conda_executable.parent.joinpath(
    path_conda_executable.name.replace("conda", "mamba")
)

# initialize new project repository
subprocess.run(["git", "init"], check=True)
subprocess.run(["git", "add", "."], check=True)
subprocess.run(
    ["git", "commit", "-m", "chore: initialize repo from data science template"], check=True
)
subprocess.run(["git", "branch", "-m", "main"], check=True)
subprocess.run(["git", "remote", "add", "origin", "{{cookiecutter.repo_url}}"], check=True)

# initialize ci based on user preference
CI_FILES = ['.gitlab-ci.yml', '.gitlab-ci-test.yaml', '.gitlab-ci-stages.yaml']
# Include CI 
if '{{cookiecutter.include_ci_files}}'.lower() == 'yes':
    # Select platform for the project
    ci_platform = input('Which CI platform do you want to use? [GitLab, GitHub] ').strip().lower()
    # GitHub
    if ci_platform == 'github':
        for file_name in CI_FILES:
            file_path = os.path.join(os.getcwd(), file_name)
            if os.path.exists(file_path):
                os.remove(file_path)
        print("Sorry, GitHub CI is not supported yet. It will become available in a future version.", file=sys.stderr)
        sys.exit(1)
elif '{{cookiecutter.include_ci_files}}'.lower() == 'no':
    for file_name in CI_FILES:
        file_path = os.path.join(os.getcwd(), file_name)
        print(os.path)
        print(file_path)
        if os.path.exists(file_path):
            os.remove(file_path)

# setup environment
subprocess.run(
    [path_mamba_executable, "env", "create", "-f", "environment.yaml", "--quiet"], check=True
)
subprocess.run(
    [
        path_mamba_executable,
        "run",
        "--no-banner",
        "-n",
        "{{cookiecutter.env_name}}",
        "pre-commit",
        "install",
    ],
    check=True,
)
