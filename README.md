
<img src="https://github.com/pelinsayar/images/blob/main/1*sZgsc3oGc7B8-jqKbqkQSw.png" width="600" height="350"/>   

---

# Customer Lifetime Value (CLTV) Prediction

This project is a CLTV prediction application that combines the **BG/NBD** and **Gamma-Gamma** models to estimate the total monetary value customers may bring to a business. Using a real dataset, the project analyzes customer purchase frequencies and average spending per transaction to calculate the future monetary contribution of each customer.

---

### **Project Aim**

This project aims to help businesses develop customer-focused strategies and optimize decision-making processes using data-driven insights. By analyzing Customer Lifetime Value (CLTV), the project provides:
- A focus on **high-value customers**,  
- Strategies to **increase loyalty among low-value customers**,  
- Accurate forecasts of future sales and revenues.  

---

### **Dataset**

This project utilizes the **Online Retail II** dataset from the UCI Machine Learning Repository. The dataset includes transaction records of a UK-based retail company from 2009 to 2010. Key features include:
- **InvoiceNo:** Invoice number,  
- **StockCode:** Product code,  
- **Description:** Product description,  
- **Quantity:** Quantity of products sold,  
- **InvoiceDate:** Date of the invoice,  
- **UnitPrice:** Price per unit of the product,  
- **CustomerID:** Unique customer identifier,  
- **Country:** Customer's location.  

This dataset provides a rich source of information to understand customer behavior and perform CLTV predictions.

---

### **How It Works**

1. **Data Preprocessing:**
   - Missing and erroneous data were cleaned, and negative and zero values were filtered out.
   - Key metrics such as Recency, Frequency, and Monetary (RFM) were calculated for each customer.

2. **BG/NBD and Gamma-Gamma Models:**
   - **BG/NBD Model:** Used to estimate the expected purchase frequency of customers within a given period.
   - **Gamma-Gamma Model:** Used to predict the average monetary value per transaction for each customer.

3. **CLTV Calculation:**
   - Combined results from BG/NBD and Gamma-Gamma models were used to calculate the total Customer Lifetime Value (CLTV) for each customer over a specific period (e.g., 3 months).

4. **Segmentation:**
   - Customers were segmented into four groups ("A", "B", "C", "D") based on their CLTV values.
   - These segments provide actionable insights for targeted customer strategies.

---

### **Key Questions and Insights**

This project addresses several critical questions for understanding customer behaviors and values using BG/NBD and Gamma-Gamma models. For instance:
- Who are the customers expected to make the most purchases within a given period?  
- What is the expected total number of sales for the company over a given period?  
- Which customers are predicted to generate the highest average profit per transaction?  

By answering these questions, businesses can identify opportunities to focus on high-potential customers and design loyalty-boosting strategies for lower-value ones.

Lastly; If you're interested in exploring the article I wrote about CLTV, where I explain my project step by step, feel free to take a look: (https://lnkd.in/dmmFDB4D)
