import streamlit as st
import pandas as pd

# 1. Setup Page Config
st.set_page_config(page_title="Wrestling Leaderboard", layout="wide")
st.title("🤼 Season Points Leaderboard")

# 2. Load Data
# Replace 'your_file.csv' with the actual filename
@st.cache_data
def load_data():
    df = pd.read_csv("wrestlers_points.csv")
    # Combine names for easier searching
    df['Full Name'] = df['First Name'] + " " + df['Last Name']
    return df

df = load_data()

# 3. Sidebar Filters
st.sidebar.header("Filters")
division_list = ["All"] + sorted(df['Division'].unique().tolist())
selected_division = st.sidebar.selectbox("Select Division", division_list)

# 4. Search Functionality
search_query = st.text_input("🔍 Search for a Wrestler by Name:", "")

# 5. Data Processing (Totaling Points)
# We group by wrestler to show their cumulative season points
leaderboard = df.groupby(['Full Name', 'Division', 'Team Name', 'Weight'])['points'].sum().reset_index()
leaderboard = leaderboard.sort_values(by='points', ascending=False)

# Apply filters
if selected_division != "All":
    leaderboard = leaderboard[leaderboard['Division'] == selected_division]

if search_query:
    leaderboard = leaderboard[leaderboard['Full Name'].str.contains(search_query, case=False)]

# 6. Display Results
st.subheader(f"Rankings: {selected_division if selected_division != 'All' else 'All Divisions'}")

# Styling the table
st.dataframe(
    leaderboard,
    column_config={
        "points": st.column_config.NumberColumn("Total Points", format="%d pts"),
    },
    hide_index=True,
    use_container_width=True
)

if leaderboard.empty:
    st.warning("No wrestlers found matching those criteria.")