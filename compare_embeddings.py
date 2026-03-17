import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain.evaluation import load_evaluator
# import openai


# Load environment variables (assume that project contains .env file with API keys)
load_dotenv()

# Set OpenAI API key (unnecessary)
# openai.api_key = os.environ['OPENAI_API_KEY']

def main():
    # Get embedding for a word
    embedding_function = OpenAIEmbeddings(model="text-embedding-3-small")
    vector = embedding_function.embed_query("pineapple")
    print(f"Vector for 'pineapple': {vector}")
    print(f"Vector length: {len(vector)}")

    # Compare vector of words
    evaluator = load_evaluator("pairwise_embedding_distance")
    words = ("pineapple", "jackfruit", "apple")
    x = evaluator.evaluate_string_pairs(prediction=words[0], prediction_b=words[1])
    y = evaluator.evaluate_string_pairs(prediction=words[0], prediction_b=words[2])
    print(f"Comparing ({words[0]}, {words[1]}): {x}")
    print(f"Comparing ({words[0]}, {words[2]}): {y}")


if __name__ == "__main__":
    main()
