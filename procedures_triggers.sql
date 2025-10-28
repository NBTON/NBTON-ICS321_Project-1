-- Stored Procedures and Triggers for Horse Racing Database

-- Stored Procedure to delete an owner and all related information
CREATE PROCEDURE DeleteOwner(IN owner_to_delete VARCHAR(15))
BEGIN
    -- Declare variables for handling any errors
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;
    
    -- Start transaction
    START TRANSACTION;
    
    -- Delete all Owns relationships for this owner
    DELETE FROM Owns WHERE ownerId = owner_to_delete;
    
    -- Delete the owner from Owner table
    DELETE FROM Owner WHERE ownerId = owner_to_delete;
    
    -- Commit the transaction
    COMMIT;
END;

-- Trigger to copy horse information to old_info table whenever a horse is deleted
CREATE TRIGGER horse_delete_trigger
    BEFORE DELETE ON Horse
    FOR EACH ROW
BEGIN
    -- Insert the horse information into old_info table before deletion
    INSERT INTO old_info (horseId, horseName, age, gender, registration, stableId)
    VALUES (OLD.horseId, OLD.horseName, OLD.age, OLD.gender, OLD.registration, OLD.stableId);
END;