def analyze_complaint(complaint):
    """
    Analyze a campus complaint and return
    category, priority, and sentiment.
    """

    text = complaint.lower()

    # -----------------------------
    # Category Detection
    # -----------------------------

    if any(word in text for word in [
        "food",
        "canteen",
        "mess",
        "meal"
    ]):
        category = "Food"

    elif any(word in text for word in [
        "hostel",
        "room",
        "water",
        "bathroom",
        "toilet"
    ]):
        category = "Hostel"

    elif any(word in text for word in [
        "wifi",
        "internet",
        "network"
    ]):
        category = "Internet"

    elif any(word in text for word in [
        "class",
        "teacher",
        "faculty",
        "lecture"
    ]):
        category = "Academics"

    elif any(word in text for word in [
        "library",
        "book"
    ]):
        category = "Library"

    elif any(word in text for word in [
        "lab",
        "computer",
        "equipment"
    ]):
        category = "Laboratory"

    else:
        category = "Other"


    # -----------------------------
    # Priority Detection
    # -----------------------------

    if any(word in text for word in [
        "urgent",
        "emergency",
        "danger",
        "immediately",
        "critical"
    ]):
        priority = "High"

    elif any(word in text for word in [
        "problem",
        "issue",
        "not working",
        "broken"
    ]):
        priority = "Medium"

    else:
        priority = "Low"


    # -----------------------------
    # Sentiment Detection
    # -----------------------------

    negative_words = [
        "bad",
        "worst",
        "terrible",
        "angry",
        "poor",
        "unhappy",
        "disappointed",
        "dirty",
        "problem",
        "issue"
    ]

    positive_words = [
        "good",
        "great",
        "excellent",
        "happy",
        "thank",
        "thanks"
    ]

    negative_count = sum(
        word in text
        for word in negative_words
    )

    positive_count = sum(
        word in text
        for word in positive_words
    )

    if negative_count > positive_count:
        sentiment = "Negative"

    elif positive_count > negative_count:
        sentiment = "Positive"

    else:
        sentiment = "Neutral"


    return {
        "category": category,
        "priority": priority,
        "sentiment": sentiment
    }