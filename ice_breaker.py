import os

from langchain.chains import LLMChain
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI

from third_parties.linkedin import scrape_linkedin_profile
from dotenv import load_dotenv

load_dotenv("dev/.env")
if __name__ == "__main__":

    print("Hello Langchain")
    print(os.environ['OPENAI_API_KEY'])
    print(os.environ['COOL_API_KEY'])
    information = """
    Elon Reeve Musk (/ˈiːlɒn/ EE-lon; born June 28, 1971) is a businessman and investor. He is the founder, chairman, CEO, and CTO of SpaceX; angel investor, CEO, product architect, and former chairman of Tesla, Inc.; owner, executive chairman, and CTO of X Corp.; founder of the Boring Company and xAI; co-founder of Neuralink and OpenAI; and president of the Musk Foundation. He is one of the wealthiest people in the world, with an estimated net worth of US$190 billion as of March 2024, according to the Bloomberg Billionaires Index, and $195 billion according to Forbes, primarily from his ownership stakes in Tesla and SpaceX.[5][6]
A member of the wealthy South African Musk family, Elon was born in Pretoria and briefly attended the University of Pretoria before immigrating to Canada at age 18, acquiring citizenship through his Canadian-born mother. Two years later, he matriculated at Queen's University at Kingston in Canada. Musk later transferred to the University of Pennsylvania, and received bachelor's degrees in economics and physics. He moved to California in 1995 to attend Stanford University, but dropped out after two days and, with his brother Kimbal, co-founded online city guide software company Zip2. The startup was acquired by Compaq for $307 million in 1999, and that same year Musk co-founded X.com, a direct bank. X.com merged with Confinity in 2000 to form PayPal.
    """
    summary_template = """
        given the linkedin information {information} about a person I want you to create
        1.A short summary
        2.two interesting facts about them
    """

    summary_prompt_template = PromptTemplate(input_variables=["information"], template=summary_template)

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    chain = LLMChain(llm=llm, prompt=summary_prompt_template)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url='https://www.linkedin.com/in/hengliu1984/', mock=True)
    res = chain.invoke(input={"information": linkedin_data})
    print(res)
