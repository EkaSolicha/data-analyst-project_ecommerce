import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

order_items_df = pd.read_csv("order_items_dataset.csv")
orders_df = pd.read_csv("orders_dataset.csv")
products_df = pd.read_csv("products_dataset.csv")

order_price_df = pd.merge(
    left=orders_df,
    right=order_items_df,
    how="outer",
    left_on="order_id",
    right_on="order_id"
)

product_ordered_df = pd.merge(
    left=order_items_df,
    right=products_df,
    how="outer",
    left_on="product_id",
    right_on="product_id"
)

def sum_price_df(df):
    sum_price_df = product_ordered_df.groupby(by="product_category_name")['price'].sum().reset_index()
    return sum_price_df


def mean_price_df(df):
    mean_price_df = order_price_df.groupby(by="order_status")['price'].mean().reset_index()

    mean_price_df = mean_price_df.reset_index()
    mean_price_df.rename(columns={
        "order_status": "status pesanan",
        "price": "harga rata-rata"
    }, inplace=True)
    
    return mean_price_df

st.header('Brazilian E-Commerce Dashboard')

st.subheader("Average Price by Order Status")
 
col1 = st.columns(1)
 
with col1[0]:
    fig, ax = plt.subplots(figsize=(20, 10))
    
    colors = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3"]
 
    sns.barplot(
        y="harga rata-rata", 
        x="status pesanan",
        data=mean_price_df(order_price_df).sort_values(by='harga rata-rata', ascending=False),
        palette=colors,
        hue="status pesanan",
        ax=ax
    )
    ax.set_title("Average Price by Order Status", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

st.subheader("Best & Worst Revenue Generator by Product Category")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
 
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
 
sns.barplot(x="price", y="product_category_name", hue="product_category_name", orient='h', data=sum_price_df(product_ordered_df).head(5), palette=colors, ax=ax[0], legend=False)
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Best Revenue Generator", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)
 
sns.barplot(x="price", y="product_category_name", hue="product_category_name", orient='h', data=sum_price_df(product_ordered_df).head(5).sort_values(by="price", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Revenue Generator", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)
 
st.pyplot(fig)