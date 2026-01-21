import pandas as pd


def clean_email_body(text):
    if pd.isna(text):
        return ""
    text = text.split("-----Original Message-----")[0]
    text = text.replace("\r\n", "\n")
    text = " ".join(text.split())
    return text



DETAILS_PATH = "email_thread_details.csv"
SUMMARIES_PATH = "email_thread_summaries.csv"

details_df = pd.read_csv(DETAILS_PATH)
summaries_df = pd.read_csv(SUMMARIES_PATH)


details_df['timestamp'] = pd.to_datetime(
    details_df['timestamp'],
    dayfirst=True,
    errors='coerce'
)

print("Invalid timestamps:", details_df['timestamp'].isna().sum())



details_df['clean_body'] = details_df['body'].apply(clean_email_body)

print("Empty clean bodies:", (details_df['clean_body'] == "").sum())



def build_thread_text(group):
    """
    Takes all emails of a thread (already grouped),
    sorts by timestamp, removes empty bodies,
    and concatenates them into one thread text.
    """
    group = group.sort_values("timestamp")

    texts = [
        text for text in group["clean_body"]
        if isinstance(text, str) and text.strip() != ""
    ]

    return "\n\n".join(texts)


threads_df = (
    details_df
    .groupby("thread_id")
    .apply(build_thread_text)
    .reset_index(name="thread_text")
)

print("Reconstructed threads:", threads_df.shape[0])


empty_threads = (threads_df["thread_text"] == "").sum()
print("Empty reconstructed threads:", empty_threads)


print("\nSample reconstructed thread:\n")
print(threads_df.loc[0, "thread_text"][:800])




emails_per_thread = details_df.groupby('thread_id').size()

print("Min emails per thread:", emails_per_thread.min())
print("Max emails per thread:", emails_per_thread.max())
print("Avg emails per thread:", round(emails_per_thread.mean(), 2))



sample_thread_id = details_df['thread_id'].iloc[0]
sample_thread = details_df[details_df['thread_id'] == sample_thread_id] \
                    .sort_values('timestamp')

print("\nSample thread_id:", sample_thread_id)
print(sample_thread[['timestamp', 'from', 'subject']].head())

print("\nSample BEFORE cleaning:\n")
print(sample_thread['body'].iloc[0][:300])

print("\nSample AFTER cleaning:\n")
print(sample_thread['clean_body'].iloc[0][:300])




final_df = threads_df.merge(
    summaries_df,
    on="thread_id",
    how="inner"
)

print("Final dataset shape:", final_df.shape)


final_df = final_df[final_df["thread_text"].str.strip() != ""]

print("Final dataset after removing empty threads:", final_df.shape)


final_df = final_df[["thread_id", "thread_text", "summary"]]


OUTPUT_PATH = "final_email_thread_dataset.csv"
final_df.to_csv(OUTPUT_PATH, index=False)

print(f"\nFinal pipeline output saved to: {OUTPUT_PATH}")


print("\nSample final row:\n")
print(final_df.iloc[0])
