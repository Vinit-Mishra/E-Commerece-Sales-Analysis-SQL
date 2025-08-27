# E-Commerce Sales Analysis - SQL Project

## Project Overview
This project involves designing and implementing a complete relational database to model an e-commerce operation. Using SQL, I developed complex queries to analyze sales performance, customer behavior, and product trends, transforming raw data into actionable business intelligence.

## Database Schema & Design
The database is built with four normalized tables to ensure data integrity and efficiency:
- Customers: Customer details and demographics (customer_id, name, email, region, signup_date)
- Products: Product information, pricing, and inventory (product_id, product_name, category, price, stock_quantity)
- Orders: Order headers with status and totals (order_id, customer_id, order_date, total_amount, status)
- Order_Items: Individual products within each order (order_item_id, order_id, product_id, quantity, item_price)

## Technical Skills Demonstrated
- Database Design: Created normalized table structures with primary/foreign keys
- SQL Programming: Wrote complex queries using JOINs, aggregations, and filtering
- Data Analysis: Translated business questions into technical solutions
- Performance Optimization: Implemented indexes for query efficiency

## Key Insights Generated
The analysis answered critical business questions:
- Calculated total revenue from completed orders
- Identified best-selling products and top-performing categories
- Analyzed customer spending patterns and regional sales distribution
- Tracked monthly sales trends for performance monitoring

## How to Use
1. Clone this repository: git clone https://github.com/Vinit-Mishra/E-Commerece-Sales-Analysis-SQL.git
2. Execute the SQL files in sequence:
   - First run schema.sql to create the database structure
   - Then run sample_data.sql to populate with sample data
   - Finally run queries.sql to perform the analysis

## Files Included
- schema.sql - Database and table creation scripts
- sample_data.sql - Sample data insertion queries
- queries.sql - Analytical SQL queries for business insights
- README.md - Project documentation (this file)

## Database Relations
Customers (1) ───── (∞) Orders (1) ───── (∞) Order_Items (∞) ───── (1) Products

## Sample Queries
- Total revenue calculation
- Best-selling products analysis
- Top customers by spending
- Regional sales performance
- Monthly sales trends
