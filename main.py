"""A small Python script to fetch GitHub contributions by organization members and
open-source contributors of a GitHub organization. It places the contributions data
in two CSV files: one for organization members and another for open-source contributors.
"""
import argparse
import csv
import os

import requests

# Read the GitHub access token from the environment variable.
ACCESS_TOKEN = os.environ.get("GITHUB_ACCESS_TOKEN")

# Define the REST API endpoint URL for organization repositories
ORG_REPOS_URL = f"https://api.github.com/orgs/{org_name}/repos"

# Set up headers with your access token
HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Accept": "application/vnd.github.v3+json",  # Use GitHub API version 3
}

if __name__ == "__main__":
    # Throw an error if the organization name or access token is not provided.
    if not ACCESS_TOKEN:
        raise ValueError("Please provide a GitHub personal access token")

    # Fetch Organization name from command line arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--org",
        help="GitHub organization name",
        type=str,
        required=True,
    )
    args = parser.parse_args()
    org_name = args.org

    # Make a GET request to fetch organization repositories.
    print(f"Fetching repositories in {org_name}...")
    response = requests.get(ORG_REPOS_URL, headers=HEADERS)

    # Retrieve the repositories data if the request is successful.
    if response.status_code == 200:
        org_repos_data = response.json()

        # Fetch the list of organization members.
        members_url = f"https://api.github.com/orgs/{org_name}/members"
        members_response = requests.get(members_url, headers=HEADERS)

        # Retrieve the members data if the request is successful.
        if members_response.status_code == 200:
            print("Fetching organization members...\n")
            members_data = members_response.json()

            # Create a set of organization member usernames for faster lookup.
            org_members = {member["login"] for member in members_data}

            # Create dictionaries to store contributions information.
            org_member_contributions = {}
            open_source_contributions = {}

            # Loop through the repositories in the organization.
            for repo in org_repos_data:
                print(f"Fetching contributors data in {repo['name']}...")
                repo_name = repo["name"]

                # Define the REST API endpoint URL for contributors in the repository.
                repo_contributors_url = (
                    f"https://api.github.com/repos/{org_name}/{repo_name}/contributors"
                )

                # Make a GET request to fetch contributors in the repository
                contributors_response = requests.get(
                    repo_contributors_url, headers=HEADERS
                )

                # Retrieve the contributions data if the request is successful.
                if contributors_response.status_code == 200:
                    contributors_data = contributors_response.json()

                    # Loop through the contributors in the repository.
                    for contributor in contributors_data:
                        contributor_name = contributor["login"]
                        contributions = contributor["contributions"]

                        # Filter data based on organization membership.
                        if contributor_name in org_members:
                            if contributor_name in org_member_contributions:
                                org_member_contributions[
                                    contributor_name
                                ] += contributions
                            else:
                                org_member_contributions[
                                    contributor_name
                                ] = contributions
                        else:
                            if contributor_name in open_source_contributions:
                                open_source_contributions[
                                    contributor_name
                                ] += contributions
                            else:
                                open_source_contributions[
                                    contributor_name
                                ] = contributions

        # Sort contributors by contributions and write to CSV files
        org_member_contributions_sorted = sorted(
            org_member_contributions.items(), key=lambda x: x[1], reverse=True
        )
        open_source_contributions_sorted = sorted(
            open_source_contributions.items(), key=lambda x: x[1], reverse=True
        )

        # Define the CSV file names.
        print("\nSaving contributions overview to CSV files...")
        org_member_csv_file = "org_member_contributions_overview.csv"
        open_source_csv_file = "open_source_contributions_overview.csv"

        # Write organization member contributions to a CSV file.
        with open(org_member_csv_file, mode="w", newline="") as org_member_file:
            writer = csv.writer(org_member_file)
            writer.writerow(["Username", "Contributions"])
            writer.writerows(org_member_contributions_sorted)

        # Write open-source contributions to a CSV file.
        with open(open_source_csv_file, mode="w", newline="") as open_source_file:
            writer = csv.writer(open_source_file)
            writer.writerow(["Username", "Contributions"])
            writer.writerows(open_source_contributions_sorted)

        print(f"Organization member contributions saved to {org_member_csv_file}")
        print(f"Open-source contributions saved to {open_source_csv_file}")
    else:
        print(f"Request failed with status code {response.status_code}")
