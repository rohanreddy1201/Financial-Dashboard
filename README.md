# Financial Data Analysis Dashboard

## Introduction

The Financial Data Analysis Dashboard is a comprehensive tool designed to provide users with insightful visualizations and analyses of stock market data. Built using Streamlit and Vertex AI, this dashboard allows users to fetch financial data, visualize it through various interactive plots, and interact with an AI chatbot for detailed insights and predictions.

## Project Outline

### Features
- **Fetch Stock Data**: Retrieve and display stock data for various companies.
- **Visualize Data**: Generate interactive visualizations including candlestick, line, and bar charts.
- **AI Analysis**: Utilize Vertex AI to generate summaries and predictions based on the financial data.
- **AI Chatbot**: Interact with an AI chatbot to ask questions and get insights about the data.

### Technologies Used
- **Streamlit**: For building the web application.
- **Vertex AI**: For AI-driven analysis and chatbot functionalities.
- **Plotly**: For creating interactive visualizations.
- **Seaborn**: For generating descriptive statistical plots.
- **Pandas**: For data manipulation and analysis.
- **Google Cloud Platform**: For hosting the AI models and handling authentication.

### Working
1. **Data Fetching**: Users can select a stock symbol and a date range from the sidebar. Upon clicking "Get Data", the application fetches the relevant financial data using the Alpha Vantage API.
2. **Data Visualization**: The fetched data is displayed in various interactive visualizations:
    - **Candlestick Chart**: Shows the opening, closing, high, and low prices of the stock.
    - **Line Chart**: Displays the closing price over time.
    - **Bar Chart**: Illustrates the trading volume over time.
3. **AI Analysis**: After generating the visualizations, the application provides a summary and analysis of the data using Vertex AI. This analysis is displayed below the visualizations.
4. **AI Chatbot Interaction**: Users can ask questions about the data to the AI chatbot, which uses Vertex AI to generate responses based on the provided data.

## Dependencies

- Python 3.x
- Streamlit
- pandas
- matplotlib
- seaborn
- plotly
- google-auth
- vertexai
- vaderSentiment
- requests

### Setup Instructions

1. **Clone the Repository**
    ```sh
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2. **Install Dependencies**
    ```sh
    pip install -r streamlit_app/requirements.txt
    ```

3. **Google Cloud Platform Setup**
    - Create a GCP Project.
    - Enable Vertex AI API.
    - Create a Service Account with necessary permissions and download the JSON key file.
    - Store credentials in `.streamlit/secrets.toml`.

4. **Run the App Locally**
    ```sh
    streamlit run streamlit_app/app.py
    ```

## Deploy to Streamlit Sharing

1. **Push the Project to GitHub**: Ensure your repository is public or authorized with Streamlit Sharing.
2. **Deploy on Streamlit Sharing**: Follow the Streamlit Sharing deployment guide to deploy your app.

## License
This project is licensed under the MIT License - see the LICENSE.md file for details.
