Sales Analytics Dashboard (Python + Pandas + NumPy + Matplotlib + Streamlit)
A complete mini-project: a synthetic medium-sized sales dataset, a script answering
15 business questions, and an interactive Streamlit dashboard.
📁 Project Files
`sales_data.csv` — 3,000-row synthetic sales dataset (2023–2024)
`generate_data.py` — script that generated the dataset
`analysis_15_questions.py` — standalone script answering all 15 questions + saves charts to `/charts`
`app.py` — the Streamlit dashboard (interactive version of all 15 questions)
`requirements.txt` — dependencies
⚙️ How to Run Locally
```bash
# 1. Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Optional) Regenerate the dataset or re-run the standalone analysis
python generate_data.py
python analysis_15_questions.py

# 4. Launch the dashboard
streamlit run app.py
```
Streamlit will open automatically at `http://localhost:8501`.
🎥 For your LinkedIn post / demo video
Run `streamlit run app.py`, screen-record yourself walking through the filters
(region, category, date range) and each of the 15 sections.
Upload the video to LinkedIn (or YouTube and link it) alongside your project post.
Push this code to a public GitHub repo and link it in the post — recruiters love
seeing the repo alongside the video.
📊 The 15 Questions Answered
What are the total net sales and average order value?
Which region generates the most sales?
Which product category generates the most sales?
What are the top 10 best-selling products?
What does the monthly sales trend look like?
What is the average profit margin?
Which category is most profitable?
Is there a correlation between discount % and quantity sold?
How much does each customer segment (New/Returning/VIP) contribute to sales?
Which payment methods are most popular?
How do sales reps compare in performance?
Which days of the week drive the most sales?
How does customer rating relate to average order value?
Which customer age group spends the most?
How many outlier (unusually high/low) orders exist, using the IQR method?
🛠️ Tech Stack
pandas — data loading, grouping, aggregation
numpy — percentile/IQR outlier detection, binning
matplotlib — custom charts embedded in the dashboard
streamlit — interactive web app with sidebar filters, KPIs, and charts
