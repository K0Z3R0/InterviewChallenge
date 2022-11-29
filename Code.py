import numpy as np 
import pandas as pd
import lxml.html as LH
import bs4 as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time 


class Maze:

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        self.driver = webdriver.Chrome('./chromedriver',options=options)
        challenge_url = 'https://pg-0451682683.fs-playground.com/'
        self.driver.get(challenge_url)
        page_source = self.driver.page_source
        maze_soup = bs.BeautifulSoup(page_source)
        print(page_source)
        table = maze_soup.find('table')
        table_body = table.find('tbody')

        rows = table_body.find_all('tr')
        maze_list = []

        for row in rows:
            tmp_row = []
            cols = row.find_all('td')
            for col in cols:
                tmp_row.append(col['class'])
            maze_list.append(tmp_row)
        self.maze = maze_list


    def checkvalidmove(self,c,r):
        if  (0 <= c < len(self.maze)) and ((0 <= r < len(self.maze))):
            if self.maze[c][r] == ['empty']:
                return True
            else:
                return False
        else:
            return False
    

    def submitsolution(self,x):
        solutioninput = self.driver.find_element(By.NAME,value='solution')
        solutionbutton = self.driver.find_element(By.CLASS_NAME,value="btn")
        solutioninput.send_keys(x)
        solutionbutton.submit()
        time.sleep(30)




class Location:
    def __init__(self,maze):
        self.maze = maze
        self.c = 0
        self.r = 0
    

    def goright(self,check):
        if check:
            return self.maze.checkvalidmove(self.r,self.c+1)
        self.c+=1
        return 'R'


    def goleft(self,check):
        if check:
            return self.maze.checkvalidmove(self.r,self.c-1)
        self.c-=1
        return 'L'


    def godown(self,check):
        if check:
            return self.maze.checkvalidmove(self.r+1,self.c)
        self.r+=1
        return 'D'


    def goup(self,check):
        if check:
            return self.maze.checkvalidmove(self.r-1,self.c)
        self.r-=1
        return 'U'
    

    def revert(self,str_path):
        reverse_path = ''
        str_tmp = str_path[::-1]
        for x in str_tmp:
            if x == 'R':
                reverse_path+=self.goleft(False)
                continue
            if x == 'L':
                reverse_path+=self.goright(False)
                continue
            if x == 'D':
                reverse_path+=self.goup(False)
                continue
            if x == 'U':
                reverse_path+=self.godown(False)
                continue
        return reverse_path


    def getc(self):
        return self.c


    def getr(self):
        return self.r


class Algorithm:
    
    def __init__(self):
        self.path = ''
        self.rightsequence = 0
        self.downsequence = 1
        self.bothvalid = 0
        self.bothvalidrightsequence = 0
        self.bothvaliddownsequence = 0
        self.bothvalidlastmove = ''

    #swapping rightsequence value with down sequence value
    def swap(self):
        tmp = self.rightsequence
        self.rightsequence = self.downsequence
        self.downsequence = tmp


    #records the spot and movement options when both right and down movements can be made
    def setbothvalid(self):
        self.bothvalid = len(self.path)
        self.bothvalidrightsequence = self.rightsequence
        self.bothvaliddownsequence = self.downsequence
    

    #assigns right and down movement sequence from the last time where both right and down movements were available
    def setbothvalidsequence(self):
        self.rightsequence = self.bothvalidrightsequence
        self.downsequence = self.bothvaliddownsequence
    

    #stores the move made when both right and down movements were available
    def setbothvalidmove(self,x):
        self.bothvalidlastmove = x


    #concatenates moves string to current path
    def addmoves(self,moves):
        self.path+=moves #string method


    # returns current path
    def getpath(self):
        return self.path
    
    
    # returns number of moves made
    def getpathmoves(self):
        return len(self.path)


    def getrightsequence(self):
        return self.rightsequence


    def getdownsequence(self):
        return self.downsequence


    def getbothvalidrightsequence(self):
        return self.bothvalidrightsequence
    

    def getbothvaliddownsequence(self):
        return self.bothvaliddownsequence


    def getbothvalid(self):
        return self.bothvalid
    

    def getbothvalidlastmove(self):
        return self.bothvalidlastmove

    def solve(self,maze_obj,loc_obj):
        while True:
            print("PATH ",self.getpath())
            if loc_obj.goright(True) == False and loc_obj.godown(True) == False:
                print(1)
                pathdiff = self.getpathmoves() - self.getbothvalid()
                self.addmoves(loc_obj.revert(self.getpath()[self.getpathmoves()-pathdiff:self.getpathmoves()]))
                if self.getbothvalidlastmove() == 'down':
                    self.addmoves(loc_obj.goright(False))
                elif self.getbothvalidlastmove() == 'right':
                    self.addmoves(loc_obj.godown(False))
                self.setbothvalidsequence()
                self.swap()
                continue

            if (self.getpathmoves()) % 2 == self.getrightsequence():
                print(2)
                if loc_obj.goright(True):
                    self.addmoves(loc_obj.goright(False))
                    if(loc_obj.godown(True)):
                        self.setbothvalid()
                        self.setbothvalidmove('down')
                else:
                    self.swap()

            elif self.getpathmoves() % 2 == self.getdownsequence():
                print(3)
                if loc_obj.godown(True):
                    self.addmoves(loc_obj.godown(False))
                    if(loc_obj.goright(True)):
                        self.setbothvalid()
                        self.setbothvalidmove('right') 
                else:
                    self.swap()

            if loc_obj.getc() == 21 and loc_obj.getr() == 21:
                print("FINAL PATH",self.getpath())
                print(maze_obj.submitsolution(self.getpath()))
                break


maze_obj = Maze()
algo_obj = Algorithm()
loc_obj = Location(maze_obj)
algo_obj.solve(maze_obj,loc_obj)
