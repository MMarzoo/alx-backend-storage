-- creates a stored procedure ComputeAverageScoreForUser that computes and store the average score for a student
DELIMITER ..
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
CREATE PROCEDURE ComputeAverageScoreForUser(user_id INT)
BEGIN
    DECLARE avg_score FLOAT;

    SELECT AVG(score) INTO avg_Score FROM corrections
    WHERE user_id = user_id;
    UPDATE users
    SET avgerage_score = avg_score
    WHERE id = user_id;
END ..