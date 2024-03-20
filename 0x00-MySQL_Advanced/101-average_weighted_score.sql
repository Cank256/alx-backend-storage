-- Creates a stored procedure that computes and stores the average weighted score for all students
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE cur_user_id INT;
    DECLARE cur_cursor CURSOR FOR SELECT id FROM users;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    OPEN cur_cursor;

    read_loop: LOOP
        FETCH cur_cursor INTO cur_user_id;
        IF done THEN
            LEAVE read_loop;
        END IF;
        CALL ComputeAverageWeightedScoreForUser(cur_user_id);
    END LOOP;

    CLOSE cur_cursor;
END$$
DELIMITER ;
