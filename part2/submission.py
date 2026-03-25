import os
import re
from huggingface_hub import get_token

def your_netid():
    return 'xw3763'

def your_hf_token():
    return get_token() or os.getenv('HF_TOKEN') or os.getenv('HUGGINGFACE_HUB_TOKEN') or 'YOUR_HF_TOKEN'


# for adding small numbers (1-6 digits) and large numbers (7 digits), write prompt prefix and prompt suffix separately.
def your_prompt():
    """Returns a prompt to add to "[PREFIX]a+b[SUFFIX]", where a,b are integers
    Returns:
        A string.
    Example: a=1111, b=2222, prefix='Input: ', suffix='\nOutput: '
    """
    prefix = (
        'Question: What is 1,234,567 + 7,654,321?\n'
        'Answer: 8,888,888\n'
        'Question: What is 9,090,909 + 1,010,101?\n'
        'Answer: 10,101,010\n'
        'Question: What is 5,000,000 + 5,000,000?\n'
        'Answer: 10,000,000\n'
        'Question: What is 9,999,999 + 1,000,000?\n'
        'Answer: 10,999,999\n'
        'Question: What is '
    )

    suffix = '?\nAnswer: '

    return prefix, suffix


def your_config():
    """Returns a config for prompting api
    Returns:
        For both short/medium, long: a dictionary with fixed string keys.
    Note:
        do not add additional keys. 
        The autograder will check whether additional keys are present.
        Adding additional keys will result in error.
    """
    config = {
        'max_tokens': 50, # max_tokens must be >= 50 because we don't always have prior on output length 
        'temperature': 0.7,
        'top_k': 50,
        'top_p': 0.7,
        'repetition_penalty': 1.0,
        'stop': []}
    
    return config


def your_pre_processing(s):
    left, right = [part.strip() for part in s.split('+', 1)]
    return ' + '.join((f'{int(left):,}', f'{int(right):,}'))

    
def your_post_processing(output_string):
    """Returns the post processing function to extract the answer for addition
    Returns:
        For: the function returns extracted result
    Note:
        do not attempt to "hack" the post processing function
        by extracting the two given numbers and adding them.
        the autograder will check whether the post processing function contains arithmetic additiona and the graders might also manually check.
    """
    cleaned = output_string.replace(',', '').strip()
    candidates = [cleaned.splitlines()[0]] if cleaned else []
    candidates.append(cleaned)

    for source in candidates:
        for pattern in (r'^\D*(\d{7,8})', r'(\d{7,8})', r'(\d+)'):
            match = re.search(pattern, source)
            if match:
                return int(match.group(1))

    return 0
