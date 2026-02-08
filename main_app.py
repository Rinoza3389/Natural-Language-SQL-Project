import sqlite3
from openai import OpenAI

client = OpenAI(
  api_key="OPENAI_API_KEY"
)

def chatGPT_sql(question, schema):
    response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = [
            {
                "role":"user",
                "content": (
                    "You are an expert SQL generator."
                    "Only output a single SQLite SQL query."
                    "Do not explain anything or add markdown or comments.\n\n"
                    f"Database Schema: \n{schema}\n\n"
                    f"Question to Answer: \n{question}"
                )
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content.strip()

def run_GPT_sql(query, db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    try:
        cursor.execute(query)
        rows = cursor.fetchall()
    except Exception as e:
        rows = f"ERROR: {e}"

    conn.close()
    return rows

def chatGPT_explain(question, query, results):
    response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = [
            {
                "role":"user",
                "content": (
                    "Explain the following query results in clear, friendly language. Be as concise as possible, preferably only one sentence.\n\n"
                    f"Original Question: \n{question}\n\n"
                    f"Query Used: \n{query}\n\n"
                    f"Query Results: \n{results}"
                )
            }
        ],
        temperature=0.5
    )

    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    dbPATH = 'habit_tracker.db'

    schema = """
        users(user_id, user_name, start_date, last_log_date)
        habits(habit_id, user_id, habit_name, creation_date)
        habit_logs(log_id, habit_id, log_date, is_done)
        """
    
    q1 = "How many times was each habit completed?" #Super easy! No interpretation needed.
    q2 = "Which users completed the most habits last week?"  #Super easy! No interpretation needed.
    q3 = "Who has the longest current streak?"   #ChatGPT would need to figure out how to do this math, if it can.
    q4 = "What habits have the longest recorded streaks?"  #ChatGPT would need to figure out how to do this math, if it can.
    q5 = "What habits are people struggling with lately?"  #Not actually that hard, as long as Chat can figure out how to filter for "lately"
    q6 = "Who is the most consistent user?" #Super vague. What does consistent mean? Will User A (who's been around longer) be counted as more consistent than User D (who has only been around for a few days?)
    q7 = "Which habits are the hardest to maintain?" #Not super hard. It's basically just seeing which habits are missed the most.
    q8 = "Who sticks with habits?"  #A similar question to who is the most consistent user, so it'll be interesting to see how the response differs.

    questionsList = [q1, q2, q3, q4, q5, q6, q7, q8]

    for question in questionsList:
        print(f"CURRENT QUESTION: {question}\n")

        query = chatGPT_sql(question, schema)
        print(f"Generated Query:\n{query}\n")

        results = run_GPT_sql(query, dbPATH)
        print(f"Results of Query:\n{results}\n")

        explanation = chatGPT_explain(question, query, results)
        print(explanation)
        print("\n")