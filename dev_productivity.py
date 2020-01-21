import json
from pr_data import get_pr_data_collection
from helper_functions import convert_repo_name_to_file_name


def dev_productivity(repo_name):
    pr_collection = get_pr_data_collection(repo_name)
    with open(convert_repo_name_to_file_name(repo_name) + '.json', 'w', encoding='utf-8') as f:
        json.dump(pr_collection, f, ensure_ascii=False, indent=4)


dev_productivity("razorpay/ifsc")
