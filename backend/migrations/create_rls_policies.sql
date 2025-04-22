-- Enable RLS on consultations table
ALTER TABLE consultations ENABLE ROW LEVEL SECURITY;

-- Create policy for users to view their own consultations
CREATE POLICY view_own_consultations ON consultations
    FOR SELECT
    TO authenticated
    USING (auth.uid() = user_id);

-- Create policy for users to insert their own consultations
CREATE POLICY insert_own_consultations ON consultations
    FOR INSERT
    TO authenticated
    WITH CHECK (auth.uid() = user_id);

-- Create policy for users to update their own consultations
CREATE POLICY update_own_consultations ON consultations
    FOR UPDATE
    TO authenticated
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

-- Create policy for users to delete their own consultations
CREATE POLICY delete_own_consultations ON consultations
    FOR DELETE
    TO authenticated
    USING (auth.uid() = user_id); 