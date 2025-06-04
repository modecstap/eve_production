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
    $$ LANGUAGE plpgsql;"""),
    "create_used_transaction": text("""
        CREATE OR REPLACE FUNCTION consume_materials(input_product_id INTEGER, input_count INTEGER)
        RETURNS void AS $$
        DECLARE
            r_material_id INTEGER;
            r_material_need_count INTEGER;
        
            r_transaction_id INTEGER;
            r_transaction_remains INTEGER;
        
            r_used_count INTEGER;
            r_remaining_need INTEGER;
            r_remaining_remains INTEGER;
        
            blueprint_efficiency NUMERIC;
            material_efficiency NUMERIC;
        BEGIN
            -- Получаем коэффициенты эффективности
            SELECT p.blueprint_efficiency, s.material_efficiency 
            INTO blueprint_efficiency, material_efficiency
            FROM product p 
            JOIN station s ON p.station_id = s.id
            WHERE p.id = input_product_id;
        
            -- Цикл по материалам
            FOR r_material_id, r_material_need_count IN 
                SELECT material_id, need_count 
                FROM material_list 
                WHERE need_count > 0 
                  AND type_id = (SELECT type_id FROM product WHERE id = input_product_id)
            LOOP
                -- Расчёт необходимого количества с учётом эффективности и количества продуктов
                r_remaining_need := CEIL(r_material_need_count * blueprint_efficiency * material_efficiency * input_count);
        
                -- Цикл по транзакциям
                FOR r_transaction_id, r_transaction_remains IN 
                    SELECT id, remains 
                    FROM transactions
                    WHERE material_id = r_material_id AND remains > 0
                    ORDER BY release_date
                LOOP
                    EXIT WHEN r_remaining_need <= 0;
        
                    IF r_transaction_remains >= r_remaining_need THEN
                        r_used_count := r_remaining_need;
                        r_remaining_remains := r_transaction_remains - r_used_count;
                        r_remaining_need := 0;
                    ELSE
                        r_used_count := r_transaction_remains;
                        r_remaining_remains := 0;
                        r_remaining_need := r_remaining_need - r_used_count;
                    END IF;
        
                    -- Вставка использованной транзакции
                    INSERT INTO used_transaction_list (product_id, transaction_id, used_count)
                    VALUES (input_product_id, r_transaction_id, r_used_count)
                    ON CONFLICT (product_id, transaction_id) DO NOTHING;
        
                    -- Обновление остатков в транзакции
                    UPDATE transactions
                    SET remains = r_remaining_remains
                    WHERE id = r_transaction_id;
                END LOOP;
            END LOOP;
        END;
        $$ LANGUAGE plpgsql;
        """)
}
