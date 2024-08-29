import streamlit as st
import sqlite3

import openai
#pip install openai==0.28

# Set OpenAI API configuration
openai.api_type = "azure"
openai.api_version = "2023-03-15-preview"
openai.api_key = "abc"
openai.api_base = "https://ai-proxy.lab.abc.com"


# Define a function to generate responses using OpenAI Chat Completion API
def generate_responses(question):
    conversation = [
            {"role": "system", 
             "content": """You are an expert in converting English questions to SQL query!
                            The SQL database has the name STUDENT and has the following columns - NAME, CLASS, 
                            SECTION \n\nFor example,
                            \nExample 1 - How many entries of records are present?, 
                            the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ;
                            \nExample 2 - Tell me all the students studying in Data Science class?, 
                            the SQL command will be something like this SELECT * FROM STUDENT 
                            where CLASS="Data Science"; 
                            also the sql code should not have ``` in beginning or end and sql word in output"""},
            {"role": "user", 
             "content": f"Query:\n{question}"}
        ]
    response = openai.ChatCompletion.create(
            engine="gpt-35-turbo-16k",
            messages=conversation,
            temperature=0.1
        )
    responses = response["choices"][0]["message"]["content"]
    return responses


## Fucntion To retrieve query from the database
def read_sql_query(sql,db):
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows


## Streamlit App

st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Gemini App To Retrieve SQL Data")

question=st.text_input("Input: ",key="input")

submit=st.button("Ask the question")

# if submit is clicked
if submit:
    response=generate_responses(question)
    print(response)
    response=read_sql_query(response,"student.db")
    st.subheader("The REsponse is")
    for row in response:
        print(row)
        st.header(row)