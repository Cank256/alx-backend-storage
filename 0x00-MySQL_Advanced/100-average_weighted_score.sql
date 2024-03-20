-- Creates a stored procedure that computes and stores the average weighted score for a student
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    UPDATE users
    SET average_score = (
        SELECT SUM(score * weight) / SUM(weight)
        FROM corrections
        JOIN projects ON corrections.project_id = projects.id
        WHERE corrections.user_id = user_id
    )
    WHERE users.id = user_id;
END$$
DELIMITER ;
