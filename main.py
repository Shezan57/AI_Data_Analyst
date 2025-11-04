# step 1 extract schema from create_database.py
from sqlalchemy import create_engine, inspect
import json
import re
import sqlite3

db_url = "sqlite:///amazon.db"
db_path = "amazon.db"
def extract_schema(db_url):
    engine = create_engine(db_url)

    inspector = inspect(engine)

    tables = inspector.get_table_names()
    schema = {}

    for table_name in tables:
        columns = inspector.get_columns(table_name)
        schema[table_name] = [col['name'] for col in columns]

    return json.dumps(schema)

#  step 2 text to sql using deepseek ollama 
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from langchain_openai import ChatOpenAI

def text_to_sql(schema, user_query):

    SYSTEM_PROMPT = """
    You are an expert in converting natural language queries into SQL queries based on the provided database schema. The database schema is given in JSON format, where each table name maps to a list of its column names.

    When you receive a user query, analyze the schema to understand the relationships between tables and their columns. Construct an accurate SQL query that retrieves the requested information.

    Ensure that your SQL queries are syntactically correct and optimized for performance. Use appropriate JOINs, WHERE clauses, and aggregations as needed based on the user's request.

    Output only the SQL query without any additional text or explanations. Becauese the goal is to directly use the SQL query in a database context.
    """
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("user", "Given the following database schema in JSON format:\n{schema}\nConvert the following natural language query into an SQL query:\n{user_query}")
    ])

    # model = OllamaLLM(model="deepseek-r1:8b", temperature=0)
    model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    chain = prompt_template | model
    raw_response = chain.invoke({
        "schema": schema,
        "user_query": user_query
    })
    # cleaned_response = re.sub(r'<think>*?</think>','',raw_response, flags=re.DOTALL).strip()
    return raw_response.content

def get_data_from_database(user_query):

    schema = extract_schema(db_url)
    sql_query = text_to_sql(schema, user_query)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    result = cur.execute(sql_query).fetchall()
    conn.close()
    return result