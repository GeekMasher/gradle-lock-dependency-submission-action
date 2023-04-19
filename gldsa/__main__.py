import json
import os
import argparse

from gldsa.dependencies import Dependency, exportDependencies
from gldsa.octokit import Octokit

parser = argparse.ArgumentParser(__name__)

parser.add_argument("-g", "--gradle-lock", help="Gradle Lockfile")

parser.add_argument("-sha", default=os.environ.get("GITHUB_SHA"), help="Commit SHA")
parser.add_argument("-ref", default=os.environ.get("GITHUB_REF"), help="Commit ref")

parser_github = parser.add_argument_group("GitHub")
parser_github.add_argument(
    "-gr",
    "--github-repository",
    default=os.environ.get("GITHUB_REPOSITORY"),
    help="GitHub Repository",
)
parser_github.add_argument(
    "-gi",
    "--github-instance",
    help="GitHub API Instance",
)
parser_github.add_argument(
    "-t",
    "-gt",
    "--github-token",
    default=os.environ.get("GITHUB_TOKEN"),
    help="GitHub API Token",
)


def findGradleLocks(path: str) -> list[str]:
    """Find the gradle.lockfile in the path"""
    results = []
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith("lockfile") and file.startswith("gradle"):
                results.append(os.path.join(root, file))
    return results


def parseGradleLock(path: str) -> list[Dependency]:
    if not os.path.exists(path):
        raise Exception(f"File not found: {path}")

    results = []
    with open(path, "r") as handle:
        lines = handle.readlines()

    for line in lines:
        line = line.strip()
        if line == "" or line.startswith("#"):
            continue

        namespace, instances = line.split("=", 1)
        # TODO: skip non compileClasspath ?

        try:
            package, name, version = namespace.split(":", 2)
        except:
            # TODO: handle this
            continue

        results.append(
            Dependency(
                namespace=package,
                name=name,
                version=version,
                manager="maven",
                path=path,
            )
        )
    return results


if __name__ == "__main__":
    arguments = parser.parse_args()

    if not arguments.github_repository:
        print("No GitHub Repository")
        exit(1)
    if not arguments.github_token:
        print("No GitHub Token")
        exit(1)

    owner, name = arguments.github_repository.split("/")
    octokit = Octokit(
        owner=owner,
        repo=name,
        token=arguments.github_token,
        # instance
    )

    lock_files = []
    if arguments.gradle_lock:
        lock_files.append(arguments.gradle_lock)
    else:
        lock_files = findGradleLocks(".")

    if len(lock_files) == 0:
        print("No lockfiles found")
        exit(0)

    for path in lock_files:
        print(f"Found lockfile: {path}")

        dependencies = parseGradleLock(path)
        print(f"Dependencies :: {len(dependencies)}")

        deps = exportDependencies(
            path, dependencies, sha=arguments.sha, ref=arguments.ref
        )
        print(json.dumps(deps, indent=2))

        octokit.submitDependencies(deps)
        print(f"Uploaded :: {path}")

