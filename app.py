import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(page_title="Dermaga Design Tool", layout="wide")
st.title("🚢 Dermaga Design – Top View & 3D")

# =====================================================
# INPUT & VIEW LAYOUT
# =====================================================
col_input, col_view = st.columns([1, 2])

# =====================================================
# INPUT PANEL (LEFT)
# =====================================================
with col_input:
    st.subheader("Parameter Dermaga")

    quay_length = st.slider("Panjang Dermaga (m)", 100, 1000, 300)
    quay_width = st.slider("Lebar Dermaga (m)", 20, 80, 35)

    lane_width = st.slider("Lebar Lane (m)", 3, 10, 5)
    lane_gap = st.slider("Jarak Antar Lane (m)", 1, 5, 2)
    lane_count = st.number_input("Jumlah Lane Dermaga", 1, 6, 2)

    hatch_width = st.slider("Lebar Hatch Cover (m)", 5, 30, 15)

    back_lane_count = st.number_input("Jumlah Lane Belakang Hatch", 1, 6, 2)
    back_lane_width = st.slider("Lebar Lane Belakang (m)", 3, 10, 5)
    back_lane_gap = st.slider("Jarak Antar Lane Belakang (m)", 1, 5, 2)

    view_mode = st.radio("Mode Tampilan", ["2D Tampak Atas", "3D Model"])

# =====================================================
# DESIGN VIEW (RIGHT)
# =====================================================
with col_view:
    st.subheader("Visualisasi Dermaga")

    # ===============================
    # 2D TOP VIEW
    # ===============================
    if view_mode == "2D Tampak Atas":
        fig, ax = plt.subplots(figsize=(12, 5))

        # Dermaga
        ax.add_patch(
            plt.Rectangle((0, 0), quay_length, quay_width,
                          color="#B0BEC5", alpha=0.8)
        )

        # Bollard tiap 10 meter
        for x in range(0, quay_length + 1, 10):
            ax.plot(x, quay_width - 1, "ko", markersize=4)

        # Traffic lane dermaga
        y_pos = 2
        for i in range(lane_count):
            ax.add_patch(
                plt.Rectangle(
                    (0, y_pos),
                    quay_length,
                    lane_width,
                    color="#90CAF9",
                    alpha=0.8
                )
            )
            y_pos += lane_width + lane_gap

        # Hatch cover
        hatch_y = y_pos
        ax.add_patch(
            plt.Rectangle(
                (0, hatch_y),
                quay_length,
                hatch_width,
                color="#A1887F",
                alpha=0.9
            )
        )

        # Rail Quay Container Crane
        ax.plot([0, quay_length], [hatch_y - 1, hatch_y - 1],
                color="black", linewidth=3)
        ax.plot([0, quay_length], [hatch_y + hatch_width + 1, hatch_y + hatch_width + 1],
                color="black", linewidth=3)

        # Traffic lane belakang hatch
        y_pos = hatch_y + hatch_width + 3
        for i in range(back_lane_count):
            ax.add_patch(
                plt.Rectangle(
                    (0, y_pos),
                    quay_length,
                    back_lane_width,
                    color="#AED581",
                    alpha=0.8
                )
            )
            y_pos += back_lane_width + back_lane_gap

        ax.set_xlim(0, quay_length)
        ax.set_ylim(0, quay_width + 40)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_title("2D Tampak Atas Dermaga")

        st.pyplot(fig)

    # ===============================
    # 3D MODEL
    # ===============================
    if view_mode == "3D Model":
        x = [0, quay_length, quay_length, 0]
        y = [0, 0, quay_width, quay_width]
        z = [0, 0, 0, 0]

        # Dermaga surface
        fig = go.Figure(
            data=[
                go.Mesh3d(
                    x=[0, quay_length, quay_length, 0, 0, quay_length, quay_length, 0],
                    y=[0, 0, quay_width, quay_width, 0, 0, quay_width, quay_width],
                    z=[0, 0, 0, 0, 2, 2, 2, 2],
                    color="lightgrey",
                    opacity=0.9
                )
            ]
        )

        # Bollard 3D (simple cylinder)
        for bx in range(0, quay_length + 1, 10):
            fig.add_trace(
                go.Scatter3d(
                    x=[bx],
                    y=[quay_width - 1],
                    z=[2],
                    mode="markers",
                    marker=dict(size=5, color="black"),
                    showlegend=False
                )
            )

        # Crane rail
        fig.add_trace(
            go.Scatter3d(
                x=[0, quay_length],
                y=[hatch_width, hatch_width],
                z=[2, 2],
                mode="lines",
                line=dict(width=6, color="black"),
                name="QCC Rail"
            )
        )

        fig.update_layout(
            scene=dict(
                xaxis_title="Panjang Dermaga (m)",
                yaxis_title="Lebar Dermaga (m)",
                zaxis_title="Elevasi (m)",
                aspectmode="data"
            ),
            margin=dict(l=0, r=0, b=0, t=30),
            title="3D Model Dermaga"
        )

        st.plotly_chart(fig, use_container_width=True)

st.caption("Dermaga Design Tool | Streamlit Cloud")
