import luigi
import pandas as pd
from sqlalchemy import create_engine

DB_URL = "mysql+pymysql://root:root123@localhost/luigi_assignment"


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

        # Save to CSV
        df.to_csv(self.csv_filename, index=False)
        print("generated file")


class LoadToMySQL(luigi.Task):
    """
    Task to read data from a CSV file and insert it into MySQL using SQLAlchemy.
    """
    csv_filename = luigi.Parameter(default="emp.csv")

    def requires(self):
        task = GenerateCSV()
        return task

    def run(self):
        df = pd.read_csv(self.csv_filename)
        engine = create_engine(DB_URL)
        df.to_sql(name="emp", con=engine, if_exists="append", index=False)
        print("✅ Data successfully inserted into MySQL!")

    def output(self):
        return luigi.LocalTarget("loaded file to mysql successfully")


if __name__ == "__main__":
    luigi.run(["LoadToMySQL", "--local-scheduler"])
