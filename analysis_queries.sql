CREATE DATABASE trip_expense_db;
USE trip_expense_db;

ALTER TABLE trip_exp
ADD COLUMN New_Date DATE;
SET SQL_SAFE_UPDATES = 0;
UPDATE trip_exp
SET New_Date = STR_TO_DATE(Date, '%d-%m-%Y');
SET SQL_SAFE_UPDATES = 1;

SELECT * 
FROM trip_exp;

SELECT count(*) 
FROM trip_exp;

SELECT * 
FROM trip_exp 
WHERE cost is null;

#Total Trip Cost
SELECT ROUND(SUM(cost),2) as Total_Trip_Cost 
FROM trip_exp;

#Total Transactions
SELECT COUNT(*) AS Transactions
FROM trip_exp;

#Average Expense
SELECT ROUND(AVG(Cost),2)
FROM trip_exp;

#Top 5 highest expense
SELECT *
FROM trip_exp
ORDER BY Cost DESC
LIMIT 5;

#Spending by Category
SELECT `Expense Category`,ROUND(SUM(Cost),2) AS Total_Spent
FROM trip_exp
GROUP BY `Expense Category`
ORDER BY Total_Spent DESC;

#Paying Amount per person
SELECT `Paid by`,ROUND(SUM(Cost),2) AS Total_Paid
FROM trip_exp
GROUP BY `Paid by`
ORDER BY Total_Paid DESC;

#Daily Spending
SELECT New_Date,ROUND(SUM(Cost),2) AS Daily_Spending
FROM trip_exp
GROUP BY New_Date
ORDER BY New_Date;

#Category Contribution by %
SELECT `Expense Category`, ROUND(100*SUM(Cost)/(SELECT SUM(Cost) FROM trip_exp),2) AS Contribution_Percent
FROM trip_exp
GROUP BY `Expense Category`
ORDER BY Contribution_Percent DESC;

#Running Total
SELECT
New_Date,
SUM(Cost) AS Daily_Spending,
SUM(SUM(Cost))
OVER(ORDER BY New_Date)
AS Running_Total
FROM trip_exp
GROUP BY New_Date;

#Top 3 expenses in each category
with trip as(SELECT
        `Expense Category`,
        Description,
        Cost,
        ROW_NUMBER() OVER(
            PARTITION BY `Expense Category`
            ORDER BY Cost DESC) as rank_no from trip_exp)
select *  from trip where rank_no<=3;

#Expense Bucketing
SELECT
    Description,
    Cost,
    CASE
        WHEN Cost < 100 THEN 'Low'
        WHEN Cost < 1000 THEN 'Medium'
        ELSE 'High'
    END AS Expense_Level
FROM trip_exp;