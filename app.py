import streamlit as st
from smile import detect_smiles
import cv2
import numpy as np
from PIL import Image
import tempfile
import os
import time

st.title ("SMILE DETECTION") 
# Buat folder output jika belum ada
os.makedirs("output", exist_ok=True)

container = st.container()
st.caption ("Smile — it's the simplest way to brighten the world.")
st.write("Selamat datang di Smile Detection, sebuah aplikasi cerdas yang bisa mengenali senyum secara otomatis dari foto, video, bahkan secara real-time lewat webcam!🥰")

# Pilih Mode
mode = st.radio("Pilih Mode:", ["Upload File", "Open Webcam"])

# Upload file
uploaded_file = None
video_file_path = None

if mode == "Upload File":
    uploaded_file = st.file_uploader("Upload Foto atau Video", type=["jpg", "jpeg", "png", "mp4", "avi"])
    if uploaded_file:
        file_type = uploaded_file.type
        if "image" in file_type:
            file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            uploaded_image = cv2.imdecode(file_bytes, 1)
        elif "video" in file_type:
            tfile = tempfile.NamedTemporaryFile(delete=False)
            tfile.write(uploaded_file.read())
            video_file_path = tfile.name

# Tombol Proses

if st.button("Proses"):
    progress_text = "Operation in progress. Please wait."
    my_bar = st.progress(0, text=progress_text)

    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=progress_text)
    time.sleep(1)
    my_bar.empty()
    if mode == "Upload File" and uploaded_file is None:
        st.warning("Silakan upload file terlebih dahulu.")
    elif mode == "Open Webcam":
        st.info("Mengakses webcam...")
        cap = cv2.VideoCapture(0)
        out_path = "output/webcam_output.avi"
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(out_path, fourcc, 20.0, (640, 480))

        stframe = st.empty()
        stop = st.button("Stop Webcam")

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret or stop:
                break
            result = detect_smiles(frame.copy())
            out.write(result)
            stframe.image(result, channels="BGR")

        cap.release()
        out.release()
        st.success("Proses selesai.")
        with open(out_path, "rb") as f:
            st.download_button("Download Hasil Webcam", f, file_name="webcam_output.avi")
    
    elif uploaded_file:
        if "image" in uploaded_file.type:
            result = detect_smiles(uploaded_image.copy())
            output_path = "output/labeled_image.jpg"
            cv2.imwrite(output_path, result)
            st.image(result, channels="BGR", caption="Hasil Deteksi")
            with open(output_path, "rb") as f:
                st.download_button("Download Gambar", f, file_name="labeled_image.jpg")
        
        elif "video" in uploaded_file.type:
            stframe = st.empty()
            cap = cv2.VideoCapture(video_file_path)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            output_path = "output/labeled_video.mp4"
            out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'XVID'), fps, (width, height))

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                result = detect_smiles(frame.copy())
                out.write(result)
                stframe.image(result, channels="BGR")
            cap.release()
            out.release()
            st.success("Video selesai diproses.")
            with open(output_path, "rb") as f:
                progress_text = "Operation in progress. Please wait."
                my_bar = st.progress(0, text=progress_text)

                for percent_complete in range(100):
                    time.sleep(0.01)
                    my_bar.progress(percent_complete + 1, text=progress_text)
                time.sleep(1)
                my_bar.empty()
                st.download_button("Download Video", f, file_name="labeled_video.avi")