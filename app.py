# Suppress all warnings
import warnings
warnings.filterwarnings("ignore")

# Importing the necessary libraries
import streamlit as st                  # For loading the Streamlit Application and its associated components
from langchain_cohere import ChatCohere # For creating a Cohere LLM instance
from dotenv import load_dotenv          # For loading relevant keys from the .env file
import os                               # For OS loading operations
import pandas as pd                     # For loading and processing the CSVs
from pandasai import SmartDataframe     # For high-level operations on our CSVs - This is the backbone of our script.
import seaborn as sns                   # For creating heatmaps, if required
import numpy as np                      # For several miscelleneous operations
import matplotlib                       # Plotting Library
# matplotlib.use('TkAgg')                 # Ensuring Matplotlib uses Agg rendering to a Tkinter canvas as a backend
matplotlib.use('Agg')                   # Ensuring Matplotlib uses Anti-Grain Geometry (AGG) renderer as a backend
import matplotlib.pyplot as plt         # Plotting Library
import chardet                          # For checking the encoding of the input file 
from get_recs import get_graph_recs     # Importing function for generating list of possible graphs

# Function to check and handle CSV encoding dynamically and check for column names
def load_csv(file):
    
    try:
        rawdata = file.read()
        result = chardet.detect(rawdata)
        encoding = result['encoding']
        file.seek(0)  # Reset file pointer to the beginning

        # Load the CSV with detected encoding
        df = pd.read_csv(file, encoding=encoding)
        
        # Check if columns are unnamed
        if df.columns.str.contains('Unnamed').any():
            # Assign arbitrary names only to unnamed columns
            df.columns = [col if not col.startswith('Unnamed') else f'Column{idx}' for idx, col in enumerate(df.columns)]
        
        return df
    
    except Exception as e:
        st.error(f"Error loading CSV file: {e}")
        return st.error("Failed to load CSV file. Please check the file encoding.")
    
# Loading the Cohere API key into the environment
load_dotenv()
os.environ["COHERE_API_KEY"] = os.getenv("COHERE_KEY")

# Creating a Cohere LLM Instance
cohere_llm = ChatCohere(model="command-r-plus",  # Using the latest model from Cohere
                        temperature=0.3,)        # Setting the temperature to a low value to avoid entropy and randomness in outputs

# Function to build LLM and Chat With Multiple CSV Files
def chat_with_csv(df, prompt):

    pandas_ai = SmartDataframe(df, config={"llm": cohere_llm})
    
    try:
        # Clear any existing plots
        plt.clf()
        plt.close('all')
        
        result = pandas_ai.chat(prompt)

        # Check if the result is a string containing "correlation matrix" or "heatmap"
        if isinstance(result, str) and ("correlation matrix" in result.lower() or "heatmap" in result.lower()):
            # Create correlation matrix
            corr = df.select_dtypes(include=[np.number]).corr()
            
            # Generate heatmap
            plt.figure(figsize=(10, 8))
            sns.heatmap(corr, annot=True, cmap='coolwarm', linewidths=0.5)
            plt.title("Correlation Matrix of Numerical Variables")
            return plt.gcf()
        
        # Check if a plot was generated
        elif plt.get_fignums():

            # If a plot exists, return it
            return plt.gcf()
        
        else:
            # If no plot, return the text result
            return result
    
    except Exception as e:
        st.error(f"Error during chat execution: {e}")
        return None

# Setting up the page UI
st.set_page_config(layout='wide')
st.title("InsightAI")
st.markdown('<style>h1{color: #154860; text-align: center;}</style>', unsafe_allow_html=True)
st.subheader('Bring your CSVs to life!')
st.markdown('<style>h3{color: #ff6b3d;  text-align: center;}</style>', unsafe_allow_html=True)

# Including a sidebar as an upload menu 
input_csvs = st.sidebar.file_uploader("Upload your CSV files", 
                                      type=['csv'],               # Accepting only 'csv' type files.
                                      accept_multiple_files=True) # Also giving the users a choice to upload multiple CSV files at once

# Activating the main menu if a file is uploaded
if input_csvs:

    # Select a CSV file from the uploaded files (if multiple uploaded) using a dropdown menu
    selected_file = st.selectbox("Select a CSV file", [file.name for file in input_csvs])
    selected_index = [file.name for file in input_csvs].index(selected_file)

    # Load and display the selected csv file 
    st.info("CSV uploaded successfully")
    
    data = load_csv(input_csvs[selected_index]) 

    # Displaying the entire dataframe on the app, for ease of reference
    st.dataframe(data, use_container_width=True)

    # Create a key for the current CSV in the session state
    csv_key = f"recs_list_{selected_file}"

    with st.spinner("Generating custom recommendations for your data..."):

        # Generate recommendations if they don't exist for this CSV
        if csv_key not in st.session_state:

            recs_list = get_graph_recs(data, cohere_llm)          # Fetching a list of possible graphs for the given data
            recs_list.append("Enter your own...")                 # Adding an option for custom input
            recs_list.insert(0, "Select your graph")              # Adding a default state at the beginning of the list
            
            st.session_state[csv_key] = recs_list
        
        # Use the recommendations for the current CSV
        recs_list = st.session_state[csv_key]

        # Reset the selected option when switching CSVs
        if 'current_csv' not in st.session_state or st.session_state.current_csv != selected_file:
            
            st.session_state.selected_option = recs_list[0]
            st.session_state.current_csv = selected_file

    # Enter the query for analysis
    st.info("Chat Below")

    # Dropdown menu for selecting query
    selected_option = st.selectbox("Select a query", recs_list, index=recs_list.index(st.session_state.selected_option))

    # Update session state based on the selected option
    st.session_state.selected_option = selected_option

    # If the selected option is "Enter your own...", show a text box for custom input
    if selected_option == "Enter your own...":
        input_text = st.text_area("Enter the query", key="custom_query")
    
    # If anything else is selected, it is directly passed as an input - except if it is a default state
    elif selected_option != recs_list[0]:
        input_text = selected_option
    
    # If the submit button gets clicked with no selection, the input string remains empty
    else:
        input_text = ""

    # Perform analysis
    if st.button("Chat with csv"):
        
        if input_text:

            st.info("Your Query: " + input_text)

            with st.spinner("Generating your graph..."):
                result = chat_with_csv(data, "Plot the following graph: " + input_text)

                if isinstance(result, plt.Figure):
                    fig_to_plot = result
                    st.pyplot(fig=fig_to_plot)

                elif result is not None:
                    st.success(result)
                    
                else:
                    st.error("Failed to generate a response.")
