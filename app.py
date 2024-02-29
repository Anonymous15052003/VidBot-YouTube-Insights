import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline

st.title("VidBot YouTube Insights")

user_input = st.text_input("Enter your message here:")

def summary_api(user_input):
    url = user_input
    video_id = url.split('=')[-1]  # Use [-1] to get the last element, which should be the video ID
    if len(video_id) == 0:
        return "Invalid YouTube URL. Please enter a valid URL."
    summary = get_summary(get_transcript(video_id))
    return summary

def get_transcript(video_id):
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    transcript = ' '.join([d['text'] for d in transcript_list])
    return transcript

def get_summary(transcript):
    summariser = pipeline('summarization')
    summary = ''
    for i in range(0, (len(transcript)//1000)+1):
        summary_text = summariser(transcript[i*1000:(i+1)*1000],max_length=200, min_length=10, do_sample=False)[0]['summary_text']
        summary = summary + summary_text + ' '
    return summary

output=summary_api(user_input)
st.write(output)