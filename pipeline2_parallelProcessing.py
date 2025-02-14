"""
how to run program
python -m luigi --module pipeline2_parallelProcessing MasterTask --workers 3 --scheduler-host localhost
or
python pipeline2_parallelProcessing.py
"""

import luigi


class TaskA(luigi.Task):
    def run(self):
        print("processing sales data")
        with self.output().open('w') as f:
            f.write("sales data processed")

    def output(self):
        return luigi.LocalTarget("output/taskA.txt")


class TaskB(luigi.Task):

    def run(self):
        print("processing customer data ")
        with self.output().open('w') as f:
            f.write("sales customer processed")


    def output(self):
        return luigi.LocalTarget("output/taskB.txt")



class TaskC(luigi.Task):
    def run(self):
        print("processing banking data")
        with self.output().open('w') as f:
            f.write("sales banking processed")

    def output(self):
        return  luigi.LocalTarget("output/taskC.txt")


class MasterTask(luigi.WrapperTask):

    def requires(self):
        return [TaskA(),TaskB(),TaskC()]

if __name__ == "__main__":
    luigi.build([MasterTask()],workers =3 , scheduler_host="localhost")






