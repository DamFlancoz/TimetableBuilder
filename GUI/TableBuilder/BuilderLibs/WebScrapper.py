from urllib.request import urlopen
from bs4 import BeautifulSoup as bSoup
#from Exceptions import *

'''
Python3 gives error if you try to use import <class> to reach module in same
directory
'''
if __name__=='PythonLibs.WebScrapper':
    
    from PythonLibs.Exceptions import NoSectionsAvailable

'''
Takes: term code, Course Object with course name and course no.
Returns: (str)the html page containing classes information
'''
def getPage(TERM,course):
    Url = 'https://www.uvic.ca/BAN1P/bwckschd.p_get_crse_unsec'
    Data = 'term_in='+TERM+'&sel_subj=dummy&sel_day=dummy&sel_schd=dummy&sel_insm=dummy&sel_camp=dummy&sel_levl=dummy&sel_sess=dummy&sel_instr=dummy&sel_ptrm=dummy&sel_attr=dummy&sel_subj='+course.course+'&sel_crse='+course.num+'&sel_title=&sel_schd=%25&sel_insm=%25&sel_from_cred=&sel_to_cred=&sel_camp=%25&sel_levl=%25&sel_ptrm=%25&sel_instr=%25&begin_hh=0&begin_mi=0&begin_ap=a&end_hh=0&end_mi=0&end_ap=a'
    # Data contains course.course and course.num further down
 
    htmlPage = urlopen(url=Url, data=Data.encode()).read().decode()
    htmlLines = htmlPage.split('\n')
    
    if (htmlLines[103] == 'No classes were found that meet your search criteria'
        or htmlLines[102] == 'No classes were found that meet your search criteria'):
        raise(NoSectionsAvailable(course))
    
    return htmlPage 





