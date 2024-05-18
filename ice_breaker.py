import os
from typing import Tuple
from langchain.chains import LLMChain
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI

from output_parser import summary_parser,Summary
from third_parties.linkedin import scrape_linkedin_profile
from third_parties.twitter import scrape_user_tweets
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from agents.twitter_lookup_agent import lookup as twitter_lookup_agent
from dotenv import load_dotenv


def ice_break_with(name: str)->Tuple[Summary, str]:
    # print("Hello Langchain")
    # print(os.environ['OPENAI_API_KEY'])
    print(os.environ['TWITTER_API_KEY'])

    linkedin_url = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_url, mock=True)

    twitter_username = twitter_lookup_agent(name=name)
    tweets = scrape_user_tweets(username=twitter_username, mock=True)

    # for mock, real information is from linkedlin
#     information = """
#     Elon Reeve Musk (/ˈiːlɒn/ EE-lon; born June 28, 1971) is a businessman and investor. He is the founder, chairman, CEO, and CTO of SpaceX; angel investor, CEO, product architect, and former chairman of Tesla, Inc.; owner, executive chairman, and CTO of X Corp.; founder of the Boring Company and xAI; co-founder of Neuralink and OpenAI; and president of the Musk Foundation. He is one of the wealthiest people in the world, with an estimated net worth of US$190 billion as of March 2024, according to the Bloomberg Billionaires Index, and $195 billion according to Forbes, primarily from his ownership stakes in Tesla and SpaceX.[5][6]
# A member of the wealthy South African Musk family, Elon was born in Pretoria and briefly attended the University of Pretoria before immigrating to Canada at age 18, acquiring citizenship through his Canadian-born mother. Two years later, he matriculated at Queen's University at Kingston in Canada. Musk later transferred to the University of Pennsylvania, and received bachelor's degrees in economics and physics. He moved to California in 1995 to attend Stanford University, but dropped out after two days and, with his brother Kimbal, co-founded online city guide software company Zip2. The startup was acquired by Compaq for $307 million in 1999, and that same year Musk co-founded X.com, a direct bank. X.com merged with Confinity in 2000 to form PayPal.
#     """


    summary_template = """
        given the information about a person from linkedin {information},
    and their latest twitter posts {twitter_posts} I want you to create:
    1. A short summary
    2. two interesting facts about them 

    Use both information from twitter and Linkedin
     \n{format_instructions}
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information","twitter_posts"],
        template=summary_template,
        partial_variables={
            "format_instructions": summary_parser.get_format_instructions()
        },
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    # chain = LLMChain(llm=llm, prompt=summary_prompt_template)
    chain = summary_prompt_template | llm | summary_parser

    #res:Summary  means Summary is the part of res
    res = chain.invoke(input={"information": linkedin_data,"twitter_posts": tweets})
    return res, linkedin_data.get("profile_pic_url")

    """
    1. Short Summary:
Eden Marco is a Customer Engineer at Google with a background in backend development and a passion for teaching. They have experience working at companies like Orca Security and Deep Instinct, and hold a Bachelor's Degree in Computer Science from Technion - Israel Institute of Technology. In addition to their professional work, they are also a best-selling Udemy instructor.

2. Two Interesting Facts:
- Eden Marco recently showcased the risks of deploying insecure LLM agents to the cloud without basic security measures, highlighting the importance of cybersecurity in cloud environments.
- They have worked as a Captain in the Israel Defense Forces before transitioning to a career in tech, showcasing their diverse background and experiences.
    
    """

if __name__ == "__main__":
    load_dotenv("dev/.env")
    print("ice breaker Enter")
    ice_break_with(name="Eden Marco udemy") #it might get different result, but you can get precisse result by inputting more details
