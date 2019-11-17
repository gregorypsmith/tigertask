PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE customer (
	id INTEGER NOT NULL, 
	name VARCHAR, 
	phone_number VARCHAR, 
	email VARCHAR, 
	password VARCHAR, 
	PRIMARY KEY (id)
);
INSERT INTO customer VALUES(1,'matt','12345','matt@matt','asldkfj');
CREATE TABLE deliverer (
	id INTEGER NOT NULL, 
	name VARCHAR, 
	phone_number VARCHAR, 
	email VARCHAR, 
	password VARCHAR, 
	PRIMARY KEY (id)
);
INSERT INTO deliverer VALUES(1,'peter','293847198734','peter','peter');
CREATE TABLE item (
	id INTEGER NOT NULL, 
	name VARCHAR, 
	price INTEGER, 
	category VARCHAR, 
	PRIMARY KEY (id)
);
INSERT INTO item VALUES(3,'Pure Silk Shave Cream - Coconut',2.6899999999999999467,'Toiletries');
INSERT INTO item VALUES(4,'Pure Silk Shave Cream - Raspberry',2.6899999999999999467,'Toiletries');
INSERT INTO item VALUES(5,'Pure Silk Shave Cream - Sensitive Skin',2.6899999999999999467,'Toiletries');
INSERT INTO item VALUES(6,'Pure Silk Shave Cream - Dry Skin',2.6899999999999999467,'Toiletries');
INSERT INTO item VALUES(7,'Gillette Mach3 Disposable Razors (3 Pack)',11.990000000000000212,'Toiletries');
INSERT INTO item VALUES(8,'Gillette Sensor2 Plus Disposable Razors (10 Pack)',13.789999999999999147,'Toiletries');
INSERT INTO item VALUES(9,'Gillette Fusion5 ProShield Razor',29.589999999999999857,'Toiletries');
INSERT INTO item VALUES(10,'Edge Extra Moisturizing Shaving Cream',4.2900000000000000355,'Toiletries');
INSERT INTO item VALUES(11,'Edge Ultra Sensitive Shaving Cream',4.2900000000000000355,'Toiletries');
INSERT INTO item VALUES(12,'Edge Soothing Aloe Shaving Cream',4.2900000000000000355,'Toiletries');
INSERT INTO item VALUES(13,'Tampax Pearl Super Tampons (36 pack)',9.9900000000000002131,'Toiletries');
INSERT INTO item VALUES(14,'Tampax Pearl Super Plus Tampons (36 pack)',9.9900000000000002131,'Toiletries');
INSERT INTO item VALUES(15,'Kotex lightdays Plus Absorbent Liners (40 pack)',3.9900000000000002131,'Toiletries');
INSERT INTO item VALUES(16,'Stayfree Regular Maxipads (24 pack)',4.2900000000000000355,'Toiletries');
INSERT INTO item VALUES(17,'Everyone for Everybody Soap, Coconut + Lemon',8,'Toiletries');
INSERT INTO item VALUES(18,'Everyone for Everybody Soap, Mint + Coconut',8,'Toiletries');
INSERT INTO item VALUES(19,'Old Spice High Endurance Bodywash',5.9900000000000002131,'Toiletries');
INSERT INTO item VALUES(20,'Old Spice High Endurance 2 in 1 Bodywash/Shampoo',5.9900000000000002131,'Toiletries');
INSERT INTO item VALUES(21,'Old Spice Krakengard Bodywash',7.2900000000000000355,'Toiletries');
INSERT INTO item VALUES(22,'Dial Odor Armor Body Wash',6.7900000000000000355,'Toiletries');
INSERT INTO item VALUES(23,'Axe Excite Body Wash',6.7900000000000000355,'Toiletries');
INSERT INTO item VALUES(24,'Reach Mint Waxed Floss',1.9899999999999999911,'Toiletries');
INSERT INTO item VALUES(25,'Reach Waxed Floss',1.9899999999999999911,'Toiletries');
INSERT INTO item VALUES(26,'Oral-B INDICATOR Contour-Clean Toothbrush',2.9900000000000002131,'Toiletries');
INSERT INTO item VALUES(27,'Oral-B Cavity Defense Toothbrush',2.1899999999999999467,'Toiletries');
INSERT INTO item VALUES(28,'Crest Plus Scope Outlast Toothpaste',4.3899999999999996802,'Toiletries');
INSERT INTO item VALUES(29,'Crest ProHealth Whitening Toothpaste',5.9900000000000002131,'Toiletries');
INSERT INTO item VALUES(30,'Listerine Cool Mint Mouthwash 500mL',5.3899999999999996802,'Toiletries');
INSERT INTO item VALUES(31,'Trojan Magnum thin Condoms (3ct)',3.8900000000000001243,'Toiletries');
INSERT INTO item VALUES(32,'Trojan ENZ Non-Lubricated Condoms (3ct)',1.9899999999999999911,'Toiletries');
INSERT INTO item VALUES(33,'Trojan Fire & Ice Condoms (3ct)',3.8900000000000001243,'Toiletries');
INSERT INTO item VALUES(34,'Hall''s Relief Cough Drops, Honey Lemon',2.4900000000000002131,'Medicine');
INSERT INTO item VALUES(35,'Hall''s Relief Cough Drops, Cool Berry',2.4900000000000002131,'Medicine');
INSERT INTO item VALUES(36,'Hall''s Relief Cough Drops, Tropical Fruit',2.4900000000000002131,'Medicine');
INSERT INTO item VALUES(37,'Advil Ibuprofen Tablets, 100 Caps',12.990000000000000212,'Medicine');
INSERT INTO item VALUES(38,'Aspirin, 36 Tablets',1.8899999999999999023,'Medicine');
INSERT INTO item VALUES(39,'Tylenol Liquid Gels, 90 ct',13.589999999999999857,'Medicine');
INSERT INTO item VALUES(40,'TUMS Assorted Fruit Antacid, 90ct',4.8899999999999996802,'Medicine');
INSERT INTO item VALUES(41,'Band-Aid Tough Strips, 20ct',4.3899999999999996802,'Medicine');
INSERT INTO item VALUES(42,'Band-Aid Skin-Flex Extra Large Bandages, 7ct',4.3899999999999996802,'Medicine');
INSERT INTO item VALUES(43,'Wet Ones Single Hand Wipes, 24ct',3.5899999999999998578,'Cleaning');
INSERT INTO item VALUES(44,'Brazilian Keratin Therapy Shampoo',8.3900000000000005684,'Toiletries');
INSERT INTO item VALUES(45,'TRESemme Moisture Rich Moisturizer',5.4900000000000002131,'Toiletries');
INSERT INTO item VALUES(46,'TRESemme Anti-Breakage Moisturrizer',5.4900000000000002131,'Toiletries');
INSERT INTO item VALUES(47,'TRESemme Keratin Smooth Shampoo',6.9900000000000002131,'Toiletries');
INSERT INTO item VALUES(48,'Whole Blends Smoothing Conditioner',4.6500000000000003552,'Toiletries');
INSERT INTO item VALUES(49,'Whole Blends Smoothing Shampoo',4.6500000000000003552,'Toiletries');
INSERT INTO item VALUES(50,'Head & Shoulders Dry Scalp Care 2 in 1 Shampoo',7.9900000000000002131,'Toiletries');
INSERT INTO item VALUES(51,'Clorox Disinfecting Wet Wipes, Lemon (35ct)',3.5899999999999998578,'Cleaning');
INSERT INTO item VALUES(52,'Clorox Disinfecting Wet Wipes, Tuscan Lavender & Jasmine (35ct)',3.5899999999999998578,'Cleaning');
INSERT INTO item VALUES(53,'Clorox Cleaner & Bleach Spray',4.9900000000000002131,'Cleaning');
INSERT INTO item VALUES(54,'409 Multi-Surface Cleaner Spray',4.4900000000000002131,'Cleaning');
INSERT INTO item VALUES(55,'Tide Pods 3-in-1 (16ct)',16.390000000000000568,'Cleaning');
INSERT INTO item VALUES(56,'Tide Detergent Classic (29 loads)',10.990000000000000213,'Cleaning');
INSERT INTO item VALUES(57,'Tide Detergent Classic (64 loads)',19.989999999999998436,'Cleaning');
INSERT INTO item VALUES(58,'All Stainlifters Free & Clear Stain Remover (24 loads)',7.9900000000000002131,'Cleaning');
INSERT INTO item VALUES(59,'All Stainlifters Oder Lifterr (20 loads)',7.9900000000000002131,'Cleaning');
INSERT INTO item VALUES(60,'Poptarts Brown Sugar Cinnamon (8ct)',3.6899999999999999467,'Food');
INSERT INTO item VALUES(61,'Poptarts Blueberry (8ct)',3.6899999999999999467,'Food');
INSERT INTO item VALUES(62,'Poptarts Cupcake',3.6899999999999999467,'Food');
INSERT INTO item VALUES(63,'KIND Oats & Honey Clusters',6.9900000000000002131,'Food');
INSERT INTO item VALUES(64,'Jif Creamy Peanut Butter',4.5899999999999998578,'Food');
INSERT INTO item VALUES(65,'Jif Extra Chunky Peanut Butter',4.5899999999999998578,'Food');
INSERT INTO item VALUES(66,'Skippy Creamy Peanut Butter',4.4900000000000002131,'Food');
INSERT INTO item VALUES(67,'Skippy Extra Chunky Peanut Butter',4.4900000000000002131,'Food');
INSERT INTO item VALUES(68,'Smucker''s Squeeze Strawberry Jam',3.9900000000000002131,'Food');
INSERT INTO item VALUES(69,'Smucker''s Squeeze Grape Jam',3.9900000000000002131,'Food');
INSERT INTO item VALUES(70,'Nutella Hazelnut Spread',4.4900000000000002131,'Food');
INSERT INTO item VALUES(71,'Dole Diced Peaches (4ct)',3.2900000000000000355,'Food');
INSERT INTO item VALUES(72,'Dole Pineapple Tidbits (4ct)',3.2900000000000000355,'Food');
INSERT INTO item VALUES(73,'Welch''s Fruit Snacks Original (10ct)',3.2900000000000000355,'Food');
INSERT INTO item VALUES(74,'Fruit Gushers (6ct)',3.2900000000000000355,'Food');
INSERT INTO item VALUES(75,'Cup of Noodles, Beef Flavor',0.98999999999999999111,'Food');
INSERT INTO item VALUES(76,'Cup of Noodles, Hearty Chicken Flavor',0.98999999999999999111,'Food');
INSERT INTO item VALUES(77,'Nissin Hot & Spicy Bowl',1.4899999999999999911,'Food');
INSERT INTO item VALUES(78,'Dr. McDougall''s Vegan Soup',2.4900000000000002131,'Food');
INSERT INTO item VALUES(79,'Cheez-It Duos',4.9900000000000002131,'Food');
INSERT INTO item VALUES(80,'Cheez-It Cheddarr Jack',4.9900000000000002131,'Food');
INSERT INTO item VALUES(81,'Nissin Top Ramen',2.1899999999999999467,'Food');
INSERT INTO item VALUES(82,'Kraft Easy Mac & Cheese (6ct)',3.9900000000000002131,'Food');
INSERT INTO item VALUES(83,'Oreo Original',5.7900000000000000355,'Food');
INSERT INTO item VALUES(84,'Oreo Double Stuf',5.7900000000000000355,'Food');
INSERT INTO item VALUES(85,'Oreo Golden',5.7900000000000000355,'Food');
INSERT INTO item VALUES(86,'Chips Ahoy Original',4.7900000000000000355,'Food');
INSERT INTO item VALUES(87,'Goldfish Original',2.4900000000000002131,'Food');
INSERT INTO item VALUES(88,'Goldfish Colorrs',2.4900000000000002131,'Food');
INSERT INTO item VALUES(89,'Goldfish Baked',2.4900000000000002131,'Food');
INSERT INTO item VALUES(90,'Goldfish Flavor Blasted',2.4900000000000002131,'Food');
INSERT INTO item VALUES(91,'Barnana Brittle',5.9900000000000002131,'Food');
INSERT INTO item VALUES(92,'Barnana Bites',5.9900000000000002131,'Food');
INSERT INTO item VALUES(93,'Totino''s Pizza Rolls (15ct)',5.2900000000000000355,'Food');
INSERT INTO item VALUES(94,'Hot Pockets Pepperoni Pizza (2ct)',3.5899999999999998578,'Food');
INSERT INTO item VALUES(95,'Hot Pockets Ham & Cheddar (2ct)',3.5899999999999998578,'Food');
INSERT INTO item VALUES(96,'Jack Links Original Beef Jerky',5.8899999999999996802,'Food');
INSERT INTO item VALUES(97,'Jack Links Peppered Beef Jerky',9.4900000000000002131,'Food');
INSERT INTO item VALUES(98,'Jack Links Teriyaki Beef Jerky',9.4900000000000002131,'Food');
INSERT INTO item VALUES(99,'Chex Mix',2.9900000000000002131,'Food');
INSERT INTO item VALUES(100,'Skinny Pop Family Size Popcorn',4.2900000000000000355,'Food');
INSERT INTO item VALUES(101,'Skinny Pop Family Size White Cheddar Popcorn',4.2900000000000000355,'Food');
INSERT INTO item VALUES(102,'Skinny Pop Family Size Sweet & Salty Kettle Popcorn',4.2900000000000000355,'Food');
INSERT INTO item VALUES(103,'Kellogg''s Corn Flakes',4.1900000000000003907,'Food');
INSERT INTO item VALUES(104,'Kellogg''s Raisin Bran Crunch',5.2900000000000000355,'Food');
INSERT INTO item VALUES(105,'Special K Vanilla & Almond Cereal',4.7900000000000000355,'Food');
INSERT INTO item VALUES(106,'Honey Nut Cheerios',5.2900000000000000355,'Food');
INSERT INTO item VALUES(107,'Chocolate Peanut Butter Cheerios',5.2900000000000000355,'Food');
INSERT INTO item VALUES(108,'Ben & Jerry''s Chocolate Chip Cookie Dough',5.9900000000000002131,'Food');
INSERT INTO item VALUES(109,'Ben & Jerry''s Karamel Sutra Core',5.9900000000000002131,'Food');
INSERT INTO item VALUES(110,'Ben & Jerry''s Americone Dream',5.9900000000000002131,'Food');
INSERT INTO item VALUES(111,'Ben & Jerry''s Half-Baked',5.9900000000000002131,'Food');
INSERT INTO item VALUES(112,'Ben & Jerry''s Chunky Monkey',5.9900000000000002131,'Food');
INSERT INTO item VALUES(113,'Tostito''s Scoops',4.2900000000000000355,'Food');
INSERT INTO item VALUES(114,'Tostito''s Original',4.2900000000000000355,'Food');
INSERT INTO item VALUES(115,'Tostito''s Hint of Lime',4.2900000000000000355,'Food');
INSERT INTO item VALUES(116,'Tostito''s Salsa Con Queso',3.9900000000000002131,'Food');
INSERT INTO item VALUES(117,'Tostito''s Chunky Salsa - Mild',3.5899999999999998578,'Food');
INSERT INTO item VALUES(118,'Tostito''s Creamy Spinach Dip',3.4900000000000002131,'Food');
INSERT INTO item VALUES(119,'Lay''s Original Potato Chips, Family Size',3.4900000000000002131,'Food');
INSERT INTO item VALUES(120,'Ruffles Original Potato Chips, Family Size',4.2900000000000000355,'Food');
INSERT INTO item VALUES(121,'Water Gallon',1.4899999999999999911,'Food');
INSERT INTO item VALUES(122,'SOLO Plates, Red (15ct)',4.9900000000000002131,'Kitchenware');
INSERT INTO item VALUES(123,'SOLO Plates, Blue (15ct)',4.9900000000000002131,'Kitchenware');
INSERT INTO item VALUES(124,'SOLO Cups, Clear (36ct)',4.4900000000000002131,'Kitchenware');
INSERT INTO item VALUES(125,'SOLO Cups, Green (36ct)',4.4900000000000002131,'Kitchenware');
INSERT INTO item VALUES(126,'SOLO Cups, Purple (36ct)',4.4900000000000002131,'Kitchenware');
INSERT INTO item VALUES(127,'SOLO Party Cups, Blue (36ct)',4.9900000000000002131,'Kitchenware');
INSERT INTO item VALUES(128,'SOLO Party Cups, Black (36ct)',4.9900000000000002131,'Kitchenware');
INSERT INTO item VALUES(129,'SOLO Party Cups, Orange (36ct)',4.9900000000000002131,'Kitchenware');
INSERT INTO item VALUES(130,'TopFlight Princeton Folder',2.5,'School Supplies');
INSERT INTO item VALUES(131,'College-Ruled Paper (150ct)',5,'School Supplies');
INSERT INTO item VALUES(132,'Avery 5pc Binder Dividers',3,'School Supplies');
INSERT INTO item VALUES(133,'TopFlight College-Ruled 3 Subject Notebook',3,'School Supplies');
INSERT INTO item VALUES(134,'TopFlight College-Ruled 5 Subject Notebook',4,'School Supplies');
INSERT INTO item VALUES(135,'Princeton 3 Subject Notebook',8,'School Supplies');
INSERT INTO item VALUES(136,'Princeton 5 Subject Notebook',10,'School Supplies');
INSERT INTO item VALUES(137,'Princeton 1" 3-Ring Binder',6,'School Supplies');
INSERT INTO item VALUES(138,'Samsill 1" Value Binder',4,'School Supplies');
INSERT INTO item VALUES(139,'Tartan Shipping Tape',2.5,'School Supplies');
INSERT INTO item VALUES(140,'Scotch Shipping Tape',3,'School Supplies');
INSERT INTO item VALUES(141,'Triplus Fineliner Point Pens (20pc)',35,'School Supplies');
INSERT INTO item VALUES(142,'BiC Medium Pt Blue Pens (10pc)',3,'School Supplies');
INSERT INTO item VALUES(143,'BiC Medium Pt Red Pens (10pc)',3,'School Supplies');
INSERT INTO item VALUES(144,'Ticon Yellow Pencil (24pc)',3,'School Supplies');
INSERT INTO item VALUES(145,'White-Out',2.5,'School Supplies');
INSERT INTO item VALUES(146,'Desk-Style Hi-Liter (2pc)',2,'School Supplies');
CREATE TABLE IF NOT EXISTS "order" (
	id INTEGER NOT NULL, 
	custid INTEGER, 
	delivid INTEGER, 
	status VARCHAR, 
	PRIMARY KEY (id), 
	FOREIGN KEY(custid) REFERENCES customer (id), 
	FOREIGN KEY(delivid) REFERENCES deliverer (id)
);
INSERT INTO "order" VALUES(1,1,1,'in progress');
INSERT INTO "order" VALUES(2,1,1,'in progress');
CREATE TABLE cart_item (
	id INTEGER NOT NULL, 
	custid INTEGER, 
	itemid INTEGER, 
	quantity INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(custid) REFERENCES customer (id), 
	FOREIGN KEY(itemid) REFERENCES item (id)
);
CREATE TABLE order_item (
	id INTEGER NOT NULL, 
	orderid INTEGER, 
	itemid INTEGER, 
	quantity INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(orderid) REFERENCES "order" (id), 
	FOREIGN KEY(itemid) REFERENCES item (id)
);
INSERT INTO order_item VALUES(1,1,NULL,20);
INSERT INTO order_item VALUES(2,1,NULL,234091);
COMMIT;
