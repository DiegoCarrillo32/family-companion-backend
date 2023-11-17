import psycopg2


class Database:

    # Create and Initialize the local database with the given data
    def __init__(self, host, database, user, password):
        self.conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")

    #Function to create the local tables if they not exists
    def create_tables(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id VARCHAR(255) PRIMARY KEY,
                user_mode CHAR(1) NOT NULL,
                family_user_chatId VARCHAR(255) NOT NULL,
                family_group_id UUID DEFAULT uuid_generate_v4()
            );
        """)

        self.cur.execute("""
                  CREATE TABLE IF NOT EXISTS detection_log (
                      dect_log SERIAL PRIMARY KEY,
                      detection_date DATE NOT NULL,
                      joy_emotion VARCHAR(255) NOT NULL,
                      sorrow_emotion VARCHAR(255) NOT NULL,
                      anger_emotion VARCHAR(255) NOT NULL,
                      surprise_emotion VARCHAR(255) NOT NULL,   
                      family_group_id UUID NOT NULL
                  );
              """)

        self.conn.commit()

    def function_check_emotions_and_clear(self):
        self.cur.execute("""
        CREATE OR REPLACE FUNCTION check_emotions_and_clear(family_id uuid)
        RETURNS TABLE(emotion VARCHAR, status VARCHAR, recommendation VARCHAR) AS $$
        DECLARE
            joy_count INT;
            sorrow_count INT;
            anger_count INT;
            surprise_count INT;
        BEGIN
            SELECT COUNT(*) INTO joy_count FROM detection_log WHERE family_group_id = family_id AND joy_emotion IN ('Very Likely', 'Likely');
            SELECT COUNT(*) INTO sorrow_count FROM detection_log WHERE family_group_id = family_id AND sorrow_emotion IN ('Very Likely', 'Likely');
            SELECT COUNT(*) INTO anger_count FROM detection_log WHERE family_group_id = family_id AND anger_emotion IN ('Very Likely', 'Likely');
            SELECT COUNT(*) INTO surprise_count FROM detection_log WHERE family_group_id = family_id AND surprise_emotion IN ('Very Likely', 'Likely');
    
            IF joy_count > 5 THEN
                -- Vaciar la tabla después de devolver el mensaje.
                RETURN QUERY SELECT 'Joy'::VARCHAR, 'Alegría detectada'::VARCHAR, 'Mantengan el ambiente positivo! Para más ideas sobre actividades familiares felices, visiten youtube.com/watch?v=MOr4h24qFXc'::VARCHAR;
                DELETE FROM detection_log WHERE family_group_id = family_id;
            ELSIF sorrow_count > 5 THEN
                DELETE FROM detection_log WHERE family_group_id = family_id;
                RETURN QUERY SELECT 'Sorrow'::VARCHAR, 'Dolor detectado'::VARCHAR, 'Consideren brindar apoyo y cuidado. Para recursos sobre manejo de la tristeza, visiten youtube.com/watch?v=3qoEgprKLjQ'::VARCHAR;
            ELSIF anger_count > 5 THEN
                DELETE FROM detection_log WHERE family_group_id = family_id;
                RETURN QUERY SELECT 'Anger'::VARCHAR, 'Ira detectada'::VARCHAR, 'Realicen actividades calmantes y resolución de conflictos. Consejos útiles en youtube.com/watch?v=DmvpukP9A5Q'::VARCHAR;
            ELSIF surprise_count > 5 THEN
                DELETE FROM detection_log WHERE family_group_id = family_id;
                RETURN QUERY SELECT 'Surprise'::VARCHAR, 'Sorpresa detectada'::VARCHAR, 'Aseguren que las sorpresas sean agradables, o proporcionen estabilidad. Vean drromeu.net/las-emociones-sorpresa/ para más información.'::VARCHAR;
            END IF;
    
            -- Vaciar la tabla después de devolver el mensaje.
    
            RETURN;
        END;
        $$ LANGUAGE plpgsql;
        """)

    # Function to delete the tables
    def drop_tables(self):
        self.cur.execute("""
            DROP TABLE IF EXISTS users;
        """)

        self.cur.execute("""
            DROP TABLE IF EXISTS detection_log;
        """)

        self.conn.commit()

    # Close the current connection
    def close(self):
        self.conn.close()
