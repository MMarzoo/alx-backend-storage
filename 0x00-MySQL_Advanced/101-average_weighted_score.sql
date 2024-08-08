-- creates a stored procedure ComputeAverageWeightedScoreForUsers that computes and store the average weighted score for all students.
DELIMITER $$
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    UPDATE users AS U,
        (SELECT U.id, SUM(score * weight) / SUM(weight) AS w_avg
        FROM users AS U
        JOIN corrections as C ON U.id=C.user_id
        JOIN projects AS p ON C.project_id=P.id
        GROUP BY U.id)
    AS WA
    SET U.avarege_score = WA.w_avg
    WHERE U.id=WA.id;
END
$$
DELIMITER ;