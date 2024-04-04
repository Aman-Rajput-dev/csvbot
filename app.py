import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from pandasai.llm.openai import OpenAI
from pandasai.llm import GooglePalm
from pandasai import SmartDataframe
from pandasai import Agent
from htmlTemplates import css, bot_template, user_template
from pandasai.connectors import BaseConnector
from pandasai.connectors import PandasConnector
from pandasai.skills import skill


load_dotenv()

openai_api_key = os.getenv('OPEN_API_KEY')
os.environ["PANDASAI_API_KEY"] = "$2a$10$tTzcQhKvPMZP/t0aKzYyR.lsKmUQLc.5syqZ/NuxG/fcU63UN63ge"
st.set_page_config(page_title="CSV-GPT",layout='wide',page_icon=":bar_chart:")

st.write(css,unsafe_allow_html=True)
card1 ='''
<style>
.card {
  /* Add shadows to create the "card" effect */
  box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
  transition: 0.3s;
    border-radius: 5px;
    height:200px;
    width:200px;
    background-color:#1e1f20;
    margin:20px;
}

/* On mouse-over, add a deeper shadow */
.card:hover {
  box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
    background-color:#2f3133    ;

}

/* Add some padding inside the card container */
.container {
  padding: 2px 16px;
}
.cunt{
display:flex;
flex-direction:row;
    justify-content:center;
}
</style>
<div class="cunt">
    <div class="card">
  
  <div class="container">
    <span style='font-size:50px;'>&#128187;</span>
    <h4><b>Step 1</b></h4>    
    <p>Upload the .csv file in the sidebar</p>
  </div>
</div>


<div class="card">
  
  <div class="container">
  <span style='font-size:50px;'>&#128070;</span>
    <h4><b>Step 2</b></h4>
    <p>Click on "Browse files" button and wait</p>
  </div>
</div>
<div class="card">
  
  <div class="container">
  <span style='font-size:50px;'>🔍</span>
    <h4><b>Step 3</b></h4>
    <p>Ask questions from the CSV file</p>
  </div>
</div>
</div>

'''

def chat_wtih_csv(df,prompt):
    llm =OpenAI()
    # llm = GooglePalm(api_key="AIzaSyD1QZx_m_hjwxP1yBjEpyZH7Rw81XY_8e4")
    # pandas_ai = SmartDataframe(df=df,config={"llm":llm})
    # field_descriptions = {
    #     'timestamp':'This is the date and time provided, the time interval is 5min,the date and time is format MM-DD-YYYY HH.MM',
    #     'acc_gii_radiation':'This is the gii radiation ,the total amount of sunlight that reaches a surface',
    #     'ambient_temperature':'This is the surrounding temperature'
    # }

    #this is working 
    pandas_ai = Agent(dfs=df,memory_size=10,config={'llm':llm})
      
    #this is working
#     pandas_ai.train(docs="The data of January month is from row 2 to row 7489")
#     pandas_ai.train(docs="the total record for february month is 8351 rows")
    
#     query = "Give me a visual representation on ambient temperature of january month"
#     response= '''
#     df = dfs[0]
    
# '''
    # pandas_ai.train(queries=[query],codes=[response])
    

    result = pandas_ai.chat(prompt)
    print(result)
    
    return result


st.markdown("<h1 style='text-align: center; color: white;'>Chat to CSV powered by LLM</h1>", unsafe_allow_html=True)

# st.title("")
with st.sidebar:
    st.header("Upload the .csv file here",divider="rainbow")
    input_csv = st.file_uploader("Upload your CSV file",type=['csv'])


if input_csv is not None:
    col1,col2 =st.columns([1,1])
    with col1:
      st.success("CSV Uploaded Successfully")
      data = pd.read_csv(input_csv)
      st.dataframe(data)
      


    with col2:
        st.info("Chat with your CSV")
        input_text = st.text_area("Enter your query")
        if input_text is not None:
            if st.button("Chat with CSV"):
                st.write(user_template.replace(
                "{{MSG}}", input_text), unsafe_allow_html=True)
                
                # st.info("Your query: "+input_text)
                
                result = chat_wtih_csv(data,input_text)
                # st.write(bot_template.replace(
                # "{{MSG}}", result), unsafe_allow_html=True)
                # st.success(result)
                # result_df = pd.DataFrame(list(result), columns=['Column_Name'])
                if isinstance(result,pd.DataFrame):
                    st.dataframe(result)
                else:
                    st.success(result)
                print(type(result))
                # st.dataframe(result_df)
      
else:
    st.markdown(card1, unsafe_allow_html=True)
                

