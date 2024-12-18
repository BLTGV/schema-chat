import streamlit as st
import os
from dotenv import load_dotenv
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.chat_models import ChatOpenAI
from langchain.agents import AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
from sqlalchemy import create_engine, inspect

# Page config
st.set_page_config(page_title="DB Schema Documentation Assistant", layout="wide")

# Initialize session states
if "messages" not in st.session_state:
    st.session_state.messages = []
if "db_inspector" not in st.session_state:
    st.session_state.db_inspector = None
if "agent_executor" not in st.session_state:
    st.session_state.agent_executor = None

def create_connection_string(db_type, host, port, database, username, password):
    if db_type == "PostgreSQL":
        return f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}"
    elif db_type == "MySQL":
        return f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
    return None

def initialize_agent(connection_string):
    try:
        db = SQLDatabase.from_uri(connection_string)
        llm = ChatOpenAI(temperature=0, model_name="gpt-4")
        toolkit = SQLDatabaseToolkit(db=db, llm=llm)
        
        # Initialize memory with Streamlit chat message history
        msgs = StreamlitChatMessageHistory()
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="output",
            chat_memory=msgs
        )
        
        agent_executor = create_sql_agent(
            llm=llm,
            toolkit=toolkit,
            verbose=True,
            agent_type="openai-tools",
            memory=memory,
        )
        
        return agent_executor
    except Exception as e:
        st.error(f"Error initializing agent: {str(e)}")
        return None

# Load environment variables
load_dotenv()

# Check for OpenAI API key
if not os.getenv("OPENAI_API_KEY"):
    st.error("Please set OPENAI_API_KEY in your environment or .env file")
    st.stop()

# Sidebar for database connection
with st.sidebar:
    st.title("Database Connection")
    db_type = st.selectbox("Database Type", ["PostgreSQL", "MySQL"])
    host = st.text_input("Host", "localhost")
    port = st.text_input("Port", "5432" if db_type == "PostgreSQL" else "3306")
    database = st.text_input("Database Name")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Connect"):
        if all([host, port, database, username, password]):
            connection_string = create_connection_string(
                db_type, host, port, database, username, password
            )
            if connection_string:
                st.session_state.agent_executor = initialize_agent(connection_string)
                if st.session_state.agent_executor:
                    st.success("Successfully connected to database!")
        else:
            st.error("Please fill in all fields")

# Main chat interface
st.title("DB Schema Documentation Assistant")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask about your database schema"):
    if not st.session_state.agent_executor:
        st.error("Please connect to a database first!")
    else:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.agent_executor.run(
                    input=prompt
                )
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.markdown(response)
