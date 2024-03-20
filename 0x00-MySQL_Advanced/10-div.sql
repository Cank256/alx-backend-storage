-- Creates a function SafeDiv for safe division, returning 0 when the divisor is 0
DELIMITER $$
CREATE FUNCTION SafeDiv(a INT, b INT) RETURNS FLOAT
BEGIN
    RETURN CASE WHEN b = 0 THEN 0 ELSE a / b END;
END$$
DELIMITER ;
