/*
==========================================================
RetailNova Decision Intelligence Platform
Master Seed Data

File        : master_data.sql
Description : Populates all master/reference tables.

Execution Order
1. Category
2. Brand
3. Supplier
4. Location

Author      : Hardik Narigra
Database    : PostgreSQL 17
==========================================================
*/

BEGIN;

-- ======================================================
-- CATEGORY
-- ======================================================

INSERT INTO category
(
    category_name,
    description
)
VALUES
('Electronics', 'Smartphones, laptops, televisions, audio devices and electronic accessories.'),
('Fashion', 'Men''s, women''s and children''s clothing, footwear and fashion accessories.'),
('Grocery', 'Daily essentials, packaged foods, beverages and household consumables.'),
('Home & Kitchen', 'Furniture, cookware, home appliances and kitchen essentials.'),
('Beauty & Personal Care', 'Cosmetics, skincare, haircare and personal hygiene products.'),
('Sports & Fitness', 'Sports equipment, fitness accessories and outdoor gear.'),
('Toys & Games', 'Educational toys, board games and entertainment products for children.'),
('Books & Stationery', 'Books, notebooks, office stationery and educational supplies.'),
('Automotive', 'Vehicle accessories, maintenance products and travel essentials.'),
('Pet Supplies', 'Pet food, grooming products, toys and accessories.'),
('Health & Wellness', 'Healthcare, nutrition and wellness products.'),
('Jewellery & Watches', 'Fashion jewellery, premium watches and accessories.'),
('Baby Products', 'Infant care, diapers, feeding and baby accessories.'),
('Office Supplies', 'Office furniture, printers, business stationery and workplace essentials.'),
('Smart Home', 'IoT devices, smart lighting, security systems and home automation.');

-- ======================================================
-- BRAND
-- ======================================================

INSERT INTO brand
(
    brand_name,
    description
)
VALUES
-- Electronics
('Apple', 'Premium consumer electronics and smart devices.'),
('Samsung', 'Consumer electronics, smartphones and home appliances.'),
('Sony', 'Entertainment, electronics and gaming products.'),
('LG', 'Home appliances, televisions and electronics.'),
('Dell', 'Computers, laptops and enterprise technology.'),
('HP', 'Computers, printers and business technology solutions.'),
('Lenovo', 'Laptops, desktops and computing devices.'),
('ASUS', 'Gaming laptops, computers and accessories.'),
('Acer', 'Affordable computing and electronic products.'),
('boAt', 'Indian consumer electronics and audio accessories.'),

-- Fashion
('Nike', 'Sportswear, footwear and athletic accessories.'),
('Adidas', 'Global sportswear and lifestyle brand.'),
('Puma', 'Sports apparel and footwear.'),
('Levi''s', 'Denim apparel and casual fashion.'),
('Allen Solly', 'Premium formal and casual clothing.'),
('FabIndia', 'Ethnic wear and handcrafted lifestyle products.'),
('Raymond', 'Formal wear and premium textiles.'),
('Van Heusen', 'Business and formal fashion apparel.'),

-- Beauty & Personal Care
('Lakmé', 'Indian beauty and cosmetic products.'),
('Maybelline', 'International cosmetics and makeup brand.'),
('Himalaya', 'Herbal healthcare and personal care products.'),
('Nivea', 'Skincare and personal care products.'),
('Dove', 'Haircare, skincare and hygiene products.'),
('Mamaearth', 'Natural personal care and wellness products.'),

-- Home & Kitchen
('Prestige', 'Kitchen appliances and cookware.'),
('Philips', 'Consumer electronics and home appliances.'),
('Milton', 'Kitchenware, storage and insulated products.'),
('Cello', 'Household and office utility products.'),

-- Grocery & FMCG
('Amul', 'Dairy and food products.'),
('Britannia', 'Biscuits, bakery and dairy products.'),
('ITC', 'Packaged foods and FMCG products.'),
('Tata Consumer', 'Tea, coffee and packaged food products.'),
('Nestlé', 'Food, beverages and nutrition products.'),

-- Watches & Lifestyle
('Titan', 'Watches, jewellery and fashion accessories.'),

-- Stationery & Office
('Parker', 'Premium writing instruments.'),

-- Pet & Baby
('Pedigree', 'Pet food and nutrition products.'),
('Johnson''s Baby', 'Baby care and hygiene products.');

-- ======================================================
-- SUPPLIER
-- ======================================================

INSERT INTO supplier
(
    supplier_name,
    contact_person,
    email,
    phone_number,
    address,
    city,
    state,
    country,
    postal_code
)
VALUES
('Western India Distributors Pvt. Ltd.', 'Rahul Mehta', 'contact@westerndist.com', '+91-9876501001', '101 Business Park, Andheri East', 'Mumbai', 'Maharashtra', 'India', '400069'),

('Apex Wholesale Solutions', 'Priya Shah', 'sales@apexwholesale.com', '+91-9876501002', '45 Industrial Estate', 'Pune', 'Maharashtra', 'India', '411019'),

('Prime Retail Supply Co.', 'Arjun Rao', 'support@primeretail.com', '+91-9876501003', '12 Tech Park Road', 'Bengaluru', 'Karnataka', 'India', '560037'),

('Metro Distribution Network', 'Neha Kapoor', 'info@metrodistribution.com', '+91-9876501004', '88 Connaught Circle', 'New Delhi', 'Delhi', 'India', '110001'),

('Infinity Trade Partners', 'Suresh Reddy', 'sales@infinitytrade.com', '+91-9876501005', '22 HITEC City', 'Hyderabad', 'Telangana', 'India', '500081'),

('Smart Logistics Supply Chain', 'Anita Nair', 'contact@smartlogistics.com', '+91-9876501006', '55 Mount Road', 'Chennai', 'Tamil Nadu', 'India', '600002'),

('Bharat Wholesale Hub', 'Vikram Patel', 'sales@bharatwholesale.com', '+91-9876501007', '77 SG Highway', 'Ahmedabad', 'Gujarat', 'India', '380015'),

('Elite Consumer Goods Pvt. Ltd.', 'Sneha Das', 'support@eliteconsumer.com', '+91-9876501008', '15 Salt Lake Sector V', 'Kolkata', 'West Bengal', 'India', '700091'),

('Urban Supply Network', 'Rohan Sharma', 'contact@urbansupply.com', '+91-9876501009', '21 MI Road', 'Jaipur', 'Rajasthan', 'India', '302001'),

('National Retail Partners', 'Pooja Verma', 'sales@nrpartners.com', '+91-9876501010', '90 Hazratganj', 'Lucknow', 'Uttar Pradesh', 'India', '226001'),

('Eastern Commerce Solutions', 'Abhijit Deka', 'info@easterncommerce.com', '+91-9876501011', '5 GS Road', 'Guwahati', 'Assam', 'India', '781005'),

('Southern Trade Link', 'Deepa Menon', 'support@southerntrade.com', '+91-9876501012', '18 MG Road', 'Kochi', 'Kerala', 'India', '682016'),

('Horizon Distribution Services', 'Karan Joshi', 'contact@horizondist.com', '+91-9876501013', '11 Vijay Nagar', 'Indore', 'Madhya Pradesh', 'India', '452010'),

('Vertex Supply Chain', 'Manish Kulkarni', 'sales@vertexsupply.com', '+91-9876501014', '44 Sitabuldi', 'Nagpur', 'Maharashtra', 'India', '440012'),

('Nova Wholesale Traders', 'Harsh Patel', 'info@novawholesale.com', '+91-9876501015', '66 Ring Road', 'Surat', 'Gujarat', 'India', '395003'),

('Unity Distribution Co.', 'Simran Kaur', 'sales@unitydistribution.com', '+91-9876501016', '10 Sector 17', 'Chandigarh', 'Chandigarh', 'India', '160017'),

('GreenLeaf Consumer Supply', 'Nitin Mishra', 'contact@greenleafsupply.com', '+91-9876501017', '8 MP Nagar', 'Bhopal', 'Madhya Pradesh', 'India', '462011'),

('BluePeak Logistics', 'Akash Singh', 'support@bluepeaklogistics.com', '+91-9876501018', '14 Beach Road', 'Visakhapatnam', 'Andhra Pradesh', 'India', '530002'),

('Zenith Retail Suppliers', 'Meera Iyer', 'sales@zenithretail.com', '+91-9876501019', '25 Avinashi Road', 'Coimbatore', 'Tamil Nadu', 'India', '641018'),

('Sterling Trade Associates', 'Amit Kumar', 'info@sterlingtrade.com', '+91-9876501020', '32 Fraser Road', 'Patna', 'Bihar', 'India', '800001');

-- ======================================================
-- LOCATION
-- ======================================================

INSERT INTO location
(
    location_name,
    location_type,
    address,
    city,
    state,
    country,
    postal_code,
    phone_number
)
VALUES
-- WEST REGION
('Mumbai Central Store', 'STORE', 'Phoenix Marketcity, Kurla West', 'Mumbai', 'Maharashtra', 'India', '400070', '+91-22-40001001'),

('Navi Mumbai Warehouse', 'WAREHOUSE', 'TTC Industrial Area, Turbhe', 'Navi Mumbai', 'Maharashtra', 'India', '400705', '+91-22-40001002'),

('Pune Store', 'STORE', 'FC Road, Shivajinagar', 'Pune', 'Maharashtra', 'India', '411005', '+91-20-40001003'),

('Pune Warehouse', 'WAREHOUSE', 'Chakan Industrial Area', 'Pune', 'Maharashtra', 'India', '410501', '+91-20-40001004'),

('Ahmedabad Store', 'STORE', 'SG Highway', 'Ahmedabad', 'Gujarat', 'India', '380015', '+91-79-40001005'),

('Ahmedabad Warehouse', 'WAREHOUSE', 'Naroda GIDC', 'Ahmedabad', 'Gujarat', 'India', '382330', '+91-79-40001006'),

-- NORTH REGION
('Delhi Connaught Place Store', 'STORE', 'Connaught Place', 'New Delhi', 'Delhi', 'India', '110001', '+91-11-40001007'),

('Delhi Warehouse', 'WAREHOUSE', 'Okhla Industrial Area Phase II', 'New Delhi', 'Delhi', 'India', '110020', '+91-11-40001008'),

('Jaipur Store', 'STORE', 'MI Road', 'Jaipur', 'Rajasthan', 'India', '302001', '+91-141-40001009'),

('Lucknow Store', 'STORE', 'Hazratganj', 'Lucknow', 'Uttar Pradesh', 'India', '226001', '+91-522-40001010'),

-- SOUTH REGION
('Bengaluru Store', 'STORE', 'MG Road', 'Bengaluru', 'Karnataka', 'India', '560001', '+91-80-40001011'),

('Bengaluru Warehouse', 'WAREHOUSE', 'Electronic City Phase I', 'Bengaluru', 'Karnataka', 'India', '560100', '+91-80-40001012'),

('Hyderabad Store', 'STORE', 'Banjara Hills Road No. 1', 'Hyderabad', 'Telangana', 'India', '500034', '+91-40-40001013'),

('Chennai Store', 'STORE', 'Anna Salai', 'Chennai', 'Tamil Nadu', 'India', '600002', '+91-44-40001014'),

('Kochi Store', 'STORE', 'MG Road', 'Kochi', 'Kerala', 'India', '682016', '+91-484-40001015'),

-- EAST REGION
('Kolkata Store', 'STORE', 'Salt Lake Sector V', 'Kolkata', 'West Bengal', 'India', '700091', '+91-33-40001016'),

('Kolkata Warehouse', 'WAREHOUSE', 'Dankuni Logistics Park', 'Kolkata', 'West Bengal', 'India', '712311', '+91-33-40001017'),

('Bhubaneswar Store', 'STORE', 'Janpath Road', 'Bhubaneswar', 'Odisha', 'India', '751001', '+91-674-40001018'),

('Guwahati Store', 'STORE', 'GS Road', 'Guwahati', 'Assam', 'India', '781005', '+91-361-40001019'),

('Guwahati Warehouse', 'WAREHOUSE', 'Amingaon Industrial Area', 'Guwahati', 'Assam', 'India', '781031', '+91-361-40001020');

COMMIT;
