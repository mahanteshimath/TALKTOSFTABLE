import streamlit as st
from snowflake.snowpark import Session

#import openai


## Validate Snowflake connection ##


st.title('❄️ How to connect Streamlit to a Snowflake database')

# Establish Snowflake session
@st.cache_resource
def create_session():
    return Session.builder.configs(st.secrets.snowflake).create()

session = create_session()
st.success("Connected to Snowflake!")

conn = st.experimental_connection("snowpark")
df = conn.query("select current_warehouse()")
st.write(df)

## Validate OpenAI connection ##
# openai.api_key = st.secrets["OPENAI_API_KEY"]

# completion = openai.ChatCompletion.create(
#   model="gpt-3.5-turbo",
#   messages=[
#     {"role": "user", "content": "What is Streamlit?"}
#   ]
# )

# st.write(completion.choices[0].message.content)
