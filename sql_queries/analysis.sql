-- 1. Έλεγχος: Πόσες εγγραφές έχουμε συνολικά ανά πίνακα;
--order table
SELECT COUNT(*) AS total_orders FROM dbo.[order];
--user table 
SELECT COUNT(*) AS total_users FROM dbo.[user];
--seller table
SELECT COUNT(*) AS total_sellers FROM dbo.[seller];
--product table
SELECT COUNT(*) AS total_products FROM dbo.[product];
--category table
SELECT COUNT(*) AS total_categories FROM dbo.[category];


-- 2. Top 5 Χρήστες με τις υψηλότερες αγορές
SELECT  TOP(5) u.id , u.username ,SUM(price_at_purchase) AS total_spent
FROM dbo.[user] u
JOIN dbo.[order] o ON o.user_id = u.id 
GROUP BY u.id , u.username
ORDER BY total_spent DESC ;



-- 3. Πιο παλιοι χρήστες προς πιο νέους χρήστες
SELECT id , username , created_at
FROM dbo.[user]
ORDER BY created_at ASC;




-- 4. Μέσος όρος συναλλαγών ανά μήνα
SELECT AVG(price_at_purchase) as avg_purchase_per_month , MONTH(order_date) AS month_name
FROM dbo.[order]
GROUP BY MONTH(order_date);




-- 5. Ποιο είναι το ποσοστό των ενεργών χρηστών (π.χ. χρήστες που έχουν κάνει τουλάχιστον μία αγορά) σε σχέση με το συνολικό αριθμό χρηστών;
SELECT 
    (SELECT COUNT(DISTINCT user_id) FROM dbo.[order]) * 100.0 / (SELECT COUNT(*) FROM dbo.[user]) AS active_user_percentage;




-- 6. Ποια είναι η μέση αξία των αγορών ανά κατηγορία προϊόντων;
SELECT c.name AS category_name, AVG(o.price_at_purchase) AS avg_purchase_value
FROM dbo.[order] o
JOIN dbo.[product] p ON o.product_id = p.id
JOIN dbo.[category] c ON p.category_id = c.id
GROUP BY c.name;




-- 7. Ποια είναι η πιο δημοφιλής κατηγορία προϊόντων (με βάση τον αριθμό των αγορών);
SELECT  c.name AS category_name, COUNT(*) AS purchase_count
FROM dbo.[order] o
JOIN dbo.[product] p ON o.product_id = p.id
JOIN dbo.[category] c ON p.category_id = c.id
GROUP BY c.name
ORDER BY purchase_count DESC;




-- 8. Ποια είναι η μέση διάρκεια μεταξύ της εγγραφής ενός χρήστη και της πρώτης του αγοράς;
SELECT AVG(DATEDIFF(day, u.created_at, o.order_date)) AS avg_days_to_first_purchase
FROM dbo.[user] u
JOIN dbo.[order] o ON u.id = o.user_id;
