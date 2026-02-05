import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Terminal Design Tool",
    layout="wide"
)

st.title("🚢 Terminal Design Configurator")

# =========================================================
# LAYOUT: LEFT (INPUT) | RIGHT (DESIGN)
# =========================================================
col_input, col_view = st.columns([1, 2])

# =========================================================
# LEFT PANEL - INPUT PARAMETER
# =========================================================
with col_input:
    st.subheader("Parameter Desain")

    layout_type = st.selectbox(
        "Tipe Layout",
        ["Lapangan Penumpukan", "Dermaga", "Gudang"]
    )

    panjang = st.slider("Panjang Area (meter)", 50, 500, 200)
    lebar = st.slider("Lebar Area (meter)", 30, 300, 100)
    tinggi = st.slider("Tinggi / Elevasi (meter)", 5, 50, 20)

    jumlah_blok = st.number_input(
        "Jumlah Blok",
        min_value=1,
        max_value=10,
        value=4
    )

    mode_view = st.radio(
        "Mode Tampilan",
        ["2D Plan", "3D Model"]
    )

# =========================================================
# RIGHT PANEL - DESIGN VIEW
# =========================================================
with col_view:
    st.subheader("Preview Desain")

    # =========================
    # 2D MODE
    # =========================
    if mode_view == "2D Plan":
        fig, ax = plt.subplots(figsize=(9, 6))

        # Main Area
        ax.add_patch(
            plt.Rectangle(
                (0, 0),
                panjang,
                lebar,
                color="#4CAF50",
                alpha=0.6
            )
        )

        # Block division
        jarak = panjang / jumlah_blok
        for i in range(1, jumlah_blok):
            ax.plot(
                [i * jarak, i * jarak],
                [0, lebar],
                linestyle="--",
                color="black",
                linewidth=1
            )

        ax.set_xlim(0, panjang)
        ax.set_ylim(0, lebar)
        ax.set_aspect("equal")
        ax.set_title(f"2D Layout - {layout_type}")
        ax.axis("off")

        st.pyplot(fig)

    # =========================
    # 3D MODE
    # =========================
    if mode_view == "3D Model":
        x = [0, panjang, panjang, 0, 0, panjang, panjang, 0]
        y = [0, 0, lebar, lebar, 0, 0, lebar, lebar]
        z = [0, 0, 0, 0, tinggi, tinggi, tinggi, tinggi]

        fig = go.Figure(
            data=[
                go.Mesh3d(
                    x=x,
                    y=y,
                    z=z,
                    color="green",
                    opacity=0.6
                )
            ]
        )

        fig.update_layout(
            scene=dict(
                xaxis_title="Panjang",
                yaxis_title="Lebar",
                zaxis_title="Tinggi",
                aspectmode="data"
            ),
            margin=dict(l=0, r=0, t=30, b=0),
            title=f"3D Model - {layout_type}"
        )

        st.plotly_chart(fig, use_container_width=True)

# =========================================================
# FOOTER
# =========================================================
st.markdown("---")
st.caption("Design Terminal Tool | Streamlit Cloud")
