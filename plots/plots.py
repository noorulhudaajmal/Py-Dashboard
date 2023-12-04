import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from utils import *

colors = ["#2a9d8f", "#264653", "#e9c46a", "#f4a261", "#e76f51", "#ef233c", "#f6bd60", "#84a59d", "#f95738"]
# colors = ["#880d1e", "#f26a8d", "#dd2d4a", "#f49cbb", "#cbeef3", "#880d1e"]


def sales_revenue_card(df):
    sales_by_month = df.groupby("MONTH")["Revenue"].sum()
    sales_by_month = sales_by_month.reindex(MONTHS_ORDER).reset_index()
    fig = go.Figure(
        go.Indicator(
            mode="number",
            value=sales_by_month["Revenue"].sum(),
            number={"prefix": "$"},
            title={"text": "Total Sales Revenue", "font": {"size": 20}},
            domain={'y': [0, 1], 'x': [0.25, 0.75]}
        ))

    fig.add_trace(go.Scatter(
        x=sales_by_month["MONTH"],
        y=sales_by_month["Revenue"],
        mode="lines",
        fill='tozeroy',
        name="Total Revenue",
    ))
    fig.update_xaxes(showticklabels=False, showgrid=False)
    fig.update_yaxes(showticklabels=False, showgrid=False)
    fig = update_hover_layout(fig)
    fig.update_layout(height=250)
    return fig


def units_sold_card(df):
    qty_sold = df.groupby("MONTH")["QTY [Units]"].sum()
    qty_sold = qty_sold.reindex(MONTHS_ORDER).reset_index()
    fig = go.Figure(
        go.Indicator(
            mode="number",
            value=qty_sold["QTY [Units]"].sum(),
            number={"suffix": " units"},
            title={"text": "Total Units Sold", "font": {"size": 20}},
            domain={'y': [0, 1], 'x': [0.25, 0.75]}
        ))

    fig.add_trace(go.Scatter(
        x=qty_sold["MONTH"],
        y=qty_sold["QTY [Units]"],
        mode="lines",
        fill='tozeroy',
        name="Qty Sold",
    ))
    fig.update_xaxes(showticklabels=False, showgrid=False)
    fig.update_yaxes(showticklabels=False, showgrid=False)
    fig = update_hover_layout(fig)
    fig.update_layout(height=250)
    return fig


def profit_margin_card(df):
    monthly_financials = df.groupby("MONTH").agg({"Revenue": "sum", "Total GM [CAD]": "sum"})
    monthly_financials = monthly_financials.reindex(MONTHS_ORDER).reset_index()
    monthly_financials['Profit Margin'] = (monthly_financials['Total GM [CAD]'] / monthly_financials['Revenue']) * 100
    total_revenue = monthly_financials['Revenue'].sum()
    total_gross_margin = monthly_financials['Total GM [CAD]'].sum()
    overall_profit_margin = (total_gross_margin / total_revenue) * 100
    delta_ref = overall_profit_margin * 100 - np.mean(monthly_financials['Profit Margin'])
    fig = go.Figure(
        go.Indicator(
            mode="number+delta",
            value=overall_profit_margin,
            number={"suffix": "%", "font": {"size": 20}},
            title={"text": "Profit Margin", "font": {"size": 20}},
            delta={'reference': np.round(delta_ref, 2), 'relative': True, 'position': "bottom",
                   'valueformat': 'f', "font": {"size": 15}},
            domain={'y': [0, 1], 'x': [0.25, 0.75]}
        ))

    fig.add_trace(go.Scatter(
        x=monthly_financials["MONTH"],
        y=monthly_financials["Profit Margin"],
        mode="lines",
        fill='tozeroy',
        name="Profit Margin",
    ))

    fig.update_xaxes(showticklabels=False, showgrid=False)
    fig.update_yaxes(showticklabels=False, showgrid=False)
    fig = update_hover_layout(fig)
    fig.update_layout(height=250)

    return fig


def average_discount_rate_card(df):
    # Calculate the weighted discount rates, assuming discounts are stored as proportions (e.g., 20% is stored as 0.20)
    df['Weighted SD1'] = df['Standard Discount [SD1 %]'] * df['Revenue']
    df['Weighted SD2'] = df['Standard Discount [SD2 %]'] * df['Revenue']
    df['Weighted DSP'] = df['Special Discount [DSP %]'] * df['Revenue']
    df['Weighted DPR'] = df['Promo Campaign [DPR%]'] * df['Revenue']

    # Aggregate these weighted discounts and sum of revenue by month
    monthly_discounts = df.groupby('MONTH').agg({
        'Weighted SD1': 'sum',
        'Weighted SD2': 'sum',
        'Weighted DSP': 'sum',
        'Weighted DPR': 'sum',
        'Revenue': 'sum'
    })
    monthly_discounts = monthly_discounts.reindex(MONTHS_ORDER).reset_index()

    # Calculate the overall average discount rate by month
    monthly_discounts['Avg Discount Rate'] = (
            monthly_discounts[['Weighted SD1', 'Weighted SD2', 'Weighted DSP', 'Weighted DPR']].sum(axis=1)
            / monthly_discounts['Revenue'])

    # Calculate the overall average discount rate
    total_discounts = monthly_discounts[['Weighted SD1', 'Weighted SD2', 'Weighted DSP', 'Weighted DPR']].sum().sum()
    total_revenue = monthly_discounts['Revenue'].sum()
    overall_avg_discount_rate = total_discounts / total_revenue

    delta_ref = overall_avg_discount_rate - np.mean(monthly_discounts['Avg Discount Rate']) * 100
    fig = go.Figure(
        go.Indicator(
            mode="number+delta",
            value=overall_avg_discount_rate * 100,  # Convert proportion to percentage
            number={"suffix": "%", "font": {"size": 20}},
            title={"text": "Average Discount Rate", "font": {"size": 20}},
            delta={'reference': delta_ref, 'relative': True, 'position': "bottom",
                   'valueformat': 'f', "font": {"size": 15}},
            domain={'y': [0, 1], 'x': [0.25, 0.75]}
        ))

    fig.add_trace(go.Scatter(
        x=monthly_discounts["MONTH"],
        y=monthly_discounts["Avg Discount Rate"] * 100,  # Convert proportion to percentage for plotting
        mode="lines",
        fill='tozeroy',
        name="Avg Discount Rate",
    ))

    fig.update_xaxes(showticklabels=False, showgrid=False)
    fig.update_yaxes(showticklabels=False, showgrid=False)
    fig = update_hover_layout(fig)
    fig.update_layout(height=250)

    return fig


def average_selling_price_card(df):
    # Calculate the Average Selling Price (ASP) by dividing total revenue by total units sold
    # Group by month to get monthly ASP
    monthly_sales = df.groupby("MONTH").agg({"Revenue": "sum", "QTY [Units]": "sum"})
    monthly_sales = monthly_sales.reindex(MONTHS_ORDER).reset_index()
    monthly_sales['ASP'] = monthly_sales['Revenue'] / monthly_sales['QTY [Units]']

    # Calculate the total Average Selling Price across all months
    total_revenue = monthly_sales['Revenue'].sum()
    total_units_sold = monthly_sales['QTY [Units]'].sum()
    overall_asp = total_revenue / total_units_sold

    fig = go.Figure(
        go.Indicator(
            mode="number",
            value=overall_asp,
            number={"prefix": "$", "font": {"size": 20}},
            title={"text": "Average Selling Price", "font": {"size": 20}},
            domain={'y': [0, 1], 'x': [0.25, 0.75]}
        ))

    fig.add_trace(go.Scatter(
        x=monthly_sales["MONTH"],
        y=monthly_sales["ASP"],
        mode="lines",
        fill='tozeroy',
        name="Average Selling Price",
    ))

    fig.update_xaxes(showticklabels=False, showgrid=False)
    fig.update_yaxes(showticklabels=False, showgrid=False)
    fig = update_hover_layout(fig)
    fig.update_layout(height=250)

    return fig


def income_statement(df):
    df['CoGS'] = df['Total Cost [CAD]']
    df['Total Expense'] = df['Standard Discount [SD1][CAD]'] + df['Standard Discount [SD2][CAD]'] + df[
        'Special Discount [DSP][CAD]'] + df['Promo Campaign [DPR][CAD]']
    df['Net Profit'] = df['Revenue'] - df['Total Expense'] - df['CoGS']

    fin_data = df.groupby("MONTH")['Total Expense', 'CoGS', 'Revenue', 'Net Profit'].sum()
    fin_data = fin_data.reindex(MONTHS_ORDER).reset_index()
    fig = go.Figure()
    fig.add_trace(
        go.Bar(x=fin_data["MONTH"], y=fin_data["Total Expense"], name="Total Expense",
               marker=dict(color=colors[0]))
    )
    fig.add_trace(
        go.Bar(x=fin_data["MONTH"], y=fin_data["CoGS"], name="CoGS",
               marker=dict(color=colors[1]))
    )
    fig.add_trace(
        go.Bar(x=fin_data["MONTH"], y=fin_data["Revenue"], name="Revenue",
               marker=dict(color=colors[2]))
    )
    fig.add_trace(
        go.Bar(x=fin_data["MONTH"], y=fin_data["Net Profit"], name="Net Profit",
               marker=dict(color=colors[3]))
    )
    fig.update_layout(barmode="group", title="Income Statement", xaxis_title="Month",
                      yaxis_title="Amount", height=450)
    fig = update_hover_layout(fig)
    fig.update_xaxes(type='category')

    return fig


def expenses_pie(df):
    summed_discounts = df[['Standard Discount [SD1][CAD]', 'Standard Discount [SD2][CAD]',
                           'Special Discount [DSP][CAD]', 'Promo Campaign [DPR][CAD]',
                           'Rebates [DREB][CAD]']].sum()
    fig = go.Figure(data=[
        go.Pie(labels=summed_discounts.index, values=summed_discounts.values, hole=.4,
               marker_colors=colors)
    ])

    fig.update_layout(
        title_text='Discounts and Promos Analysis',
        annotations=[dict(text='Expenses', x=0.5, y=0.5, font_size=15, showarrow=False)]
    )

    fig = update_hover_layout(fig)

    return fig


def monthly_rev_gm(filtered_data):
    revenue_data = filtered_data.groupby("MONTH")["Revenue", "Total GM [CAD]"].sum()
    revenue_data = revenue_data.reindex(MONTHS_ORDER).reset_index()
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=revenue_data["MONTH"], y=revenue_data["Revenue"], mode="lines+markers+text",
        marker=dict(color="#e76f51"), line=dict(color="#e76f51"), textposition="top center", name="Revenue"))
    fig.add_trace(go.Scatter(
        x=revenue_data["MONTH"], y=revenue_data["Total GM [CAD]"], mode="lines+markers",
        marker=dict(color="#264653"), line=dict(color="#264653"), textposition="top center", name="Profit Margin"))
    fig.update_layout(title="Revenue/G.Profit Over Time", xaxis_title="Month", yaxis_title="Amount")
    fig = update_hover_layout(fig)
    return fig


def product_performance(df):
    df["Unit GM [%]"] = pd.to_numeric(df['Unit GM [%]'], errors='coerce')
    prod_data = df.groupby("Product Range").agg(
        {"Unit GM [%]": "mean",
         "QTY [Units]": "sum"}
    ).reset_index()
    prod_data = prod_data.sort_values(by="QTY [Units]", ascending=False)
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Bar(
            x=prod_data["Product Range"], y=df["QTY [Units]"], name="Quantity Sold",
            marker=dict(color="#264653")
        ), secondary_y=False
    )
    fig.add_trace(
        go.Scatter(
            x=prod_data["Product Range"], y=df["Unit GM [%]"], name="Profit Margin Contribution",
            marker=dict(color="#e76f51"), mode="markers+lines"
        ), secondary_y=True
    )
    fig.update_layout(title="Product Selling Performance", xaxis_title="Product Range", yaxis_title="Units")
    fig = update_hover_layout(fig)
    return fig


def rev_by_customer(df):
    prod_data = df.groupby("Customer Name")[["Revenue", "Total GM [CAD]", "QTY [Units]"]].sum().reset_index()
    fig = make_subplots(rows=1, cols=3, specs=[[{'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}]])
    fig.add_trace(
        go.Pie(labels=prod_data["Customer Name"], values=prod_data["Revenue"], name="Revenue",
               marker_colors=colors, title="Revenue"), 1, 1
    )
    fig.add_trace(
        go.Pie(labels=prod_data["Customer Name"], values=prod_data["Total GM [CAD]"], name="Profit Margin",
               marker_colors=colors, title="Profit Margin"), 1, 2
    )
    fig.add_trace(
        go.Pie(labels=prod_data["Customer Name"], values=prod_data["QTY [Units]"], name="Qty Sold",
               marker_colors=colors, title="Quantity"), 1, 3
    )

    fig.update_traces(hole=.4, hoverinfo="label+percent+name")

    fig.update_layout(
        title_text='Customers Distribution'
    )

    fig = update_hover_layout(fig)
    return fig


def avg_disc_given(df):
    df["Total Discount"] = df['Standard Discount [SD1][CAD]'] + df['Standard Discount [SD2][CAD]'] + df[
        'Special Discount [DSP][CAD]']
    df = df.groupby("Customer Name")["Total Discount"].mean().reset_index()

    fig = go.Figure(
        go.Bar(x=df["Customer Name"], y=df["Total Discount"],
               marker=dict(color=colors[0]))
    )
    fig.update_layout(
        title_text='Avg. Discount availed by Customers')
    fig = update_hover_layout(fig)
    return fig


def clv_plot(df):
    # Calculate Customer Lifetime Value approximation
    clv = df.groupby('Customer Name')['Revenue'].sum().sort_values(ascending=False).reset_index()

    # Calculate the cumulative sum of revenue and the cumulative percentage
    clv['Cumulative Revenue'] = clv['Revenue'].cumsum()
    clv['Cumulative Percentage'] = clv['Cumulative Revenue'] / clv['Revenue'].sum() * 100

    # Plot for Customer Lifetime Value
    fig_clv = go.Figure(data=[
        go.Bar(x=clv['Customer Name'], y=clv['Cumulative Percentage'], marker=dict(color=colors[1]))
    ])

    fig_clv.update_layout(
        title_text='Customer Lifetime Value (CLV) Approximation',
        xaxis_title='Customer Name',
        yaxis_title='Cumulative Percentage'
    )
    fig_clv = update_hover_layout(fig_clv)

    return fig_clv


def average_list_price_card(df):
    monthly_sales = df.groupby("MONTH")["List Price [CAD]"].mean()
    monthly_sales = monthly_sales.reindex(MONTHS_ORDER).reset_index()
    fig = go.Figure(
        go.Indicator(
            mode="number",
            value=df["List Price [CAD]"].mean(),
            number={"prefix": "C$", "font": {"size": 32}},
            title={"text": "Average List Price", "font": {"size": 20}},
            domain={'y': [0, 1], 'x': [0.25, 0.75]}
        ))
    fig.add_trace(go.Scatter(
        x=monthly_sales["MONTH"],
        y=monthly_sales["List Price [CAD]"],
        mode="lines",
        fill='tozeroy',
        name="Avg. List Price",
    ))

    fig.update_xaxes(showticklabels=False, showgrid=False)
    fig.update_yaxes(showticklabels=False, showgrid=False)
    fig = update_hover_layout(fig)
    fig.update_layout(height=250)

    return fig


def total_prod_qty_card(df):
    monthly_sales = df.groupby("MONTH")["QTY [Units]"].sum()
    monthly_sales = monthly_sales.reindex(MONTHS_ORDER).reset_index()
    fig = go.Figure(
        go.Indicator(
            mode="number",
            value=df["QTY [Units]"].sum(),
            number={"suffix": " units", "font": {"size": 32}},
            title={"text": "Qty Sold", "font": {"size": 20}},
            domain={'y': [0, 1], 'x': [0.25, 0.75]}
        ))
    fig.add_trace(go.Scatter(
        x=monthly_sales["MONTH"],
        y=monthly_sales["QTY [Units]"],
        mode="lines",
        fill='tozeroy',
        name="Qty Sold",
    ))

    fig.update_xaxes(showticklabels=False, showgrid=False)
    fig.update_yaxes(showticklabels=False, showgrid=False)
    fig = update_hover_layout(fig)
    fig.update_layout(height=250)

    return fig


def total_prod_rev_card(df):
    monthly_sales = df.groupby("MONTH")["Revenue"].sum()
    monthly_sales = monthly_sales.reindex(MONTHS_ORDER).reset_index()
    fig = go.Figure(
        go.Indicator(
            mode="number",
            value=df["Revenue"].sum(),
            number={"prefix": "C$ ", "font": {"size": 32}},
            title={"text": "Total Revenue", "font": {"size": 20}},
            domain={'y': [0, 1], 'x': [0.25, 0.75]}
        ))
    fig.add_trace(go.Scatter(
        x=monthly_sales["MONTH"],
        y=monthly_sales["Revenue"],
        mode="lines",
        fill='tozeroy',
        name="Total Revenue",
    ))

    fig.update_xaxes(showticklabels=False, showgrid=False)
    fig.update_yaxes(showticklabels=False, showgrid=False)
    fig = update_hover_layout(fig)
    fig.update_layout(height=250)

    return fig


def total_prod_GM_card(df):
    monthly_sales = df.groupby("MONTH")["Total GM [CAD]"].sum()
    monthly_sales = monthly_sales.reindex(MONTHS_ORDER).reset_index()
    fig = go.Figure(
        go.Indicator(
            mode="number",
            value=df["Total GM [CAD]"].sum(),
            number={"prefix": "C$ ", "font": {"size": 32}},
            title={"text": "Profit Margin", "font": {"size": 20}},
            domain={'y': [0, 1], 'x': [0.25, 0.75]}
        ))
    fig.add_trace(go.Scatter(
        x=monthly_sales["MONTH"],
        y=monthly_sales["Total GM [CAD]"],
        mode="lines",
        fill='tozeroy',
        name="Total Gross Margin",
    ))

    fig.update_xaxes(showticklabels=False, showgrid=False)
    fig.update_yaxes(showticklabels=False, showgrid=False)
    fig = update_hover_layout(fig)
    fig.update_layout(height=250)

    return fig
