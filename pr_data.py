# Author: Sammarth Kapse
from helper_functions import *


def get_pr_data_collection(repo_name):
    pr_collection = []
    historical_data = get_historical_data(repo_name)
    for entry in historical_data:
        pr_information = get_pr_information(entry[URL])
        pr_collection.append(pr_information)

    return pr_collection


def get_pr_information(pr_url):
    pr_data = fetch_data_from_github_api(pr_url)
    pr_information = {REPO: pr_data[BASE][REPO][FULL_NAME], NUMBER: pr_data[NUMBER], TITLE: pr_data[TITLE],
                      AUTHOR: pr_data[USER][LOGIN], CREATED_AT: pr_data[CREATED_AT], CLOSED_AT: pr_data[CLOSED_AT],
                      MERGED_AT: pr_data[MERGED_AT], MERGED_BY: get_merged_by(pr_data[MERGED_BY]),
                      NUMBER_OF_LINES_ADDED: pr_data[ADDITIONS], NUMBER_OF_LINES_DELETED: pr_data[DELETIONS],
                      COMMITS: get_pr_commits(pr_data[URL] + "/" + COMMITS), COMMENTS: get_pr_comments(pr_data[URL]),
                      PENDING_REVIEWERS: get_requested_reviewers(pr_data[REQUESTED_REVIEWERS])}

    return pr_information
