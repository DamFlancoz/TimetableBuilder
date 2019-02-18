from urllib2 import urlopen as uOpen

'''
Takes: term code, course code and course no.
Returns: the page containing classes information
'''
def getPage(TERM,COURSE,COURSENO):
    Url = 'https://www.uvic.ca/BAN1P/bwckschd.p_get_crse_unsec'
    Data = 'term_in='+TERM+'&sel_subj=dummy&sel_day=dummy&sel_schd=dummy&sel_insm=dummy&sel_camp=dummy&sel_levl=dummy&sel_sess=dummy&sel_instr=dummy&sel_ptrm=dummy&sel_attr=dummy&sel_subj='+COURSE+'&sel_crse='+COURSENO+'&sel_title=&sel_schd=%25&sel_insm=%25&sel_from_cred=&sel_to_cred=&sel_camp=%25&sel_levl=%25&sel_ptrm=%25&sel_instr=%25&begin_hh=0&begin_mi=0&begin_ap=a&end_hh=0&end_mi=0&end_ap=a'
    # Data contains COURSE and COURSENO further down
 
    return uOpen(url=Url, data=Data).read()


'''
Tests: getPage with CSC 111, 2019 Jan-Apr term
Puts: out a.html
'''
def Test_getPage():
    with open('a.html','w') as t:
        t.write(getPage('201901','CSC','111'))


# scrap out info to be useful

