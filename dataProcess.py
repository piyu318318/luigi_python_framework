import luigi
import pandas as pd
from sqlalchemy import create_engine
import logging

DB_URL = "mysql+pymysql://root:root123@localhost/luigi_assignment"

logging.basicConfig(
    filename="luigi_pipeline.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class GenerateCSV(luigi.Task):
    """
    Task to generate a CSV file with sample employee data.
    """
    csv_filename = luigi.Parameter(default="emp.csv")

    def output(self):
        return luigi.LocalTarget(self.csv_filename)

    def run(self):
        data = {
            'eid': [101, 102, 103, 104, 105],
            'ename': ['piyush', 'madhav', 'aishwarya', 'pooja', 'john']
        }
        df = pd.DataFrame(data)

        df.to_csv(self.csv_filename, index=False)
        print("Generated CSV file:", self.csv_filename)


class LoadToMySQL(luigi.Task):
    """
    Task to read data from a CSV file and insert it into MySQL using SQLAlchemy.
    """
    csv_filename = luigi.Parameter(default="emp.csv")
    table_name = luigi.Parameter(default="emp")

    def requires(self):
        return GenerateCSV()

    def output(self):
        return luigi.LocalTarget("output/load_to_mysql_success.txt")

    def run(self):
        engine = create_engine(DB_URL)
        df = pd.read_csv(self.csv_filename)

        df.to_sql(name=self.table_name, con=engine, if_exists="append", index=False)
        print("Data successfully inserted into MySQL!")

        with self.output().open("w") as f:
            f.write("Data loaded successfully")


if __name__ == "__main__":
    luigi.build([LoadToMySQL()], workers=1, scheduler_host="localhost")
