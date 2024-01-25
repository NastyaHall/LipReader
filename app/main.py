import streamlit as st 
import os
import imageio
import tensorflow as tf 
from utils import load_data, num_to_char
from neuralnetworkmodel import load_model 
import numpy as np 
from PIL import Image
from converttogif import convert_to_gif
import subprocess

st.set_page_config(layout='wide')

with st.sidebar:
    st.image('https://www.onepointltd.com/wp-content/uploads/2020/03/inno2.png')
    st.title('Lip Reader')
    st.info('This application is originally developed from LipNet deep learning model.')

st.header('Lip Reader')
options = os.listdir('data/s1')
selected_video = st.selectbox('Choose a video and the deep learning model will lip read what the man says and output the result', options)

col1, col2 = st.columns(2)

if options:
    with col1:
        # file_path = os.path.join('..', 'data', 's1', selected_video) 
        file_path = f'data/s1/{selected_video}'
        # os.system(f'ffmpeg -i {file_path} -vcodec libx264 test_video.mp4 -y')
        subprocess.run(f'ffmpeg -i {file_path} -vcodec libx264 test_video.mp4 -y', shell=True, check=True)
        # video = open('test_video.mp4', 'rb')
        video = open('app/test_video.mp4', 'rb')
        video_bytes = video.read()
        st.video(video_bytes)

    with col2:
        st.info('This is all the machine learning model sees when making a prediction')
        video, annotations = load_data(tf.convert_to_tensor(file_path))
        convert_to_gif()
        st.image('app/animation.gif', width=500)

        st.subheader('Result', divider='rainbow')
        with st.spinner('Wait for it...'):
            model = load_model()
            yhat = model.predict(tf.expand_dims(video, axis=0))
            decoder = tf.keras.backend.ctc_decode(yhat, [75], greedy=True)[0][0].numpy()
            
            converted_prediction = tf.strings.reduce_join(num_to_char(decoder)).numpy().decode('utf-8')
            st.success(converted_prediction, icon="✅")