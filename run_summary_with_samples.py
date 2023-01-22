from cronkite import feed_summary
import json
import os

sample_location = "samples/world/summaries/"
summary_dicts = []
for i in os.listdir(sample_location):
    with open(os.path.join(sample_location, i), "r") as f:
        summary_dicts.append(json.loads(f.read()))

executive_summary = feed_summary.executive_summary_map_reduce(
    articles_data=summary_dicts, openai_api_key=os.environ.get("OPENAI_API_KEY")
)

print(executive_summary["output_text"])
