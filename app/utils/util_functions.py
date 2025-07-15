def format_string(val: str, acronyms=None):
    if acronyms is None:
        acronyms = {"UPI", "ATM", "EMI", "GST", "NEFT", "RTGS", "IMPS"}

    words = val.strip().split()
    formatted_words = [
        word.upper() if word.upper() in acronyms else word.capitalize()
        for word in words
    ]
    return " ".join(formatted_words)
