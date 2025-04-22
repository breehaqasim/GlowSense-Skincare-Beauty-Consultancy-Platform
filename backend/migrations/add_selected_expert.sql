-- Add selected_expert_id column to consultations table
ALTER TABLE consultations
ADD COLUMN selected_expert_id UUID REFERENCES experts(id);

-- Add comment for clarity
COMMENT ON COLUMN consultations.selected_expert_id IS 'The ID of the expert specifically selected by the user during booking';

-- Update existing consultations to use expert_id as selected_expert_id if available
UPDATE consultations 
SET selected_expert_id = expert_id 
WHERE expert_id IS NOT NULL; 