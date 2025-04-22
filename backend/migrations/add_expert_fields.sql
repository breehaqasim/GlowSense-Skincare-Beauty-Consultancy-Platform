-- Add experience and consultation_price columns to experts table if they don't exist
ALTER TABLE experts 
ADD COLUMN IF NOT EXISTS experience INTEGER NOT NULL DEFAULT 5,
ADD COLUMN IF NOT EXISTS consultation_price INTEGER NOT NULL DEFAULT 1500;

-- Update existing experts
UPDATE experts 
SET specialization = 'dark circles, antiaging',
    bio = 'Expert in treating dark circles and aging concerns with over 8 years of experience',
    experience = 8,
    consultation_price = 1800
WHERE email = 'sarah.johnson@example.com';

UPDATE experts 
SET specialization = 'acne treatment, hyperpigmentation',
    bio = 'Specialized in acne treatment and hyperpigmentation with advanced certification',
    experience = 10,
    consultation_price = 2000
WHERE email = 'michael.chen@example.com';

UPDATE experts 
SET specialization = 'acne treatment, sensitivity',
    bio = 'Expert in treating acne for sensitive skin types',
    experience = 7,
    consultation_price = 1700
WHERE email = 'emily.rodriguez@example.com';

-- Insert additional experts
INSERT INTO experts (name, email, specialization, bio, experience, consultation_price)
SELECT * FROM (VALUES
    ('Dr. James Rodriguez', 'james.rodriguez@example.com', 'hyperpigmentation', 'Expert in treating various forms of hyperpigmentation and skin discoloration', 7, 1700),
    ('Dr. Lisa Thompson', 'lisa.thompson@example.com', 'sensitivity', 'Specialized in treating sensitive skin conditions and developing gentle skincare routines', 9, 1900),
    ('Dr. Maria Garcia', 'maria.garcia@example.com', 'antiaging, sensitivity', 'Expert in anti-aging treatments for sensitive skin types', 15, 2500),
    ('Dr. Rachel Brown', 'rachel.brown@example.com', 'sensitivity, hyperpigmentation', 'Expert in gentle treatments for hyperpigmentation in sensitive skin', 8, 1800)
) AS new_experts(name, email, specialization, bio, experience, consultation_price)
WHERE NOT EXISTS (
    SELECT 1 FROM experts WHERE email = new_experts.email
);

-- Insert experts with specializations matching inquiry types
INSERT INTO experts (name, email, specialization, bio, experience, consultation_price) VALUES
('Dr. Emily Williams', 'emily.williams@example.com', 'antiaging', 'Anti-aging specialist focusing on natural rejuvenation techniques', 12, 2200),
('Dr. David Kim', 'david.kim@example.com', 'acne treatment, hyperpigmentation', 'Double specialization in acne treatment and post-acne hyperpigmentation', 11, 2100),
('Dr. John Smith', 'john.smith@example.com', 'dark circles, antiaging', 'Specialized in treating aging concerns around the eye area', 13, 2300),
('Dr. Alex Turner', 'alex.turner@example.com', 'acne treatment, sensitivity', 'Focused on treating acne in patients with sensitive skin conditions', 6, 1600)
ON CONFLICT (email) DO UPDATE SET
    name = EXCLUDED.name,
    specialization = EXCLUDED.specialization,
    bio = EXCLUDED.bio,
    experience = EXCLUDED.experience,
    consultation_price = EXCLUDED.consultation_price;

-- Update existing records with some sample data
UPDATE experts 
SET experience = FLOOR(RANDOM() * 15 + 5),  -- Random experience between 5-20 years
    consultation_price = FLOOR(RANDOM() * 2000 + 1000);  -- Random price between 1000-3000;

-- Add slot_duration column to expert_time_slots table
ALTER TABLE expert_time_slots
ADD COLUMN IF NOT EXISTS slot_duration INTERVAL DEFAULT '30 minutes';

-- Add unique constraint to expert_time_slots table
ALTER TABLE expert_time_slots
ADD CONSTRAINT expert_time_slots_unique_day UNIQUE (expert_id, day_of_week);

-- Create some sample time slots for experts
INSERT INTO expert_time_slots (expert_id, day_of_week, start_time, end_time, slot_duration)
SELECT 
    e.id,
    d.day_of_week,
    '11:00:00'::time as start_time,
    '14:00:00'::time as end_time,
    '30 minutes'::interval as slot_duration
FROM experts e
CROSS JOIN (
    SELECT generate_series(1, 5) as day_of_week -- Monday to Friday
) d
ON CONFLICT (expert_id, day_of_week) DO UPDATE
SET 
    start_time = EXCLUDED.start_time,
    end_time = EXCLUDED.end_time,
    slot_duration = EXCLUDED.slot_duration;

-- Add consultation_type column to consultations table
ALTER TABLE consultations
ADD COLUMN IF NOT EXISTS consultation_type VARCHAR(50) DEFAULT 'video';

-- Add missing columns for patient details
ALTER TABLE consultations
ADD COLUMN IF NOT EXISTS patient_name VARCHAR(255),
ADD COLUMN IF NOT EXISTS patient_email VARCHAR(255),
ADD COLUMN IF NOT EXISTS patient_phone VARCHAR(50),
ADD COLUMN IF NOT EXISTS patient_age INTEGER,
ADD COLUMN IF NOT EXISTS patient_gender VARCHAR(20); 