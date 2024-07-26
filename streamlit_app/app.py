import sys
import os
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json

# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from streamlit_app.financial_data import get_stock_data, get_stock_symbols
from models.vertex_ai_model import ask_vertex_ai

# Load credentials from secrets
credentials = st.secrets["gcp_service_account"]

# Function to generate summary text from visualizations
def generate_visualization_summary(data):
    summary = ""
    
    # Summarize closing prices
    closing_prices = data['Close'].describe()
    summary += f"The closing prices range from {closing_prices['min']} to {closing_prices['max']} with an average of {closing_prices['mean']}.\n"

    # Summarize trading volumes
    trading_volumes = data['Volume'].describe()
    summary += f"Trading volumes range from {trading_volumes['min']} to {trading_volumes['max']} with an average of {trading_volumes['mean']}.\n"

    return summary

# Initialize session state for chatbot history, data, and analysis
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'data' not in st.session_state:
    st.session_state.data = None

if 'ai_analysis' not in st.session_state:
    st.session_state.ai_analysis = None

# Streamlit layout
st.title('Financial Data Analysis Dashboard')
st.sidebar.header('Controls')

# Fetch stock symbols
stock_symbols = get_stock_symbols()

selected_option = st.sidebar.selectbox('Select Stock', stock_symbols)

date_range = st.sidebar.date_input('Select Date Range', [])

if st.sidebar.button('Get Data'):
    data = get_stock_data(selected_option, date_range)
    if not data.empty:
        data['Date'] = data['Date'].astype(str)  # Ensure Date is string for Streamlit
        st.session_state.data = data

        # Generate visualizations
        if st.session_state.data is not None:
            data = st.session_state.data

            # Generate summary text from visualizations
            visualization_summary = generate_visualization_summary(data)

            # Perform AI analysis on the visualizations
            st.session_state.ai_analysis = ask_vertex_ai(visualization_summary)
    else:
        st.error("No data found for the selected date range.")

# Display data if it exists in session state
if st.session_state.data is not None:
    data = st.session_state.data
    
    # Display data
    st.write('### Financial Data', data)
    
    # Detailed analysis
    st.write('### Data Analysis')
    st.write(data.describe())

    # Create plots with white theme
    st.write('### Visualizations')
    
    # Candlestick chart
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.02)
    fig.add_trace(go.Candlestick(x=data['Date'],
                                 open=data['Open'],
                                 high=data['High'],
                                 low=data['Low'],
                                 close=data['Close'],
                                 name='Candlestick'), row=1, col=1)
    fig.add_trace(go.Bar(x=data['Date'], y=data['Volume'], name='Volume'), row=2, col=1)
    fig.update_layout(title='Candlestick Chart and Volume', xaxis_title='Date', yaxis_title='Price', template='plotly_white')
    fig.update_xaxes(type='category', tickformat='%Y-%m-%d')
    st.plotly_chart(fig)

    # Line chart for closing price
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.set_style("whitegrid")
    sns.lineplot(data=data, x='Date', y='Close', ax=ax)
    ax.set_title('Closing Price Over Time')
    ax.set_xlabel('Date')
    ax.set_ylabel('Close Price')
    ax.xaxis.set_major_locator(plt.MaxNLocator(10))
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Bar chart for volume
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.set_style("whitegrid")
    sns.barplot(data=data, x='Date', y='Volume', ax=ax)
    ax.set_title('Trading Volume Over Time')
    ax.set_xlabel('Date')
    ax.set_ylabel('Volume')
    ax.xaxis.set_major_locator(plt.MaxNLocator(10))
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # AI Analysis after visualizations
    if st.session_state.ai_analysis:
        st.write('### AI Analysis')
        st.write(st.session_state.ai_analysis)
    
    # Chatbot interaction
    st.write('### Ask the AI Chatbot about the data!')
    user_input = st.text_input("Ask a question about the data:")
    if st.button('Submit'):
        if user_input and st.session_state.data is not None:
            chatbot_response = ask_vertex_ai(f"The user has provided the following data: {st.session_state.data.describe().to_json()}. The user asked: {user_input}")
            st.session_state.chat_history.append((user_input, chatbot_response))

    # Display chat history
    if st.session_state.chat_history:
        st.write('### Chatbot Conversation History')
        for question, response in st.session_state.chat_history:
            st.write(f"**User:** {question}")
            st.write(f"**Bot:** {response}")
else:
    st.write('Please generate data to enable AI chatbot interaction.')
