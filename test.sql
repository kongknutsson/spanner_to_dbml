CREATE TABLE WorkSchedule (
    uuid String(36) NOT NULL, 
    company_id String(36) NOT NULL,
    start_time timestamp NOT NULL, 
    end_time timestamp NOT NULL,
    archived_timestamp timestamp,
    archived_reason String(50),
)PRIMARY KEY (uuid);


CREATE TABLE Shift (
    uuid String(36) NOT NULL, 
    shift_type String(50) NOT NULL, 
    team_id String(36) NOT NULL, 
    schedule_id String(36) NOT NULL,
    company_id String(36) NOT NULL, 
    start_time timestamp NOT NULL, 
    end_time timestamp NOT NULL, 
    description String(36),
    archived_timestamp timestamp, 
    archived_reason String(50),
    CONSTRAINT FK_ShiftWorkSchedule FOREIGN KEY (schedule_id) REFERENCES WorkSchedule (uuid),
)PRIMARY KEY (uuid);