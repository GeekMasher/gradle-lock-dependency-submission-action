# gradle-lock-dependency-submission-action

Gradle Lock Dependency Submission Action

## Usage

```yaml
- name: Gradle Lock Dependency Submission Action
  uses: GeekMasher/gradle-lock-dependency-submission-action@main
  with:
    # [optonal] The path to the gradle.lock file. Defaults to finding all gradle*.lock in the current
    # working directory
    gradle-lock: "./gradle.lock"
    # [optional ] Token used to authenticate with the GitHub API. Defaults to the GITHUB_TOKEN secret.
    token: ${{ secrets.CODEQL_SUMMARY_GENERATOR_TOKEN }}
```

#### Workflow Example

```yaml
name: Gradle Lock Dependency Submission Action
on:
  push:
    branches: [main]

permissions: 
  contents: write   # needed

jobs:
  gradle-lock:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      # ... generate gradle.lock file

      - name: Gradle Lock Dependency Submission Action
        uses: GeekMasher/gradle-lock-dependency-submission-action@main
```
