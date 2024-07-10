
import requests
import json

def parse_job_titles(job_titles):
    """
    Sends a POST request with job titles to a prediction API and returns the response.

    Parameters:
    job_titles (list of str): A list of job title strings to be parsed.

    Returns:
    dict: A dictionary containing the parsed job titles and their predictions, 
          or an error message if the request fails.
    """
    url = 'http://34.69.91.183:8000/predict_jobs'
    headers = {"Content-Type": "application/json"}
    payload = {"jobTitles": job_titles}
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Error in request: {response.status_code}, {response.text}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Request exception: {str(e)}"}

def clean_job_titles(job_titles):
    """
    Cleans job titles based on predictions obtained from the parse_job_titles function.

    Parameters:
    job_titles (list of str): A list of job title strings to be cleaned.

    Returns:
    list of str: A list of cleaned job titles.
    """
    response = parse_job_titles(job_titles)
    if 'error' in response:
        return response

    words = response.get('job_titles_splitted', [])
    predictions = response.get('labels_for_words', [])
    
    ner_job_titles = []
    for job_title_splitted, preds in zip(words, predictions):
        clean_job_title = [word for i, word in enumerate(job_title_splitted) if 'job' in preds[i]]
        ner_job_titles.append(' '.join(clean_job_title) if clean_job_title else '')

    return ner_job_titles
