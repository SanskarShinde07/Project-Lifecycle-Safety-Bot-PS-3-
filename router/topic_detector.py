from csv_engine.query_engine import get_all_topics

topics = get_all_topics()

def detect_topic(question):

    q = question.lower()

    for topic in topics:

        topic_lower = topic.lower()

        if topic_lower in q:
            return topic

        # handle & vs and
        if topic_lower.replace("&", "and") in q:
            return topic

    return None