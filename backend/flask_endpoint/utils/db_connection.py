from neo4j import GraphDatabase


class Neo4jConnection:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def execute(self, query):
        with self.driver.session() as session:
            return session.read_transaction(self._execute, query)

    @staticmethod
    def _execute(tx, query):
        return tx.run(query).data()
