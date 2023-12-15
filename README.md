# Org Contributors Contributions Overview

This Python script fetches GitHub contributions data for both organization members and open-source contributors of a specified GitHub organization. The data is then exported into two separate CSV files.

## Prerequisites

1. Python 3.6 or higher. If you don't have Python installed, you can download it from [python.org](https://www.python.org/downloads/).
2. A GitHub access token. This should be stored in an environment variable named `GITHUB_ACCESS_TOKEN`. If you don't have a token, you can create one by following the instructions in the [GitHub documentation](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token).

## Usage

1. Clone this repository and navigate into its directory.
2. Add the GitHub access token to an environment variable named `GITHUB_ACCESS_TOKEN`.
3. Run the script by using the following command:

   ```bash
   python main.py --org <organization name>
   ```

Replace `<organization name>` with the name of the GitHub organization you want to fetch contributions data for.

## Output

The script will generate two CSV files:

1. `org_members_contributions.csv`: Contains contributions data for members of the specified organization.
1. `open_source_contributors_contributions.csv`: Contains contributions data for open-source contributors to the specified organization's repositories.

Each row in the CSV files represents a contributor and their contributions data.
