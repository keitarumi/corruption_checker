from pydoc import describe
import streamlit as st
from PIL import Image
import numpy as np


def get_unique_colors(image):
    pixels = np.array(image)
    return set(tuple(p) for p in pixels.reshape(-1, 3))


def classify_colors_adjustable_v2(unique_colors, white_r_threshold, white_g_threshold, white_b_threshold, orange_r_threshold, orange_g_threshold, orange_b_threshold):
    white_like = set()
    orange_like = set()

    for color in unique_colors:
        r, g, b = color
        if r > white_r_threshold and g > white_g_threshold and b > white_b_threshold:
            white_like.add(color)
        elif r > orange_r_threshold and g > orange_g_threshold and b > orange_b_threshold:
            orange_like.add(color)
    return white_like, orange_like


def count_pixels_by_color_set(image, color_set):
    pixels = np.array(image)
    return sum(1 for pixel in pixels.reshape(-1, 3) if tuple(pixel) in color_set)


st.title("Corruption Checker")

# 画像を読み込む
image = Image.open('mihon.jpg')

# 画像を表示する
st.image(image, caption='スクリーンショットをするエリア', use_column_width=True)

uploaded_file = st.file_uploader(
    "マーケットプレイスの汚染度バーのスクリーンショットをアップしてください。", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert('RGB')
    st.image(image, use_column_width=True)

    st.write("デフォルト設定でうまくいかなかった場合に調整してみてください。")
    white_r_threshold = st.slider("White R Threshold", 0, 255, 200)
    white_g_threshold = st.slider("White G Threshold", 0, 255, 200)
    white_b_threshold = st.slider("White B Threshold", 0, 255, 200)

    orange_r_threshold = st.slider("Orange R Threshold", 0, 255, 100)
    orange_g_threshold = st.slider("Orange G Threshold", 0, 255, 30)
    orange_b_threshold = st.slider("Orange B Threshold", 0, 255, 30)

    if st.button("汚染度測定"):
        unique_colors = get_unique_colors(image)
        white_like, orange_like = classify_colors_adjustable_v2(
            unique_colors, white_r_threshold, white_g_threshold, white_b_threshold, orange_r_threshold, orange_g_threshold, orange_b_threshold)
        white_like_pixels = count_pixels_by_color_set(image, white_like)
        orange_like_pixels = count_pixels_by_color_set(image, orange_like)
        # st.write(f"白に近い色のピクセル数: {white_like_pixels}")
        # st.write(f"オレンジに近い色のピクセル数: {orange_like_pixels}")
        st.write(
            f"汚染度: {orange_like_pixels / (white_like_pixels + orange_like_pixels):.2%}")
