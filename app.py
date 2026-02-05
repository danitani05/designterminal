import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("Design Configurator")

col_input, col_view = st.columns([1, 2])

# =========================
# PANEL INPUT (KIRI)
# =========================
with col_input:
    st.header("Parameter Desain")

    panjang = st.slider("Panjang (m)", 50, 500, 200)
    lebar = st.slider("Lebar (m)", 30, 300, 100)
    tinggi = st.slider("Tinggi (m)", 5, 50, 20)

    mode = st.radio("Mode Tampilan", ["2D", "3D"])

# =========================
# PANEL DESAIN (KANAN)
# =========================
with col_view:
    st.header("Preview Desain")

    if mode == "2D":
        fig, ax = plt.subplots(figsize=(8,5))
        ax.add_patch(
            plt.Rectangle((0,0), panjang, lebar, color="#4CAF50", alpha=0.6)
        )
        ax.set_xlim(0, panjang)
        ax.set_ylim(0, lebar)
        ax.set_aspect("equal")
        ax.axis("off")
        st.pyplot(fig)

    if mode == "3D":
        fig = go.Figure(data=[
            go.Mesh3d(
                x=[0, panjang, panjang, 0, 0, panjang, panjang, 0],
                y=[0, 0, lebar, lebar, 0, 0, lebar, lebar],
                z=[0, 0, 0, 0, tinggi, tinggi, tinggi, tinggi],
                opacity=0.6
            )
        ])

        fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            scene=dict(aspectmode="data")
        )

        st.plotly_chart(fig, use_container_width=True)

