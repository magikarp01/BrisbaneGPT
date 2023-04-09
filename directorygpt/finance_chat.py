import embed_files
import chat_files

# embed_files.generate_embeddings('./embeddings/finance-dir', "./demo-files/finance")
# query = "How is the budget deficit funded, using only evidence from the provided files?"
query = "How has the Federal Reserve's monetary policy affected interest rates and the US deficit, and how might they move in the future? I'm particularly interested in Bloomberg reports on the subject."
finance_chatbot = chat_files.make_chatbot("./embeddings/finance-dir", top_k_docs=6)
chat_files.ask_query(finance_chatbot, query)
