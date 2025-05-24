import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
from utils import PreprocessTxTFile, Helper

st.sidebar.title("WhatsApp Chat Analyzer")

# Upload section
uploaded_file = st.sidebar.file_uploader("Choose a file", type="txt")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    chat_data = data.splitlines()

    df = PreprocessTxTFile(chat_data).preprocess()
    # st.dataframe(df)

    # User selection
    user_list = df["User"].unique().tolist()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("Show analysis with respect to", user_list)

    if st.sidebar.button("Show Analysis"):
        # Top Stats
        num_messages, words, num_media_message, links = Helper.fetch_stats(selected_user, df)

        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(len(words))
        with col3:
            st.header("Media Shared")
            st.title(num_media_message)
        with col4:
            st.header("Links Shared")
            st.title(len(links))

        # Monthly timeline
        st.title("Monthly Timeline")
        fig, ax = plt.subplots()
        timeline = Helper.monthly_timeline(selected_user, df)
        ax.plot(timeline["time"], timeline["message"], color="green")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Daily timeline
        st.title("Daily Timeline")
        daily = Helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily["only_date"], daily["message"])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Activity maps
        st.title("Activity Map")
        col1, col2 = st.columns(2)
        with col1:
            st.header("Most Busy Day")
            busy_day = Helper.activity_map_for_everyday(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header("Most Busy Month")
            busy_month = Helper.activity_map_for_month(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color="orange")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # Heatmap
        st.title("Weekly Activity Heatmap")
        heatmap = Helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        sns.heatmap(heatmap, ax=ax)
        st.pyplot(fig)

        # Most active users (group-level)
        if selected_user == "Overall":
            st.title("Most Active Users")
            x, user_percent = Helper.fecth_most_busy_users(df)
            col1, col2 = st.columns(2)
            with col1:
                fig, ax = plt.subplots()
                ax.bar(x.index, x.values, color="red")
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(user_percent)

        # Wordcloud
        st.title("Wordcloud")
        wc = Helper.create_wordcld(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(wc)
        ax.axis("off")
        st.pyplot(fig)

        # Most common words
        
        common_words = Helper.most_common_words(selected_user, df)
        if not common_words.empty:
            st.title("Most Common Words")
            fig, ax = plt.subplots()
            ax.barh(common_words[0], common_words[1])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
            

        # Emoji analysis
        # st.title("Emoji Analysis")
        # emoji_df = Helper.emoji_helper(selected_user, df)
        # col1, col2 = st.columns(2)
        # with col1:
        #     st.dataframe(emoji_df)
        # with col2:
        #     if not emoji_df.empty:
        #         fig, ax = plt.subplots()
        #         ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
        #         st.pyplot(fig)
        #     else:
        #         st.write("No emojis found.")
        
        st.title("Emoji Analysis")
        emoji_df = Helper.emoji_helper(selected_user, df)

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:
            if not emoji_df.empty:
                # Use emoji-compatible font from helper
                emoji_font = Helper.get_emoji_font()

                fig, ax = plt.subplots()
                wedges, texts, autotexts = ax.pie(
                    emoji_df[1].head(),
                    labels=emoji_df[0].head(),
                    autopct="%0.2f"
                )

                # Apply emoji font to pie labels and percentages
                if emoji_font:
                    for text in texts + autotexts:
                        text.set_fontproperties(emoji_font)

                st.pyplot(fig)
            else:
                st.write("No emojis found.")