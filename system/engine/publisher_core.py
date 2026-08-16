import re
import os

def validate_x_tweet(text):
    """
    Validates X.com tweet.
    Returns (is_valid, list_of_tweets)
    """
    text = text.strip()
    if len(text) <= 280:
        return True, [text]
    
    # Needs threading. Check if it's already a thread.
    if re.search(r'^\d+/\d*[:]*\s', text, re.MULTILINE):
        # Already threaded. Validate each part.
        parts = re.split(r'^\d+/\d*[:]*\s*', text, flags=re.MULTILINE)
        parts = [p.strip() for p in parts if p.strip()]
        for p in parts:
            if len(p) > 280:
                return False, parts
        return True, parts
    
    return False, [text]

def validate_linkedin_post(text):
    """
    Validates LinkedIn post.
    Returns (is_valid, validation_errors)
    """
    errors = []
    text = text.strip()
    if len(text) > 3000:
        errors.append(f"Exceeds 3000 characters (Current: {len(text)})")
    
    lines = text.split('\n')
    # Check if there is a hook in the first 3 lines (non-empty)
    content_lines = [l.strip() for l in lines if l.strip()]
    if not content_lines:
        errors.append("LinkedIn post is empty.")

    return len(errors) == 0, errors

def extract_drafts(markdown_content, post_identifier):
    """
    Extracts X and LinkedIn drafts for a specific post.
    """
    # Find the post section
    pattern = r'### ' + re.escape(post_identifier) + r'(.*?)(?=### Post \d+|$)'
    match = re.search(pattern, markdown_content, re.DOTALL | re.IGNORECASE)
    if not match:
        return None, None
    
    post_section = match.group(1)
    
    # Extract X.com draft
    x_pattern = r'\*\*\[X\.com.*?\]\*\*(.*?)(?=\-\-\-|\*\*\[LinkedIn)'
    x_match = re.search(x_pattern, post_section, re.DOTALL | re.IGNORECASE)
    x_draft = x_match.group(1).strip() if x_match else ""
    
    # Extract LinkedIn draft
    li_pattern = r'\*\*\[LinkedIn Post.*?\]\*\*(.*?)(?=</details>|<details>|$)'
    li_match = re.search(li_pattern, post_section, re.DOTALL | re.IGNORECASE)
    li_draft = li_match.group(1).strip() if li_match else ""
    
    return x_draft, li_draft
