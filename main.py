import os
from typing import Dict
import warnings

from openai import OpenAI

from config import openai_config, query_config
from text_processor import analyze_text

warnings.filterwarnings("ignore")

os.environ["OPENAI_API_KEY"] = openai_config["api_key"]


def generate_report(file_analysis: Dict[str, str]) -> str:
    """
    Generates a report comparing the perspectives of multiple books.

    Args:
        file_analysis (Dict[str, str]): A dictionary where keys are book titles and values are their analysis.

    Returns:
        str: The generated report comparing the perspectives of multiple books.
    """
    prompt = (
        f"Write a 5-paragraph book report comparing {len(file_analysis)} books' perspectives on {query_config['query']}. "
        "Your report must:\n"
        "- Include a clear thesis statement in the introduction.\n"
        "- Use arguments supported by specific excerpts or citations from the analyses provided.\n"
        "- Accurately cite the lines from excerpts in quotes by referring to the specific text.\n"
        "- Conclude with a paragraph summarizing your arguments and reinforcing the thesis.\n\n"
        "The books' titles are: " + ", ".join(file_analysis.keys()) + "\n\n"
    )

    for title, analysis in file_analysis.items():
        prompt += f"Analysis of '{title}':\n{analysis}\n\n"

    prompt += (
        "When writing the report, refer directly to the excerpts (e.g., as mentioned in '(excerpt)') to support your arguments.\n\n"
        "Do not use any special formatting. Begin your report now:"
    )

    client = OpenAI()
    response = client.chat.completions.create(
        model=openai_config["model"],
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=openai_config["temperature"],
        max_tokens=openai_config["max_output_tokens"]
    )
    return response.choices[0].message.content


def main() -> None:
    files_to_analyze = os.listdir(query_config["input_files_dir"])
    files_analysis = {}

    for file in files_to_analyze:
        print("\n\nAnalyzing file:", file)
        file_path = os.path.join(query_config["input_files_dir"], file)
        analysis = analyze_text(file_path, len(files_to_analyze))

        filename = file.split(".")[0]
        files_analysis[filename] = analysis

    print("\n\nGenerating report...")
    report = generate_report(files_analysis)

    with open(query_config["output_file"], "w", encoding="utf-8") as output_file:
        output_file.write(report)
    print("\n\nReport generated and saved to", query_config["output_file"])


if __name__ == "__main__":
    main()
