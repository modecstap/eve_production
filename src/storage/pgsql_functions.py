from sqlalchemy import text
pgsql_functions = {
    "calculate_material_cost": text("""
        CREATE OR REPLACE FUNCTION calculate_material_cost (
        p_material_id INTEGER,
        p_need_count INTEGER
    ) 
    RETURNS NUMERIC AS
    $$
    DECLARE
        r_material_p_need_count INTEGER;
        r_transaction_id INTEGER;
        r_transaction_remains INTEGER;
        r_transaction_price NUMERIC;
        r_used_count INTEGER;
        r_remaining_remains INTEGER;
        production_cost NUMERIC := 0;
    BEGIN
        FOR r_transaction_id, r_transaction_remains, r_transaction_price IN 
            SELECT id, remains, price 
            FROM transactions
            WHERE material_id = p_material_id AND remains > 0
            ORDER BY release_date
        LOOP
            IF p_need_count > 0 THEN
                IF r_transaction_remains >= p_need_count THEN
                    r_used_count := p_need_count;
                    r_remaining_remains := r_transaction_remains - r_used_count;
                    p_need_count := 0;
                ELSE
                    r_used_count := r_transaction_remains;
                    r_remaining_remains := 0;
                    p_need_count := p_need_count - r_used_count;
                END IF;
                production_cost := production_cost + r_used_count * r_transaction_price;
            END IF;
        END LOOP;
    
        RETURN production_cost;
    END;
    $$ LANGUAGE plpgsql;""")
}
