import time,csv,math,create_map
from random import randint

class TSP:

    def __init__(self,**kwargs):
        self.state_list = kwargs["state_list"]
        self.dataset_length = len(self.state_list)
        self.state_score = self.calculate_score(self.state_list)
        self.temperature = kwargs["temperature"]
        self.neighbours_number = kwargs["neighbours_number"]

    @classmethod
    def config(cls,**kwargs):
        with open(kwargs["dataset_name"],encoding="utf-8") as f:
            state_list = [{"city":x[0],"lat":float(x[1]),"lng":float(x[2])} for x in csv.reader(f)]
            kwargs["state_list"] = state_list
            return cls(**kwargs)

    def create_neighbours(self,n,lst):
        best_ngbr_lst = []
        best_ngbr_score = 10**6
        for x in range(n):
            lst_cp = lst[::]
            rnd1 = randint(1,self.dataset_length-1)
            rnd2 = randint(1,self.dataset_length-1)
            lst_cp[rnd1],lst_cp[rnd2] = lst_cp[rnd2],lst_cp[rnd1]
            sc = self.calculate_score(lst_cp)
            if sc < best_ngbr_score:
                best_ngbr_score = sc
                best_ngbr_lst = lst_cp
        return best_ngbr_lst,best_ngbr_score

    def calculate_score(self,lst):
        tbst = 0
        for x in range(self.dataset_length-1):
            tbst+=self.calculate_distance(
                lst[x]["lng"],
                lst[x]["lat"],
                lst[x+1]["lng"],
                lst[x+1]["lat"]
            )
        return tbst

    @staticmethod
    def calculate_distance(x,y,x2,y2):
        return math.sqrt(((y2-y)**2)+((x2-x)**2))

    def save_as_html(self,html_file_name):
        cord = [[x["lat"],x["lng"]] for x in self.state_list]
        create_map.c_map(self.state_list,cord,html_file_name)
        print(f"successfully saved as {html_file_name}.html")

    def simulated_annealing(self):
        while self.temperature > 0:

            best_ngbr_lst,best_ngbr_score = self.create_neighbours(
                self.neighbours_number,
                self.state_list
            )

            delta = best_ngbr_score / self.temperature

            if best_ngbr_score < self.state_score or (delta < 1 and delta >= randint(0,1)):
                self.state_score = best_ngbr_score
                self.state_list = best_ngbr_lst
                print(self.temperature,self.state_score)

            self.temperature-=1



iran = TSP.config(
    dataset_name="ir.csv",
    temperature=int(input("Enter The Temperature : ")),
    neighbours_number=int(input("Enter The Number Of Neighbours To Generate : "))
)
iran.simulated_annealing()
iran.save_as_html("iran")