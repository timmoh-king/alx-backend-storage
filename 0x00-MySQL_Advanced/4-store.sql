-- Write a SQL script that creates a trigger that decreases the quantity of an item after adding a new order
-- Quantity in the table items can be negative

DROP TRIGGER IF EXISTS on_order_decrease_quantity;

DELIMITER //
CREATE TRIGGER on_order_decrease_quantity
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
	UPDATE items
		SET quantity = quantity - NEW.number
		WHERE name = NEW.item_name;
END
//
DELIMITER ;
