# Email Thread Data Pipeline

An end-to-end data engineering pipeline that ingests raw email data, cleans and reconstructs email threads, and produces a final dataset ready for downstream NLP tasks such as **email thread summarization**.

---

## Project Objective

To design and implement a **single, clear data pipeline** that transforms raw email-level data into **thread-level structured text**, aligned with human-written summaries.

This project focuses on:
- Data ingestion
- Data cleaning
- Thread reconstruction
- Dataset merging
- Final pipeline output generation

---

## 📂 Dataset Used

**Email Thread Summary Dataset**  
Source: Kaggle  
Link: https://www.kaggle.com/datasets/marawanxmamdouh/email-thread-summary-dataset

### Files:
- `email_thread_details.csv`  
  Contains individual emails with metadata (thread_id, sender, timestamp, body, etc.)
- `email_thread_summaries.csv`  
  Contains one human-written summary per email thread

---

## Pipeline Architecture

```
Raw Email CSVs
      ↓
Data Ingestion
      ↓
Timestamp Parsing
      ↓
Email Body Cleaning
      ↓
Thread Reconstruction
      ↓
Merge with Summaries
      ↓
Final Thread-Level Dataset
```

---

## Pipeline Steps

### Step 1: Data Ingestion
- Load raw CSV files using pandas
- Validate schema and row counts

### Step 2: Timestamp Parsing
- Convert timestamp strings to datetime
- Handle invalid or malformed timestamps safely

### Step 3: Email Body Cleaning
- Remove forwarded/replied email chains
- Normalize whitespace and formatting
- Handle missing or empty email bodies

### Step 4: Thread Reconstruction
- Group emails by `thread_id`
- Sort emails chronologically within each thread
- Concatenate cleaned email bodies into a single thread text

### Step 5: Merge & Final Output
- Merge reconstructed threads with human summaries
- Remove empty or invalid threads
- Save final dataset to CSV

---

## Final Output

**File:** `final_email_thread_dataset.csv`

**Columns:**
- `thread_id` – Unique identifier for each email thread
- `thread_text` – Reconstructed full email conversation
- `summary` – Human-written summary of the thread

**Final Shape:**
- Total threads: **4140**
- One row per email thread

---

## Quality Checks Performed

- Null timestamp validation
- Empty email body detection
- Emails per thread statistics
- Empty reconstructed thread filtering
- One-to-one alignment between threads and summaries

---

##  Project Structure

```
EMAIL PIPELINE/
│── main.py
│── README.md
│── .gitignore
│── email_thread_details.csv      (ignored in git)
│── email_thread_summaries.csv    (ignored in git)
│── final_email_thread_dataset.csv
```

---

## How to Run

1. Clone the repository
2. Place dataset CSV files in the project directory
3. Run:

```bash
python main.py
```

4. Final output will be generated as:

```
final_email_thread_dataset.csv
```

---

## Technologies Used

- Python
- Pandas
- Git & GitHub

---

## Notes

- Large CSV files are excluded from GitHub using `.gitignore`
- This repository focuses on **data pipeline construction**, not model training
- Output dataset is ready for summarization or NLP modeling

---

## License

This project is for academic and learning purposes.
<!-- Submission PR for review -->
