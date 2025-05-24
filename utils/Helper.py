from collections import Counter
from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
import emoji
import os
import matplotlib.font_manager as fm

def fetch_stats(selected_user, df):
    if selected_user != "Overall":
        df = df[df["User"] == selected_user]

    num_messages = df.shape[0]

    words = []
    for message in df["message"]:
        words.extend(message.split())

    extractor = URLExtract()
    links = []
    for message in df["message"]:
        links.extend(extractor.find_urls(message))

    return num_messages, words, len(df[df['message'] == "<Media omitted>"]), links


def fecth_most_busy_users(df):
    x = df['User'].value_counts().head()
    percent_df = round((df['User'].value_counts() / df.shape[0]) * 100, 2).reset_index()
    percent_df.columns = ['Name', 'Percent']
    return x, percent_df


def create_wordcld(selected_user, df):
    if selected_user != "Overall":
        df = df[df["User"] == selected_user]

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color="black")
    df_wc = wc.generate(df["message"].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user, df):
    if selected_user != "Overall":
        df = df[df["User"] == selected_user]

    # temp = df[df['message'] != "<Media omitted>"]

    with open("hinglish_stopwords.txt", 'r') as f:
        stop_words = f.read().splitlines()

    words = []
    for mess in df["message"]:
        for word in mess.lower().split():
            if word not in stop_words and word not in {"(file", "attached)", ","}:
                words.append(word)

    return pd.DataFrame(Counter(words).most_common(20))


def emoji_helper(selected_user, df):
    if selected_user != "Overall":
        df = df[df["User"] == selected_user]

    emojis = []
    for msg in df["message"]:
        emojis.extend([c for c in msg if c in emoji.EMOJI_DATA])

    return pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))


def monthly_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df["User"] == selected_user]

    timeline = df.groupby(["Year", "month_num", "month"]).count()["message"].reset_index()
    timeline['time'] = timeline['month'] + "-" + timeline['Year'].astype(str)

    return timeline


def daily_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df["User"] == selected_user]

    daily = df.groupby("only_date").count()["message"].reset_index()
    return daily


def activity_map_for_everyday(selected_user, df):
    if selected_user != "Overall":
        df = df[df["User"] == selected_user]

    return df["day_name"].value_counts()


def activity_map_for_month(selected_user, df):
    if selected_user != "Overall":
        df = df[df["User"] == selected_user]

    return df["month"].value_counts()


def activity_heatmap(selected_user, df):
    if selected_user != "Overall":
        df = df[df['User'] == selected_user]

    # Create "period" column if not present (hour-wise slot)
    if 'period' not in df.columns:
        df['period'] = df['hour'].apply(lambda x: f"{x}-{x+1 if x < 23 else 0}")

    heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return heatmap



# Try to load an emoji-capable font
def get_emoji_font():
    if os.name == 'nt':
        return fm.FontProperties(family='Segoe UI Emoji')  # Windows
    else:
        # For Linux (Streamlit Cloud or WSL)
        for path in fm.findSystemFonts(fontpaths=None, fontext='ttf'):
            if "NotoColorEmoji" in path and path.endswith(".ttf"):
                try:
                    # Test if the font is valid
                    fm.FontProperties(fname=path).get_name()
                    return fm.FontProperties(fname=path)
                except Exception:
                    continue
        return None