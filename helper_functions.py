import requests
from static_variables import *


def get_historical_data(repo_name):
    token = 'ac08edcd81da07a1e5cfa1904dd44aa6de63f3b4'
    headers = {'Authorization': 'token ' + token}
    url = BASE_URL + "/" + repo_name + "/" + PULLS_ALL
    print(url)
    historical_data = []

    while 1:
        response = requests.get(url, headers=headers)
        response_in_json = response.json()
        historical_data += response_in_json
        print(historical_data)
        if LINK in response.headers:
            url = get_next_page_url(response.headers[LINK])
        else:
            url = None

        if url is None:
            break

    return historical_data


def get_next_page_url(links):
    links = links.split(", ")
    for link in links:
        ind = link.find('next')
        if ind != -1:
            return link[1:ind-8]

    return None


def fetch_data_from_github_api(url):
    token = 'ac08edcd81da07a1e5cfa1904dd44aa6de63f3b4'
    headers = {'Authorization': 'token ' + token}
    response = requests.get(url, headers=headers)
    response_in_json = response.json()

    return response_in_json


def get_merged_by(merged_by):
    if merged_by is None:
        return None
    else:
        return merged_by[LOGIN]


def get_pr_commits(commits_url):
    commits_data = fetch_data_from_github_api(commits_url)
    commits = []
    for commit_data in commits_data:
        commit = {SHA: commit_data[SHA], COMMITED_AT: commit_data[COMMIT][AUTHOR][DATE]}
        if commit_data[AUTHOR] is None:
            commit[AUTHOR] = commit_data[COMMIT][AUTHOR][NAME]
        else:
            commit[AUTHOR] = commit_data[AUTHOR][LOGIN]
        commits.append(commit)

    return commits


def get_requested_reviewers(requested_reviewers):
    output = []
    for reviewer in requested_reviewers:
        user = {USER: reviewer[LOGIN]}
        output.append(user)
    return output


def get_pr_comments(pr_url):
    review_comments = get_review_comments(pr_url + "/" + REVIEWS)
    line_comments = get_line_comments(pr_url + "/" + COMMENTS)
    comments = review_comments + line_comments
    return comments


def get_review_comments(url):
    reviews = fetch_data_from_github_api(url)

    review_comments = []
    for review in reviews:
        if review[BODY] and review[STATE] != PENDING:
            value = {AUTHOR: review[USER][LOGIN], BODY: review[BODY], SUBMITTED_AT: review[SUBMITTED_AT]}
            review_comments.append(value)

    return review_comments


def get_line_comments(url):
    comments = fetch_data_from_github_api(url)
    line_comments = []
    for comment in comments:
        value = {AUTHOR: comment[USER][LOGIN], BODY: comment[BODY], SUBMITTED_AT: comment[UPDATED_AT]}
        line_comments.append(value)

    return line_comments


def convert_repo_name_to_file_name(repo_name):
    file_name = ""
    for letter in repo_name:
        if letter == '/':
            file_name += '_'
        else:
            file_name += letter

    return file_name
