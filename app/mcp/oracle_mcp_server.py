import oracledb

from app.config import ORACLE_PASSWORD, ORACLE_USER, get_oracle_dsn


class OracleMCPServer:

    def __init__(self):
        self.conn = oracledb.connect(
            user=ORACLE_USER, password=ORACLE_PASSWORD, dsn=get_oracle_dsn()
        )

    def skill_exists(self, skill_name: str, skill_type: str) -> bool:
        cursor = self.conn.cursor()

        if skill_type.lower() == "technical":
            query = """
            SELECT 1
            FROM COMP_TECHNIQUE
            WHERE LOWER(CTC_LIBELLE) = LOWER(:skill_name)
            """
        else:
            query = """
            SELECT 1
            FROM COMP_FONCTION
            WHERE LOWER(CFN_LIBELLE) = LOWER(:skill_name)
            """

        cursor.execute(query, {"skill_name": skill_name})
        result = cursor.fetchone()
        cursor.close()

        return result is not None

    def add_skill(self, skill: dict):
        """
        Désactivé temporairement :
        COMP_TECHNIQUE et COMP_FONCTION sont exposés comme materialized views,
        donc les DML échouent avec ORA-01732.
        """
        return {
            "status": "oracle_insert_disabled",
            "reason": "COMP_TECHNIQUE / COMP_FONCTION non insérables",
        }

    def task_exists(self, task_name: str) -> bool:
        cursor = self.conn.cursor()

        query = """
        SELECT 1
        FROM COMP_TACHE
        WHERE LOWER(CTA_LIBELLE) = LOWER(:task_name)
        """
        cursor.execute(query, {"task_name": task_name})
        result = cursor.fetchone()
        cursor.close()

        return result is not None

    def add_task(self, task_name: str):
        cursor = self.conn.cursor()

        next_id = self._next_id("COMP_TACHE", "CTA_ID")

        query = """
        INSERT INTO COMP_TACHE (CTA_ID, CTA_LIBELLE, CTA_ORDRE)
        VALUES (:id, :label, NULL)
        """

        cursor.execute(query, {"id": next_id, "label": task_name.strip()})

        self.conn.commit()
        cursor.close()

        return {"status": "task_added", "name": task_name}

    def _next_id(self, table_name: str, id_column: str) -> int:
        cursor = self.conn.cursor()

        query = f"SELECT NVL(MAX({id_column}), 0) + 1 FROM {table_name}"
        cursor.execute(query)

        next_id = cursor.fetchone()[0]
        cursor.close()

        return next_id

    def close(self):
        if self.conn:
            self.conn.close()
