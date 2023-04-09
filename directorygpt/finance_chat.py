import embed_files
import chat_files

queries = [
"How is the budget deficit funded, using only evidence from the provided files?",
"How do Fed rates affect housing availability and affordability?",
"How has the Federal Reserve's monetary policy affected interest rates and the US deficit? I'm particularly interested in Bloomberg reports on the subject.",
"How might interest rates in the US move in the future?",
"Can you summarize the Federal Reserve Monetary Policy Report?"
]

# embed_files.generate_embeddings('./embeddings/finance-dir', "./demo-files/finance", chunk_size=300)
finance_chatbot = chat_files.make_chatbot("./embeddings/finance-dir", top_k_docs=10)

# default_prompt = " What files (and pages) did you get your information from? Do in-text citations and list the sources using bullets/dashes."

for query in queries:
    print(f"Asking query: {query}")
    chat_files.ask_query(finance_chatbot, query)
    print("\n\n\n")