CREATE DATABASE ECOMMERCE;
USE ECOMMERCE;

CREATE TABLE Customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    region VARCHAR(50),
    signup_date DATE,
    INDEX idx_region (region)
);

CREATE TABLE Products (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    price DECIMAL(10,2) NOT NULL,
    stock_quantity INT DEFAULT 0,
    INDEX idx_category (category)
);

CREATE TABLE Orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT,
    order_date DATE NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'Pending',
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
    INDEX idx_order_date (order_date),
    INDEX idx_status (status)
);

CREATE TABLE Order_Items (
    order_item_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT,
    product_id INT,
    quantity INT NOT NULL DEFAULT 1,
    item_price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

-- Insert more comprehensive sample data
INSERT INTO Customers (name, email, region, signup_date) VALUES
('Alice', 'alice@example.com', 'New York', '2022-01-10'),
('Bob', 'bob@example.com', 'California', '2022-02-15'),
('Charlie', 'charlie@example.com', 'Texas', '2022-03-12'),
('Diana', 'diana@example.com', 'New York', '2022-04-20'),
('Evan', 'evan@example.com', 'California', '2022-05-05');

INSERT INTO Products (product_name, category, price, stock_quantity) VALUES
('iPhone 14', 'Electronics', 999.99, 50),
('MacBook Pro', 'Electronics', 1999.99, 30),
('AirPods', 'Electronics', 199.99, 100),
('Nike Shoes', 'Fashion', 120.00, 200),
('Samsung TV', 'Electronics', 799.99, 40),
('Levi Jeans', 'Fashion', 59.99, 150);

INSERT INTO Orders (customer_id, order_date, total_amount, status) VALUES
(1, '2023-01-15', 1199.99, 'Completed'),
(2, '2023-02-20', 1999.99, 'Completed'),
(1, '2023-03-05', 199.99, 'Completed'),
(3, '2023-03-15', 120.00, 'Cancelled'),
(4, '2023-03-20', 799.99, 'Completed'),
(5, '2023-04-10', 179.97, 'Completed'),
(1, '2023-04-15', 239.98, 'Completed');

INSERT INTO Order_Items (order_id, product_id, quantity, item_price) VALUES
(1, 1, 1, 999.99),
(1, 3, 1, 199.99),
(2, 2, 1, 1999.99),
(3, 3, 1, 199.99),
(4, 4, 1, 120.00),
(5, 5, 1, 799.99),
(6, 3, 3, 199.99),
(7, 4, 2, 120.00);

-- Your existing analysis queries (they work correctly)

-- Average order value
SELECT AVG(total_amount) AS avg_order_value
FROM Orders
WHERE status = 'Completed';

-- Customer retention rate (customers with more than one order)
SELECT COUNT(*) AS returning_customers
FROM (
    SELECT customer_id
    FROM Orders
    WHERE status = 'Completed'
    GROUP BY customer_id
    HAVING COUNT(*) > 1
) AS returning_customers;

-- Category performance
SELECT p.category, SUM(oi.quantity) AS total_sold, SUM(oi.quantity * oi.item_price) AS total_revenue
FROM Order_Items oi
JOIN Products p ON oi.product_id = p.product_id
JOIN Orders o ON oi.order_id = o.order_id
WHERE o.status = 'Completed'
GROUP BY p.category
ORDER BY total_revenue DESC;