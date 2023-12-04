import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from plots.plots import *
from utils import *

# ------------------------------ Page Configuration------------------------------
st.set_page_config(page_title="Aitionics", page_icon="📊", layout="wide")
# ----------------------------------- Page Styling ------------------------------

with open("css/style.css") as css:
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

st.markdown("""
<style>
    [data-testid=stHeader] {
        display:none;
    }
    [data-testid=block-container] {
        padding-top: 0px;
        # background:#eff0d1;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
  <style>
   [data-testid=stSidebarUserContent]{
      margin-top: -75px;
      margin-top: -75px;
    }
  </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.image("./assets/logo.png", width=200)
    file_upload = st.file_uploader("", type=["csv", "xlsx", "xls"], )


def main():
    df = pd.DataFrame()

    if file_upload is not None:
        if file_upload.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            df = pd.read_excel(file_upload, engine="openpyxl")
        elif file_upload.type == "application/vnd.ms-excel":  # Check if it's an XLS file
            df = pd.read_excel(file_upload)
        elif file_upload.type == "text/csv":  # Check if it's a CSV file
            df = pd.read_csv(file_upload, encoding=("UTF-8"))

        df = pre_process_data(df)
        # --------------------------- Data Pre-processing -------------------------------

        # ----------------------------------- Menu --------------------------------------
        menu = option_menu(menu_title=None, menu_icon=None, orientation="horizontal",
                           options=["Overview", "Customer Insights", "Product Performance"])

        if menu == "Overview":
            # -------------------------------- KPIs ----------------------------------
            kpi_row = st.columns(5)
            kpi_row[0].plotly_chart(sales_revenue_card(df), use_container_width=True)
            kpi_row[1].plotly_chart(units_sold_card(df), use_container_width=True)
            kpi_row[2].plotly_chart(profit_margin_card(df), use_container_width=True)
            kpi_row[3].plotly_chart(average_discount_rate_card(df), use_container_width=True)
            kpi_row[4].plotly_chart(average_selling_price_card(df), use_container_width=True)

            row_1 = st.columns((3,2))
            # ------------------------------- Income & Discounts Analysis --------------------------
            row_1[0].plotly_chart(income_statement(df), use_container_width=True)
            row_1[1].plotly_chart(expenses_pie(df), use_container_width=True)
            # ----------------------------- End Overview --------------------------------

        if menu == "Customer Insights":
            df_0 = df.copy()
            # ----------------------------- Filters --------------------------------
            year = st.sidebar.selectbox(label="Year", options=df_0["YEAR"].unique())
            df_0 = df_0[df_0["YEAR"] == year]
            months = st.sidebar.multiselect(label="Month", options=df_0["MONTH"].unique(), placeholder="All")
            if months:
                df_0 = df_0[df_0["MONTH"].isin(months)]

            channel = st.sidebar.selectbox(label="Channel", options=df_0["Channel Category"].unique())
            df_0 = df_0[df_0["Channel Category"] == channel]
            # --------------------------- Product Sales Analysis ------------------------------------
            st.plotly_chart(rev_by_customer(df_0), use_container_width=True)
            row_1 = st.columns(2)
            row_1[0].plotly_chart(avg_disc_given(df_0), use_container_width=True)
            row_1[1].plotly_chart(clv_plot(df_0), use_container_width=True)

        if menu == "Product Performance":
            df_1 = df.copy()
            # ----------------------------- Filters --------------------------------
            year = st.sidebar.selectbox(label="Year", options=df["YEAR"].unique())
            df_1 = df_1[df_1["YEAR"] == year]
            category = st.sidebar.selectbox(label="Product Category", options=df["Product Category"].unique())
            df_1 = df_1[df_1["Product Category"] == category]
            family = st.sidebar.selectbox(label="Product Family", options=df_1["Product Family"].unique())
            df_1 = df_1[df_1["Product Family"] == family]

            # --------------------------- KPIs ------------------------------------
            avg_list_price = df_1["List Price [CAD]"].mean()
            total_qty_cold = df_1["QTY [Units]"].sum()
            total_rev = df_1["Revenue"].sum()
            total_profit_margin = df_1['Total GM [CAD]'].sum()

            kpi_row = st.columns(4)
            kpi_row[0].plotly_chart(average_list_price_card(df_1), use_container_width=True)
            kpi_row[1].plotly_chart(total_prod_qty_card(df_1), use_container_width=True)
            kpi_row[2].plotly_chart(total_prod_rev_card(df_1), use_container_width=True)
            kpi_row[3].plotly_chart(total_prod_GM_card(df_1), use_container_width=True)

            # --------------------------- Product Sales Analysis ------------------------------------

            row_1 = st.columns(2)
            row_1[0].plotly_chart(monthly_rev_gm(df_1), use_container_width=True)
            row_1[1].plotly_chart(product_performance(df_1), use_container_width=True)

            # --------------------------- End Product Performance ------------------------------------

    else:
        st.info("Upload data to analyze")


if __name__ == main():
    main()