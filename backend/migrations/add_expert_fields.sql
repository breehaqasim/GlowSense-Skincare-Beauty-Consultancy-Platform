-- Add experience and consultation_price columns to experts table
ALTER TABLE experts 
ADD COLUMN experience INTEGER NOT NULL DEFAULT 5,
ADD COLUMN consultation_price INTEGER NOT NULL DEFAULT 1500;

-- Update existing records with some sample data
UPDATE experts 
SET experience = FLOOR(RANDOM() * 15 + 5),  -- Random experience between 5-20 years
    consultation_price = FLOOR(RANDOM() * 2000 + 1000);  -- Random price between 1000-3000; 