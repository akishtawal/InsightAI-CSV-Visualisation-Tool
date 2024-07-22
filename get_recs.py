#Importing all the libraries
from prompts import PLOT_RECO_ALT_PROMPT # Fetching the prompt
import ast                               # For converting string list to Python list
from io import StringIO                  # To capture the output of df.info (stdout by default) as a string

# Function for generating and loading a Python list of recommended graphs based on the input CSV's data.
def get_graph_recs(user_df, llm):

  # Defining an empty list to store API Messages
  llm_messages = []

  # Loading PlotReco's prompt as the system prompt
  llm_messages.append(("system", PLOT_RECO_ALT_PROMPT))

  # Extracting the required data and metadata from the DF
  
  # Getting a random sample of 10 rows from the dataframe
  df_sample = user_df.sample(n=min(10, len(user_df)), random_state=42).reset_index(drop=True)
  df_head = df_sample.to_string(index=False)

  # Getting the dataframe description
  df_desc = user_df.describe().to_string()

  # Getting the dataframe information
  buffer = StringIO()
  user_df.info(buf=buffer)
  df_info = buffer.getvalue()
  
  # Merging all extracted into one common string
  df_str = (
      "1. First 10 rows of the dataframe (df.head(10)):\n'''\n"
      f"{df_head}\n'''\n\n"
      "2. DataFrame description (df.describe()):\n'''\n"
      f"{df_desc}\n'''\n\n"
      "3. DataFrame info (df.info()):\n'''\n"
      f"{df_info}\n'''"
  )


  # Providing the combined information of the dataset (in string format) as the user/human input
  llm_messages.append(("human", df_str)) 

  # Getting the output from the LLM
  llm_response = llm.invoke(llm_messages)

  # Loading the response
  llm_response_clean = llm_response.content

  try:
    # Since this response is in a string format, we will have to load it as a Python list
    graph_rec_list = ast.literal_eval(llm_response_clean)
    return graph_rec_list
  
  except Exception as e:
    print("Conversion from String to Python List FAILED!")
    print("Details:\n", e)
    return None