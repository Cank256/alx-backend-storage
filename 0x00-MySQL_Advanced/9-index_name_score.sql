-- Creates an index for optimizing searches on the first letter of names and the score
CREATE INDEX idx_name_first_score ON names (name(1), score);
