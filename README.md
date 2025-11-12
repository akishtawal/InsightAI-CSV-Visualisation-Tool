<h1 align="center">💡 InsightAI</h1>
<p align="center">
Turning CSVs into insights — instantly, intelligently, and visually.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-%233776AB.svg?style=for-the-badge&logo=Python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Streamlit-%23FF0000.svg?style=for-the-badge&logo=Streamlit&logoColor=red&color=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas">
  <img src="https://img.shields.io/badge/Cohere-%234B0082.svg?style=for-the-badge&logo=cohere&logoColor=white" alt="Cohere">
  <img src="https://img.shields.io/badge/PandasAI-%2300C4CC.svg?style=for-the-badge&logoColor=white" alt="PandasAI">
</p>

---

## 🌍 Context

In our rapidly advancing technological world, the ability to comprehend and utilize data efficiently has become paramount. As data volume grows, finding methods to make it comprehensible becomes crucial. CSV (Comma Separated Values) files, a common format for datasets, contain structured data that professionals, especially Data Scientists, frequently use. Visualizing these relationships and distributions simplifies data analysis.  

**InsightAI** aims to automate the visualization of data from CSV files using **Generative AI models**. The end goal is to create an interactive application that takes CSVs as input and responds with various graphs based on the CSV's data, enhancing the data analysis process.

---

## ⚙️ Approach and Methodologies

1. **🧠 Model Selection**  
   - **Research**: A thorough search for suitable models that cater to the needs of visual data representation.  
   - **Testing and Feasibility**: Iterative testing of identified models to select the most appropriate one.

2. **🧩 Model Choices**  
   - [Pandas Dataframe Agent by Langchain](https://python.langchain.com/v0.2/docs/integrations/toolkits/pandas/)  
   - [LIDA by Microsoft](https://github.com/microsoft/lida)  
   - [PandasAI by Sinaptik-AI](https://github.com/Sinaptik-AI/pandas-ai)

3. **🏁 Final Model**  
   - **PandasAI**: Chosen for its seamless integration with the Pandas library, ease of use, and cost-effectiveness.  
   - **Cohere LLM**: Selected for backend integration due to its compatibility and efficiency.

4. **🧰 Implementation**
   - Leverage the **SmartDataframe** functionality of PandasAI to utilize the power of existing LLM models.  
   - Use **Cohere's 'command-r-plus' model** to automate analysis operations on the dataset.

---

## 🧭 High-Level Workflow

![High-Level Workflow](./InsightAI_Workflow.png)

---

## 🧱 Libraries and Tools Used

- **Streamlit** 🧩 — For building the web application interface.  
- **Pandas** 🐼 — For handling CSVs and data manipulation.  
- **PandasAI** 🤖 — For integrating LLM capabilities into data analysis.  
- **Cohere** 🧠 — For backend LLM processing and natural language analysis.  
- **Matplotlib** 📊 — For generating graphs and visual representations.  
- **dotenv** ⚙️ — For managing environment variables securely.

---

## 🚀 App Usage

To use and test the app, follow these steps:

1. **Activate the Virtual Environment**  
   - On Windows:  
     ```bash
     .\venv\Scripts\activate
     ```  
   - On macOS/Linux:  
     ```bash
     source venv/bin/activate
     ```

2. **Update API Keys**  
   - Open the `.env` file in the project directory and update the `COHERE_KEY` with your Cohere API key.  
   - ⚠️ *Note*: The application will not work unless the Cohere API key is correctly set in the `.env` file.

3. **Run the Application**  
   - Execute the following command:  
     ```bash
     streamlit run app.py
     ```

---

## 🌱 Scopes of Improvement

- ⚙️ **Enhanced Query Handling** — Improve handling of a wider variety of user queries.  
- 🎯 **Output Accuracy** — Minimize bias and improve precision in generated visualizations.  
- 🧾 **Documentation** — Strengthen documentation for better debugging and onboarding.  
- 🏗️ **Custom Solution Architecture** — Develop a bespoke architecture using LLMs and code interpreters for better control.  
- 🧮 **Integration with NLP Libraries** — Generate **word clouds** or insights from textual data.  
- 📊 **Integration with LIDA** — Incorporate Microsoft’s LIDA for more context-aware data visual recommendations.

---

## 💬 Thank You

<p align="center">
  🙏 Thank you for exploring <b>InsightAI</b>!  
</p>
<p align="center">
  This project represents a small-scale yet powerful implementation of modern Generative AI tools to simplify data visualization and analysis.  
</p>
<p align="center">
  <i>“Bridging data with understanding — one CSV at a time.”</i> ✨  
</p>
