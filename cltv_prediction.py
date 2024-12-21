#  BG-NBD ve Gamma-Gamma ile CLTV Prediction

# Variables in the Dataset:
# - InvoiceNo: Invoice number.
# - StockCode: Product code. A unique number for each product.
# - Description: Product name.
# - Quantity: Quantity of the product. Indicates how many units of the products were sold in each invoice.
# - InvoiceDate: Invoice date and time.
# - UnitPrice: Product price.
# - CustomerID: Unique customer number.
# - Country: Country name. Refers to the country where the customer resides.

# Customer Value = Purchase Frequency * Average Order Value
# CLTV Prediction = Expected Number of Transaction * Expected Average Profit
# CLTV = BG/NBD Model * Gamma Gamma Submodel


##########################
# Required Library and Functions
##########################

# !pip install lifetimes

import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt

from lifetimes import BetaGeoFitter
from lifetimes import GammaGammaFitter
from lifetimes.plotting import plot_period_transactions

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
pd.set_option('display.float_format', lambda x: '%.4f' % x)
from sklearn.preprocessing import MinMaxScaler


def outlier_thresholds(dataframe, variable):
    quartile1 = dataframe[variable].quantile(0.01)
    quartile3 = dataframe[variable].quantile(0.99)
    interquantile_range = quartile3 - quartile1
    up_limit = quartile3 + 1.5 * interquantile_range
    low_limit = quartile1 - 1.5 * interquantile_range
    return low_limit, up_limit


def replace_with_thresholds(dataframe, variable):
    low_limit, up_limit = outlier_thresholds(dataframe, variable)
    dataframe.loc[(dataframe[variable] < low_limit), variable] = low_limit
    dataframe.loc[(dataframe[variable] > up_limit), variable] = up_limit


#########################
# Verinin Okunması
#########################

df_ = pd.read_excel("rfm/online_retail_II.xlsx", sheet_name="Year 2010-2011")

df = df_.copy()

df.head()
df.describe().T
df.isnull().sum()


#########################
# Veri Ön İşleme
#########################

df.dropna(inplace=True)

df["Invoice"] = df["Invoice"].astype(str)
df = df[~df["Invoice"].str.contains("C", na=False)]

df = df[df["Quantity"] > 0]
df = df[df["Price"] > 0]

replace_with_thresholds(df, "Quantity")
replace_with_thresholds(df, "Price")

df["TotalPrice"] = df["Quantity"] * df["Price"]

df["InvoiceDate"].max()  # 2011-12-09
today_date = dt.datetime(2011, 12, 11)  # analysis day


#########################
# Lifetime Veri Yapısının Hazırlanması
#########################

cltv_df = df.groupby("Customer ID").agg(
    {"InvoiceDate": [lambda x: (x.max() - x.min()).days,
                     lambda x: (today_date - x.min()).days],
     "Invoice": lambda y: y.nunique(),
     "TotalPrice": lambda z: z.sum()})

cltv_df.columns = cltv_df.columns.droplevel(0)

cltv_df.columns = ['recency', 'T', 'frequency', 'monetary']

cltv_df["monetary"] = cltv_df["monetary"] / cltv_df["frequency"]

cltv_df = cltv_df[(cltv_df["frequency"] > 1)]

cltv_df["recency"] = cltv_df["recency"] / 7

cltv_df["T"] = cltv_df["T"] / 7


##############################################################
# 2. BG-NBD Modelinin Kurulması (Beklenen satın alma sayısı)
##############################################################

# CLTV = BG/NBD Model * Gamma Gamma Submodel

bgf = BetaGeoFitter(penalizer_coef=0.001)

bgf.fit(cltv_df['frequency'],
        cltv_df['recency'],
        cltv_df['T'])


################################################################
# 1 hafta içinde en çok satın alma beklediğimiz 10 müşteri kimdir?
################################################################

bgf.conditional_expected_number_of_purchases_up_to_time(1,  # 1 week
                                                        cltv_df['frequency'],
                                                        cltv_df['recency'],
                                                        cltv_df['T']).sort_values(ascending=False).head(10)


bgf.predict(1,  # 1 week
            cltv_df['frequency'],
            cltv_df['recency'],
            cltv_df['T']).sort_values(ascending=False).head(10)

cltv_df["expected_purc_1_week"] = bgf.predict(1,  # 1 week
                                              cltv_df['frequency'],
                                              cltv_df['recency'],
                                              cltv_df['T'])


################################################################
# 1 ay içinde en çok satın alma beklediğimiz 10 müşteri kimdir?
################################################################

bgf.predict(4,  # 4 weeks
            cltv_df['frequency'],
            cltv_df['recency'],
            cltv_df['T']).sort_values(ascending=False).head(10)

cltv_df["expected_purc_1_month"] = bgf.predict(4,  # 4 weeks
                                               cltv_df['frequency'],
                                               cltv_df['recency'],
                                               cltv_df['T'])

bgf.predict(4,  # 4 weeks
            cltv_df['frequency'],
            cltv_df['recency'],
            cltv_df['T']).sum()


################################################################
# 3 Ayda Tüm Şirketin Beklenen Satış Sayısı Nedir?
################################################################

(bgf.predict(4 * 3,
             cltv_df['frequency'],
             cltv_df['recency'],
             cltv_df['T']).sum())

cltv_df["expected_purc_3_month"] = bgf.predict(4 * 3,
                                               cltv_df['frequency'],
                                               cltv_df['recency'],
                                               cltv_df['T'])


################################################################
# Tahmin Sonuçlarının Değerlendirilmesi
################################################################

plot_period_transactions(bgf)
plt.show()


##############################################################
# 3. GAMMA-GAMMA Modelinin Kurulması (Average Profit'i modeller)
##############################################################

ggf = GammaGammaFitter(penalizer_coef=0.01)

ggf.fit(cltv_df['frequency'],
        cltv_df['monetary'])

ggf.conditional_expected_average_profit(cltv_df['frequency'],
                                        cltv_df['monetary']).head(10)

ggf.conditional_expected_average_profit(cltv_df['frequency'],
                                        cltv_df['monetary']).sort_values(ascending=False).head(10)

cltv_df["expected_average_profit"] = ggf.conditional_expected_average_profit(cltv_df['frequency'],
                                                                             cltv_df['monetary'])

cltv_df.sort_values("expected_average_profit", ascending=False).head(10)


##############################################################
# 4. BG-NBD ve GG modeli ile CLTV'nin hesaplanması.
##############################################################

cltv = ggf.customer_lifetime_value(bgf,
                                   cltv_df['frequency'],
                                   cltv_df['recency'],
                                   cltv_df['T'],
                                   cltv_df['monetary'],
                                   time=3,  # 3 months
                                   freq="W",  # Week (W)
                                   discount_rate=0.01)


##############################################################
# 5. CLTV'ye Göre Segmentlerin Oluşturulması
##############################################################

cltv = cltv.reset_index()

cltv["segment"] = pd.qcut(cltv["clv"], 4, labels=["D", "C", "B", "A"])

cltv.sort_values(by="clv", ascending=False).head(50)

cltv.groupby("segment").agg({"count", "mean", "sum"})



