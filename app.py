import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px
from mysql.connector import Error

# Page configuration
st.set_page_config(page_title="E-Commerce Sales Dashboard", page_icon="📊", layout="wide")

# Title and description
st.title("📊 E-Commerce Sales Analysis Dashboard")
st.markdown("Interactive dashboard for analyzing e-commerce sales data")

# Database connection function
@st.cache_resource
def init_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Add your password if needed
        database="ECOMMERCE"
    )

conn = init_connection()

# Function to run queries
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        result = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        return pd.DataFrame(result, columns=columns)

# Create database and tables if they don't exist
def setup_database():
    setup_queries = [
        "CREATE DATABASE IF NOT EXISTS ECOMMERCE",
        "USE ECOMMERCE",
        """CREATE TABLE IF NOT EXISTS Customers (
            customer_id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            region VARCHAR(50),
            signup_date DATE
        )""",
        """CREATE TABLE IF NOT EXISTS Products (
            product_id INT PRIMARY KEY AUTO_INCREMENT,
            product_name VARCHAR(100) NOT NULL,
            category VARCHAR(50),
            price DECIMAL(10,2) NOT NULL,
            stock_quantity INT DEFAULT 0
        )""",
        """CREATE TABLE IF NOT EXISTS Orders (
            order_id INT PRIMARY KEY AUTO_INCREMENT,
            customer_id INT,
            order_date DATE NOT NULL,
            total_amount DECIMAL(10,2) NOT NULL,
            status VARCHAR(20) DEFAULT 'Pending',
            FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
        )""",
        """CREATE TABLE IF NOT EXISTS Order_Items (
            order_item_id INT PRIMARY KEY AUTO_INCREMENT,
            order_id INT,
            product_id INT,
            quantity INT NOT NULL DEFAULT 1,
            item_price DECIMAL(10,2) NOT NULL,
            FOREIGN KEY (order_id) REFERENCES Orders(order_id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES Products(product_id)
        )"""
    ]
    
    with conn.cursor() as cur:
        for query in setup_queries:
            try:
                cur.execute(query)
            except Exception as e:
                st.error(f"Error executing query: {query}\nError: {e}")
        conn.commit()

# Insert sample data
def insert_sample_data():
    # Check if data already exists to avoid duplicates
    check_query = "SELECT COUNT(*) FROM Customers"
    with conn.cursor() as cur:
        cur.execute(check_query)
        count = cur.fetchone()[0]
        
    if count == 0:
        sample_data_queries = [
            "INSERT INTO Customers (name, email, region, signup_date) VALUES ('Alice', 'alice@example.com', 'New York', '2022-01-10')",
            "INSERT INTO Customers (name, email, region, signup_date) VALUES ('Bob', 'bob@example.com', 'California', '2022-02-15')",
            "INSERT INTO Customers (name, email, region, signup_date) VALUES ('Charlie', 'charlie@example.com', 'Texas', '2022-03-12')",
            "INSERT INTO Products (product_name, category, price, stock_quantity) VALUES ('iPhone 14', 'Electronics', 999.99, 50)",
            "INSERT INTO Products (product_name, category, price, stock_quantity) VALUES ('MacBook Pro', 'Electronics', 1999.99, 30)",
            "INSERT INTO Products (product_name, category, price, stock_quantity) VALUES ('AirPods', 'Electronics', 199.99, 100)",
            "INSERT INTO Products (product_name, category, price, stock_quantity) VALUES ('Nike Shoes', 'Fashion', 120.00, 200)",
            "INSERT INTO Orders (customer_id, order_date, total_amount, status) VALUES (1, '2023-01-15', 1199.99, 'Completed')",
            "INSERT INTO Orders (customer_id, order_date, total_amount, status) VALUES (2, '2023-02-20', 1999.99, 'Completed')",
            "INSERT INTO Orders (customer_id, order_date, total_amount, status) VALUES (1, '2023-03-05', 199.99, 'Completed')",
            "INSERT INTO Order_Items (order_id, product_id, quantity, item_price) VALUES (1, 1, 1, 999.99)",
            "INSERT INTO Order_Items (order_id, product_id, quantity, item_price) VALUES (1, 3, 1, 199.99)",
            "INSERT INTO Order_Items (order_id, product_id, quantity, item_price) VALUES (2, 2, 1, 1999.99)"
        ]
        
        with conn.cursor() as cur:
            for query in sample_data_queries:
                try:
                    cur.execute(query)
                except Exception as e:
                    st.error(f"Error inserting data: {query}\nError: {e}")
            conn.commit()
        st.success("Sample data inserted successfully!")
    else:
        st.info("Sample data already exists in the database")

# Initialize database
setup_database()
insert_sample_data()

# Sidebar filters
st.sidebar.header("Filters")
min_date = run_query("SELECT MIN(order_date) FROM Orders WHERE status = 'Completed'").iloc[0,0]
max_date = run_query("SELECT MAX(order_date) FROM Orders WHERE status = 'Completed'").iloc[0,0]

start_date = st.sidebar.date_input("Start date", min_date)
end_date = st.sidebar.date_input("End date", max_date)

# Main dashboard
col1, col2, col3 = st.columns(3)

with col1:
    # Total Revenue
    revenue_df = run_query(f"""
        SELECT SUM(total_amount) AS total_revenue
        FROM Orders
        WHERE status = 'Completed'
        AND order_date BETWEEN '{start_date}' AND '{end_date}'
    """)
    st.metric("Total Revenue", f"${revenue_df.iloc[0,0]:,.2f}")

with col2:
    # Total Orders
    orders_df = run_query(f"""
        SELECT COUNT(*) AS total_orders
        FROM Orders
        WHERE status = 'Completed'
        AND order_date BETWEEN '{start_date}' AND '{end_date}'
    """)
    st.metric("Total Orders", orders_df.iloc[0,0])

with col3:
    # Average Order Value
    aov_df = run_query(f"""
        SELECT AVG(total_amount) AS avg_order_value
        FROM Orders
        WHERE status = 'Completed'
        AND order_date BETWEEN '{start_date}' AND '{end_date}'
    """)
    st.metric("Average Order Value", f"${aov_df.iloc[0,0]:,.2f}")

# Charts
col1, col2 = st.columns(2)

with col1:
    # Sales by Category
    st.subheader("Sales by Category")
    category_df = run_query(f"""
        SELECT p.category, SUM(oi.quantity * oi.item_price) AS total_revenue
        FROM Order_Items oi
        JOIN Products p ON oi.product_id = p.product_id
        JOIN Orders o ON oi.order_id = o.order_id
        WHERE o.status = 'Completed'
        AND o.order_date BETWEEN '{start_date}' AND '{end_date}'
        GROUP BY p.category
        ORDER BY total_revenue DESC
    """)
    if not category_df.empty:
        fig = px.pie(category_df, values='total_revenue', names='category', 
                    title='Revenue by Category')
        st.plotly_chart(fig, use_container_width=True)

with col2:
    # Monthly Sales Trend
    st.subheader("Monthly Sales Trend")
    monthly_df = run_query(f"""
        SELECT DATE_FORMAT(order_date, '%Y-%m') AS month, 
               SUM(total_amount) AS monthly_sales
        FROM Orders
        WHERE status = 'Completed'
        AND order_date BETWEEN '{start_date}' AND '{end_date}'
        GROUP BY month
        ORDER BY month
    """)
    if not monthly_df.empty:
        fig = px.line(monthly_df, x='month', y='monthly_sales', 
                     title='Monthly Sales Trend', markers=True)
        st.plotly_chart(fig, use_container_width=True)

# Top Products
st.subheader("Top Selling Products")
top_products_df = run_query(f"""
    SELECT p.product_name, SUM(oi.quantity) AS total_sold
    FROM Order_Items oi
    JOIN Products p ON oi.product_id = p.product_id
    JOIN Orders o ON oi.order_id = o.order_id
    WHERE o.status = 'Completed'
    AND o.order_date BETWEEN '{start_date}' AND '{end_date}'
    GROUP BY p.product_name
    ORDER BY total_sold DESC
    LIMIT 10
""")
st.dataframe(top_products_df, use_container_width=True)

# Top Customers
st.subheader("Top Customers")
top_customers_df = run_query(f"""
    SELECT c.name, SUM(o.total_amount) AS total_spent
    FROM Customers c
    JOIN Orders o ON c.customer_id = o.customer_id
    WHERE o.status = 'Completed'
    AND o.order_date BETWEEN '{start_date}' AND '{end_date}'
    GROUP BY c.name
    ORDER BY total_spent DESC
    LIMIT 10
""")
st.dataframe(top_customers_df, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("Built with Streamlit & MySQL | E-Commerce Sales Analysis Dashboard")