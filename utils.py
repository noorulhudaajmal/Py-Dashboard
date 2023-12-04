import pandas as pd

MONTHS_ORDER = ["Jan", "Feb", "Mar", "April", "May",
                "Jun", "Jul", "Aug", "Sept", "Oct",
                "Nov", "Dec"]


def format_currency_label(value):
    if value >= 1e9:  # Billion
        return f'{value / 1e9:.2f} bn'
    elif value >= 1e6:  # Million
        return f'{value / 1e6:.2f} M'
    elif value >= 1e3:  # Thousand
        return f'{value / 1e3:.2f} K'
    else:
        return f'{value:.2f}'


def update_hover_layout(fig):
    fig.update_layout(
        {
            "paper_bgcolor": "rgba(0, 0, 0, 0)",
            "plot_bgcolor": "rgba(0, 0, 0, 0)",
        },
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="white",
            font_color="black",
            font_size=16,
            font_family="Rockwell"
        ),
        height=400
    )
    return fig


def pre_process_data(df):
    # Convert columns to float, coerce errors to NaN
    df['Standard Discount [SD1][CAD]'] = pd.to_numeric(df['Standard Discount [SD1][CAD]'], errors='coerce')
    df['Standard Discount [SD2][CAD]'] = pd.to_numeric(df['Standard Discount [SD2][CAD]'], errors='coerce')
    df['Special Discount [DSP][CAD]'] = pd.to_numeric(df['Special Discount [DSP][CAD]'], errors='coerce')
    df['Promo Campaign [DPR][CAD]'] = pd.to_numeric(df['Promo Campaign [DPR][CAD]'], errors='coerce')

    return df



