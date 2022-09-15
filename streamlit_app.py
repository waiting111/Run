import streamlit as st
import numpy as np
import cv2
import glob, os


class streamlit_im2im:
    def __init__(self, page_title, func, sliders={}, display_path=None,
                 layout='wide', initial_sidebar_state='expanded'):

        st.set_page_config(page_title=page_title, layout=layout, initial_sidebar_state=initial_sidebar_state)
        st.title(page_title)

        sliders_dict = {}
        for name, range in sliders.items():
            sliders_dict[name] = st.sidebar.slider(
                name, range['min'], range['max'], range['default'], range['step'])

        img = None
        if display_path is not None:
            files = glob.glob(os.path.join(display_path, '*.*'))
            basenames = [os.path.basename(file) for file in files]
            select_img = st.selectbox('test images', basenames)
            img = cv2.imread(os.path.join(display_path, select_img))

        uploaded_file = st.file_uploader("Choose a file", ['jpg', 'jpeg', 'png'])
        if uploaded_file is not None:
            print(f'{uploaded_file}')
            nparr = np.fromstring(uploaded_file.getvalue(), np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is not None:
            outputs = func(img, sliders_dict)
            cols = st.columns(len(outputs))

            i = 0
            for name in outputs.keys():
                with cols[i]:
                    st.image(outputs[name], caption=name, channels='BGR')
                i += 1


def GaussianBlur(img, radius, sigma):
    ksize = 2 * radius + 1
    out = cv2.GaussianBlur(img, ksize=(ksize, ksize), sigmaX=sigma, sigmaY=sigma)
    return out


def imgprocess(img, slider_dict):
    radius = slider_dict['radius']
    sigma = slider_dict['sigma']
    draw_outs = {}
    draw_outs['Source'] = img
    draw_outs['gauss'] = GaussianBlur(img, radius, sigma)
    return draw_outs

sliders = {
    'radius': {'min': 1, 'max': 15, 'default': 5, 'step': 1},
    'sigma': {'min': 0.1, 'max': 5.0, 'default': 1.2, 'step': 0.01},
}

streamlit_im2im("My first Demo", func=imgprocess, sliders=sliders, display_path=None)
