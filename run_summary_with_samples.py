from cronkite import feed_summary
import os

summary_files = [
    open("tmp/experiment-scripts/summaries/" + i).read()
    for i in os.listdir("tmp/experiment-scripts/summaries")
    if i.endswith(".txt")
]


# Creating dictionary
summary_dicts = [
    {
        "title": " ".join(i.split("\n")[0].split(": ")[1:]),
        "date": i.split("\n")[1].split(": ")[1],
        "url": i.split("\n")[2].split(": ")[1],
        "summary": "\n".join(i.split("\n")[4:]),
    }
    for i in summary_files
]

executive_summary = feed_summary.executive_summary_map_reduce(
    articles_data=summary_dicts, openai_api_key=os.environ.get("OPENAI_API_KEY")
)

print(executive_summary["output_text"])
