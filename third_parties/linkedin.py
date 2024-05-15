from dotenv import load_dotenv
import os
import json
import requests


load_dotenv("../dev/.env")


def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """
    :param linkedin_profile_url:
    :param mock:
    :return:
    scrape information from Linkedin profiles;
    Manullay scrape the information from linkedin profiles
    """
    print(os.environ.get("PROXY_CURL_KEY"))
    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/emarco177/0d6a3f93dd06634d95e46a2782ed7490/raw/78233eb934aa9850b689471a604465b188e761a0/eden-marco.json"
        response = requests.get(
            linkedin_profile_url,
            timeout=10,
        )
    else:
        api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
        header_dic = {"Authorization": f'Bearer {os.environ.get("PROXY_CURL_KEY")}'}
        response = requests.get(
            api_endpoint,
            params={"url": linkedin_profile_url},
            headers=header_dic,
            timeout=10,
        )

    # data = response.json()

    # f = open('../json/linkedinProfile.json')
    f = open('/Users/henry/PycharmProjects/langchain-demo/json/linkedinProfile.json')
    # returns JSON object as
    # a dictionary
    data = json.load(f)
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None)
           and k not in ["people_also_viewed", "certifications"]
    }
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    return data


if __name__ == "__main__":
    print(
        scrape_linkedin_profile(linkedin_profile_url="https://www.linkedin.com/in/hengliu1984/", mock=True)
    )
