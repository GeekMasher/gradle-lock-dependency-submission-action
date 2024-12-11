<!-- markdownlint-disable -->
<div align="center">
<h1>gradle-lock-dependency-submission-action</h1>

[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)][github]
[![GitHub Stars](https://img.shields.io/github/stars/GeekMasher/gradle-lock-dependency-submission-action?style=for-the-badge)][github]
[![GitHub Issues](https://img.shields.io/github/issues/GeekMasher/gradle-lock-dependency-submission-action?style=for-the-badge)][github-issues]
[![Licence](https://img.shields.io/github/license/Ileriayo/markdown-badges?style=for-the-badge)][license]

</div>
<!-- markdownlint-restore -->

## Overview

Gradle Lock Dependency Submission Action allows you to submit a gradle.lock file to the GitHub Dependency Graph.

## Usage

```yaml
- name: Gradle Lock Dependency Submission Action
  uses: GeekMasher/gradle-lock-dependency-submission-action@v1.0.0
```

### Action Inputs

```yaml
- name: Gradle Lock Dependency Submission Action
  uses: GeekMasher/gradle-lock-dependency-submission-action@v1.0.0
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
        uses: GeekMasher/gradle-lock-dependency-submission-action@v1.0.0
```

## License

This project is licensed under the terms of the MIT open source license. Please refer to [MIT](./LICENSE) for the full terms.

## Maintainers

Maintained by [@GeekMasher](https://github.com/GeekMasher).

## Support

Please create GitHub Issues and Discussions for any feature requests, bugs, or documentation problems.

## Acknowledgement

- @GeekMasher: Author and Maintainer

<!-- Resources -->

[license]: ./LICENSE
[github]: https://github.com/GeekMasher/gradle-lock-dependency-submission-action
[github-issues]: https://github.com/GeekMasher/gradle-lock-dependency-submission-action/issues