from langchain import OpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
import logging
import tiktoken
import time
import os
from langchain.chains.question_answering import load_qa_chain

openai_api_key = os.environ.get("OPENAI_API_KEY")
# Summarization parameters
OPENAI_MODEL_NAME: str = "text-curie-001"
OPENAI_TOKENIZER_NAME: str = "cl100k_base"
OPENAI_MODEL_TEMPERATURE: float = 0.0  # 0 is fully deterministic, 1 is most random
OPENAI_MODEL_MAX_TOKENS: int = 500  # langchain automatically sets to max for OPENAI_MODEL_NAME
ANSWER_PROMPT_TEMPLATE: str = (
    "You are a world class journalist."
    "Answer a question by using information from a text."
    "Use as few words as possible."
    "Only include any information from the text that relates to the question."
    "The question is '{question}'"
    "Ignore any information that appear to be website artifacts."
     "Only include information that is found in the text."
    "Answer in the tone of the text."
    "The text is '{text}'"
)

# Summarization helpers
encoder = tiktoken.get_encoding(OPENAI_TOKENIZER_NAME)

answer_prompt = PromptTemplate(template=ANSWER_PROMPT_TEMPLATE, input_variables=["question", "text"])

def answer_follow_up_question(question: str, text: str, openai_api_key: str) -> str:
    """
    Arguments:
        question {str} -- Question
        text {str} -- Text

    Returns:
        str -- Answer
    """
    # Initialize OpenAI LLM with langchain
    llm = OpenAI(
        model_name=OPENAI_MODEL_NAME,
        temperature=OPENAI_MODEL_TEMPERATURE,
        max_tokens=OPENAI_MODEL_MAX_TOKENS,
        openai_api_key=openai_api_key,
    )
    text1 = Document(page_content=text)
    # Creating langchain summarize chain
    chain = load_qa_chain(llm, chain_type="stuff")
    answer = chain.run(input_documents=[text1], question=question)
    return answer

def main():
    text = "European markets live updates: News from WEF, data and earningsSkip NavigationwatchliveMarketsPre-MarketsU.S. MarketsCurrenciesCryptocurrencyFutures & CommoditiesBondsFunds & ETFsBusinessEconomyFinanceHealth & ScienceMediaReal EstateEnergyClimateTransportationIndustrialsRetailWealthLifeSmall BusinessInvestingPersonal FinanceFintechFinancial AdvisorsOptions ActionETF StreetBuffett ArchiveEarningsTrader TalkTechCybersecurityEnterpriseInternetMediaMobileSocial MediaCNBC Disruptor 50Tech GuidePoliticsWhite HousePolicyDefenseCongressEquity and OpportunityCNBC TVLive TVLive AudioBusiness Day ShowsEntertainment ShowsFull EpisodesLatest VideoTop VideoCEO InterviewsCNBC DocumentariesCNBC PodcastsCNBC WorldDigital OriginalsLive TV ScheduleWatchlistInvesting ClubTrust PortfolioAnalysisTrade AlertsVideoEducationPROPro NewsPro LiveSubscribeSign InMenuMake ItSelectUSAINTLwatchliveSearch quotes, news & videosWatchlistSIGN INCreate free accountMarketsBusinessInvestingTechPoliticsCNBC TVWatchlistInvesting ClubPROMenuLIVE UPDATESUpdated Tue, Jan 17 20233:16 AM ESTShareShare Article via FacebookShare Article via TwitterShare Article via LinkedInShare Article via EmailEuropean markets mixed as economic concerns dominate DavosElliot SmithHolly EllyattThis is CNBC's live blog covering European markets.European markets were muted on Tuesday, with concerns about the global economy high on the agenda at the World Economic Forum in Davos this week.European marketsThe pan-European Stoxx 600 hovered around the flatline in early trade, with autos adding 0.5% while retail stocks dropped by a similar amount.CNBC will be speaking to a range of delegates at the forum on Tuesday, including the leaders of Spain, Latvia, Lithuania and Poland and the CEOs of Unilever, UBS, Allianz, Swiss Re and many others. Follow our coverage here.Concerns over the direction of the global economy, persistent inflation, fragmentation and sluggish growth are high on the agenda, as well as the war in UkraineInvestors will also be digesting a slew of Chinese economic data that was released overnight, including figures showingÂ the nation's gross domestic productÂ grew by 3% in 2022, marking one of the slowest growths in decades.4 Min AgoStocks on the move: Leonardo up 4%, Ocado down 8%Shares of British digital grocer Ocado fell more than 8% in early trade to the bottom of the Stoxx 600 after the company missed fourth-quarter sales estimates as customers bought less per order ami the U.K.'s cost of living crisis.At the top of the European blue chip index, Italian aerospace and defense company Leonardo added 4.5%.- Elliot Smith8 Hours AgoCNBC Pro: This under-the-radar global carbon capture stock could soar by 65%, investment banks sayShares of an under-the-radar carbon capture company are expected to rise by 65% due to increasing global demand for emissions reduction technology, according to investment banks analyzing the stock.The company's latest innovation, revealed last week, could cut the energy needed to capture carbon and improve the company's profitability in the future, according to analysts at a German investment bank.CNBC Pro subscribers can read more here.â€” Ganesh Rao9 Hours AgoWhere the major indexes stand coming off the first two weeks of 2023 tradingWith the first two weeks of 2023 trading done, the three major indexes are up so far for the year.The Nasdaq Composite is leading the way, adding 5.9% as investors bought beaten-down technology stocks on rising hopes of an improving landscape for growth holdings. The S&P 500 and Dow followed, gaining 4.2% and 3.5%, respectively.â€” Alex Harring6 Hours AgoChina's retail sales beat estimates, economy expands more than expectedChina's December retail sales beat estimates, falling only 1.8% on an annualized basis, significantly better than the decline of 8.6% projected in a Reuters poll.Industrial output also grew 1.3% in December, higher than expectations for an increase of 0.2%.In the fourth quarter, China's economy expanded by 2.9% on an annualized basis, better than the expected 1.8% growth. While quarterly growth was flat, it still beat expectations for a 0.8% contraction.Despite better-than-expected data, the Chinese offshore yuan weakened sharply from 6.7403 to 6.7563 against the U.S. dollar shortly after the release.â€“ Jihye Lee4 Hours AgoEuropean markets: Here are the opening callsEuropean markets are heading for a flat to lower open Tuesday, with concerns about the global economy high on the agenda at the World Economic Forum in Davos this week.The U.K.'s FTSE 100 index is expected to open 1 point higher at 7,862, Germany's DAX 31 points lower at 15,111, France's CAC down 14 points at 7,033 and Italy's FTSE MIB down 37 points at 25,836, according to data from IG.CNBC will be speaking to a range of delegates at the World Economic Forum on Tuesday, including the presidents of Spain, Latvia, Lithuania and Poland and the CEOs of Unilever, UBS, Allianz and Swiss Re, among many others. Follow our coverage here.â€” Holly EllyattSubscribe to CNBC PROLicensing & ReprintsCNBC CouncilsSelect Personal FinanceCNBC on PeacockJoin the CNBC PanelSupply Chain ValuesSelect ShoppingClosed CaptioningDigital ProductsNews ReleasesInternshipsCorrectionsAbout CNBCAd ChoicesSite MapPodcastsCareersHelpContactNews TipsGot a confidential news tip? We want to hear from you.Get In TouchAdvertise With UsPlease Contact UsCNBC NewslettersSign up for free newsletters and get more CNBC delivered to your inboxSign Up NowGet this delivered to your inbox, and more info about our products and services.Â Privacy Policy|Do Not Sell My Personal Information|CA Notice|Terms of ServiceÂ© 2023 CNBC LLC. All Rights Reserved. A Division of NBCUniversalData is a real-time snapshot *Data is delayed at least 15 minutes. Global Business and Financial News, Stock Quotes, and Market Data and Analysis.Market Data Terms of Use and DisclaimersData also provided by"
    question = "What happened to European Markets?"
    answer = answer_follow_up_question(question, text, openai_api_key)
    print(answer)

if __name__ == "__main__":
    main()