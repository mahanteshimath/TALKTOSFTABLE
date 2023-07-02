import streamlit as st
import pandas as pd
from snowflake.connector import connect
from snowflake.connector.connection import SnowflakeConnection

# Share the connector across all users connected to the app
@st.cache_resource()
def get_connector() -> SnowflakeConnection:
    """Create a connector using credentials filled in Streamlit secrets"""
    connector = connect(**st.secrets["snowflake"], client_session_keep_alive=True)
    return connector

# Time to live: the maximum number of seconds to keep an entry in the cache
TTL = 24 * 60 * 60

# Using `experimental_memo()` to memoize function executions
@st.cache_data(ttl=TTL)
def get_databases(_connector) -> pd.DataFrame:
    """Get all databases available in Snowflake"""
    return pd.read_sql("SHOW DATABASES;", _connector)

@st.cache_data(ttl=TTL)
def get_data(_connector, database) -> pd.DataFrame:
    """Get tables available in this database"""
    query = f"SELECT * FROM {database}.INFORMATION_SCHEMA.TABLES;"
    return pd.read_sql(query, _connector)

st.markdown(f"## ❄️ Connecting to Snowflake")

snowflake_connector = get_connector()

databases = get_databases(snowflake_connector)
database = st.selectbox("Choose a Snowflake database", databases.name)

data = get_data(snowflake_connector, database)
st.write(f"👇 Find below the available tables in database `{database}`")
st.dataframe(data)