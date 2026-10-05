import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime

from utils.analyzer import analyze_complaint
from utils.models import Complaint


# ============================================================
# CONFIGURATION
# ============================================================

DATA_FILE = Path("data/complaints.csv")

st.set_page_config(
    page_title="Campus Complaint Analyzer",
    page_icon="🎓",
    layout="wide"
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def load_complaints():
    """Load complaints from CSV file."""

    if DATA_FILE.exists():
        try:
            return pd.read_csv(DATA_FILE)
        except Exception:
            pass

    return pd.DataFrame(
        columns=[
            "id",
            "name",
            "email",
            "category",
            "complaint",
            "priority",
            "sentiment",
            "status",
            "timestamp"
        ]
    )


def save_complaint(complaint_data):
    """Save a complaint to the CSV file."""

    DATA_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df = load_complaints()

    if df.empty:
        new_id = 1
    else:
        new_id = int(df["id"].max()) + 1

    complaint_data["id"] = new_id

    complaint_data["timestamp"] = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    complaint_data["status"] = "Pending"

    new_row = pd.DataFrame([complaint_data])

    df = pd.concat(
        [df, new_row],
        ignore_index=True
    )

    df.to_csv(
        DATA_FILE,
        index=False
    )


# ============================================================
# LOAD DATA
# ============================================================

complaints_df = load_complaints()


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

st.sidebar.title("🎓 Campus Complaint Analyzer")

st.sidebar.write(
    "Complaint Management System"
)

page = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Submit Complaint",
        "Dashboard",
        "Complaints"
    ]
)


# ============================================================
# HOME PAGE
# ============================================================

if page == "Home":

    st.title("🎓 Campus Complaint Analyzer")

    st.subheader(
        "Smart campus complaint management system"
    )

    st.write(
        "Submit, analyze and monitor student complaints "
        "using an automated complaint analysis system."
    )

    st.divider()

    # -------------------------
    # Statistics
    # -------------------------

    total = len(complaints_df)

    if not complaints_df.empty:

        pending = len(
            complaints_df[
                complaints_df["status"] == "Pending"
            ]
        )

        high_priority = len(
            complaints_df[
                complaints_df["priority"] == "High"
            ]
        )

        negative = len(
            complaints_df[
                complaints_df["sentiment"] == "Negative"
            ]
        )

    else:
        pending = 0
        high_priority = 0
        negative = 0

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Complaints",
            total
        )

    with col2:
        st.metric(
            "Pending",
            pending
        )

    with col3:
        st.metric(
            "High Priority",
            high_priority
        )

    with col4:
        st.metric(
            "Negative",
            negative
        )

    st.divider()

    st.info(
        "Use the 'Submit Complaint' option from the "
        "sidebar to submit a new complaint."
    )


# ============================================================
# SUBMIT COMPLAINT PAGE
# ============================================================

elif page == "Submit Complaint":

    st.title("📝 Submit a Complaint")

    st.write(
        "Enter the student's details and describe the issue."
    )

    st.divider()

    name = st.text_input(
        "Student Name",
        placeholder="Enter your name"
    )

    email = st.text_input(
        "Email",
        placeholder="Enter your email"
    )

    complaint_text = st.text_area(
        "Describe Your Complaint",
        placeholder="Describe the problem in detail...",
        height=180
    )

    submit = st.button(
        "🚀 Submit Complaint"
    )

    if submit:

        if not name or not email or not complaint_text:

            st.warning(
                "Please fill in all the fields."
            )

        else:

            # Analyze complaint
            analysis = analyze_complaint(
                complaint_text
            )

            # Create complaint object
            complaint = Complaint(
                name=name,
                email=email,
                category=analysis["category"],
                complaint=complaint_text,
                priority=analysis["priority"],
                sentiment=analysis["sentiment"]
            )

            # Save complaint
            save_complaint(
                complaint.model_dump()
            )

            st.success(
                "🎉 Complaint submitted successfully!"
            )

            st.divider()

            st.header("Complaint Analysis")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Category",
                    analysis["category"]
                )

            with col2:
                st.metric(
                    "Priority",
                    analysis["priority"]
                )

            with col3:
                st.metric(
                    "Sentiment",
                    analysis["sentiment"]
                )

            st.info(
                "Your complaint has been recorded "
                "in the complaint database."
            )


# ============================================================
# DASHBOARD PAGE
# ============================================================

elif page == "Dashboard":

    st.title("📊 Complaint Dashboard")

    st.write(
        "Monitor complaint statistics and trends."
    )

    st.divider()

    if complaints_df.empty:

        st.info(
            "No complaints available yet."
        )

    else:

        # -------------------------
        # Statistics
        # -------------------------

        total = len(complaints_df)

        pending = len(
            complaints_df[
                complaints_df["status"] == "Pending"
            ]
        )

        high_priority = len(
            complaints_df[
                complaints_df["priority"] == "High"
            ]
        )

        negative = len(
            complaints_df[
                complaints_df["sentiment"] == "Negative"
            ]
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Total",
                total
            )

        with col2:
            st.metric(
                "Pending",
                pending
            )

        with col3:
            st.metric(
                "High Priority",
                high_priority
            )

        with col4:
            st.metric(
                "Negative",
                negative
            )

        st.divider()

        # -------------------------
        # Category Chart
        # -------------------------

        st.header("Complaints by Category")

        category_counts = (
            complaints_df["category"]
            .value_counts()
        )

        st.bar_chart(
            category_counts
        )

        st.divider()

        # -------------------------
        # Priority Chart
        # -------------------------

        st.header("Complaints by Priority")

        priority_counts = (
            complaints_df["priority"]
            .value_counts()
        )

        st.bar_chart(
            priority_counts
        )

        st.divider()

        # -------------------------
        # Sentiment Chart
        # -------------------------

        st.header("Complaints by Sentiment")

        sentiment_counts = (
            complaints_df["sentiment"]
            .value_counts()
        )

        st.bar_chart(
            sentiment_counts
        )


# ============================================================
# COMPLAINTS PAGE
# ============================================================

elif page == "Complaints":

    st.title("📋 All Complaints")

    st.write(
        "View and search all submitted complaints."
    )

    st.divider()

    if complaints_df.empty:

        st.info(
            "No complaints have been submitted yet."
        )

    else:

        # -------------------------
        # Search
        # -------------------------

        search = st.text_input(
            "🔍 Search Complaints",
            placeholder="Search by name, email, category, complaint..."
        )

        filtered_df = complaints_df.copy()

        if search:

            search_lower = search.lower()

            filtered_df = filtered_df[
                filtered_df.astype(str)
                .apply(
                    lambda row:
                    row.str.lower()
                    .str.contains(
                        search_lower,
                        na=False
                    )
                    .any(),
                    axis=1
                )
            ]

        # -------------------------
        # Display table
        # -------------------------

        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True
        )