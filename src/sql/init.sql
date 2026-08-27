
CREATE TABLE total_consumption (
    date_time TIMESTAMPTZ NOT NULL,
    bidding_zone TEXT NOT NULL,
    value_mwh NUMERIC NOT NULL,
    UNIQUE (date_time, bidding_zone) 
); 