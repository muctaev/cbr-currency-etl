DROP TABLE IF EXISTS exchange_rates;

CREATE TABLE exchange_rates (
    id SERIAL PRIMARY KEY,              
    date DATE NOT NULL,                 
    currency VARCHAR(3) NOT NULL,       
    rate NUMERIC(10,4) NOT NULL,        
    nominal INTEGER NOT NULL,           
    loaded_at TIMESTAMP DEFAULT NOW(),  
    UNIQUE(date, currency)
);