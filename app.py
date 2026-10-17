import os
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Data Reviewer Eksternal FEB UNESA",
    layout="wide",
    page_icon="📝",
)

UPLOAD_DIR = "uploaded_files"
CSV_FILE = "data_reviewer.csv"
os.makedirs(UPLOAD_DIR, exist_ok=True)

INITIAL_DATA = [
    {
        "Nama Reviewer": "Prof. Dr. S. Pantja Djati, M.Si., M.A.",
        "Contact Person": "https://wa.me/+62816522737",
        "Asal Kampus": "Universitas Pertahanan RI",
        "Moderator": "Dr. Cici Widowati, S.P., M.S.M.",
    },
    {
        "Nama Reviewer": "Prof. Dr. Willy Arafah, M.M., DBA",
        "Contact Person": "https://wa.me/+6281318667667",
        "Asal Kampus": "Universitas Trisakti",
        "Moderator": "Dr. Anik Lestari Andjarwati, M.M.",
    },
    {
        "Nama Reviewer": "Prof. Dr. Murpin Josua Sembiring Gurky, S.E., M.Si.",
        "Contact Person": "https://wa.me/+62811339762",
        "Asal Kampus": "Universitas Ciputra Surabaya",
        "Moderator": "Dr. Dewi Ratih, S.E., M.S.M.",
    },
    {
        "Nama Reviewer": "Prof. Dr. Idayanti Nursyamsi, S.E., M.Si.",
        "Contact Person": "https://wa.me/+6281242607777",
        "Asal Kampus": "Universitas Hasanuddin",
        "Moderator": "Dr. Ni Nyoman Alit Triani, S.E., M.Ak.",
    },
    {
        "Nama Reviewer": "Prof. Dr. Ari Warok",
        "Contact Person": "https://wa.me/+628123313610",
        "Asal Kampus": "Tongmyong University",
        "Moderator": "Dr. Ratih Amelia, S.E., M.M.",
    },
    {
        "Nama Reviewer": "Prof. Risna Wijayanti, S.E., M.M., Ph.D.",
        "Contact Person": "https://wa.me/+6281232470244",
        "Asal Kampus": "Universitas Brawijaya",
        "Moderator": "Dr. Tri Sudarwanto, S.Pd., M.S.M.",
    },
    {
        "Nama Reviewer": "Prof. Dr. Isti Fadah, M.Si., CRA., CMA",
        "Contact Person": "https://wa.me/+6282140291875",
        "Asal Kampus": "Universitas Jember",
        "Moderator": "Dr. Rasyidi Faiz Akbar, S.E., M.M.",
    },
    {
        "Nama Reviewer": "Prof. Dr. Nasikh, S.E., M.P., M.Pd.",
        "Contact Person": "https://wa.me/+6281233497061",
        "Asal Kampus": "Universitas Negeri Malang",
        "Moderator": "Dr. Syaifurrizal Wijaya Putra, S.E., M.M.",
    },
    {
        "Nama Reviewer": "Prof. Dr. Yuliani, S.E., M.M.",
        "Contact Person": "https://wa.me/+628127829200",
        "Asal Kampus": "Universitas Sriwijaya",
        "Moderator": "Dr. Yessy Artanti, S.E., M.Si.",
    },
    {
        "Nama Reviewer": "Prof. Dr. Mohamad Yusak Anshori, M.M., CPM",
        "Contact Person": "https://wa.me/+62811337799",
        "Asal Kampus": "Universitas Nahdlatul Ulama Surabaya",
        "Moderator": "Dr. Nadia Asandimitra Haryono, S.E., M.M.",
    },
]


def load_data():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE, dtype=str).fillna("")
    else:
        df = pd.DataFrame(INITIAL_DATA)
        df["No. KTP"] = ""
        df["Berkas KTP"] = ""
        df["No. NPWP"] = ""
        df["Berkas NPWP"] = ""
        df["No. Rekening"] = ""
        df["Berkas Rekening"] = ""
        return df


df_data = load_data()

st.title("📌 Portal Pengumpulan Data Reviewer Eksternal FEB UNESA")
tab1, tab2 = st.tabs(["📥 Form Upload Moderator", "📊 Tabel Data Terkumpul"])

with tab1:
    options = [
        f"{row['Nama Reviewer']} (Moderator: {row['Moderator']})"
        for idx, row in df_data.iterrows()
    ]
    selected_option = st.selectbox("Pilih Reviewer / Moderator:", options)
    selected_index = options.index(selected_option)
    curr_row = df_data.iloc[selected_index]

    st.info(
        f"**Kampus:** {curr_row['Asal Kampus']} | **WhatsApp:** {curr_row['Contact Person']}"
    )

    with st.form("upload_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            no_ktp = st.text_input("Nomor KTP", value=str(curr_row["No. KTP"]))
            file_ktp = st.file_uploader(
                "Unggah KTP", type=["png", "jpg", "jpeg"]
            )
        with col2:
            no_npwp = st.text_input("Nomor NPWP", value=str(curr_row["No. NPWP"]))
            file_npwp = st.file_uploader(
                "Unggah NPWP", type=["png", "jpg", "jpeg"]
            )
        with col3:
            no_rek = st.text_input(
                "Nomor Rekening", value=str(curr_row["No. Rekening"])
            )
            file_rek = st.file_uploader(
                "Unggah Buku Rekening", type=["png", "jpg", "jpeg"]
            )

        submitted = st.form_submit_button("💾 Simpan Data & Berkas")

        if submitted:
            df_data.at[selected_index, "No. KTP"] = no_ktp
            df_data.at[selected_index, "No. NPWP"] = no_npwp
            df_data.at[selected_index, "No. Rekening"] = no_rek

            rev_id = f"reviewer_{selected_index+1}"

            def save_file(uploaded_file, file_type):
                ext = uploaded_file.name.split(".")[-1]
                path = os.path.join(UPLOAD_DIR, f"{rev_id}_{file_type}.{ext}")
                with open(path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                return path

            if file_ktp:
                df_data.at[selected_index, "Berkas KTP"] = save_file(
                    file_ktp, "ktp"
                )
            if file_npwp:
                df_data.at[selected_index, "Berkas NPWP"] = save_file(
                    file_npwp, "npwp"
                )
            if file_rek:
                df_data.at[selected_index, "Berkas Rekening"] = save_file(
                    file_rek, "rekening"
                )

            df_data.to_csv(CSV_FILE, index=False)
            st.success("✅ Data & Dokumen berhasil disimpan!")
            st.rerun()

with tab2:
    st.dataframe(df_data, use_container_width=True)
    csv_data = df_data.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Unduh Rekap Data (CSV)",
        data=csv_data,
        file_name="rekap_reviewer.csv",
        mime="text/csv",
    )
