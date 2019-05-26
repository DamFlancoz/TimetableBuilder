''' Prototype to Time table builder
- made to get to classes info page( c.html ) through 2 pages- a.html , b.html
- it was realsised it can be accessed without them
- no login is need to access page, the reason switch to requests instead of urllib was made (cookie handling)
- can pass list of tuples instad to dict to request.post if key value is repeating
- encoded fprm is passed to urllib2.open for data, got from inspect tool of page > network
'''



from requests import Session #class
import urllib2

COURSE = 'CSC'
COURSENO = '111'

def proto_Requests():
    with Session() as s:
        url = 'https://www.uvic.ca'

        exten = '/BAN1P/bwckschd.p_disp_dyn_sched' #term selector page
        page = s.get(url+exten)
        
        with open('a.html','w') as t:
            t.write(page.content)



        exten2 = '/BAN1P/bwckgens.p_proc_term_date' #course selector page
        data2 = {'p_calling_proc': 'bwckschd.p_disp_dyn_sched','p_term': '201901'}

        page2 = s.post(url + exten2, data = data2, headers={'Referer':url+exten})

        with open('b.html','w') as t:
            t.write(page2.content)



        exten3 = '/BAN1P/bwckschd.p_get_crse_unsec'
        data3 = [('term_in', '201901'),
                ('sel_subj', 'dummy'),
                ('sel_day', 'dummy'),
                ('sel_schd', 'dummy'),
                ('sel_insm', 'dummy'),
                ('sel_camp', 'dummy'),
                ('sel_levl', 'dummy'),
                ('sel_sess', 'dummy'),
                ('sel_instr', 'dummy'),
                ('sel_ptrm', 'dummy'),
                ('sel_attr', 'dummy'),
                ('sel_subj', COURSE),
                ('sel_crse', COURSENO),
                ('sel_title', ''),
                ('sel_schd', '%'),
                ('sel_insm', '%'),
                ('sel_from_cred', ''),
                ('sel_to_cred', ''),
                ('sel_camp', '%'),
                ('sel_levl', '%'),
                ('sel_ptrm', '%'),
                ('sel_instr', '%'),
                ('begin_hh', '0'),
                ('begin_mi', '0'),
                ('begin_ap', 'a'),
                ('end_hh', '0'),
                ('end_mi', '0'),
                ('end_ap', 'a')]

        page3 = s.post(url + exten3, data = data3, headers= {'Referer': url+exten2} )

        with open('c.html','w') as t:
            t.write(page3.content)

def proto_Urllib2():
    url = 'https://www.uvic.ca'
    exten = '/BAN1P/bwckschd.p_get_crse_unsec'

    # contain COURSE and COURSENO further down
    data = 'term_in=201901&sel_subj=dummy&sel_day=dummy&sel_schd=dummy&sel_insm=dummy&sel_camp=dummy&sel_levl=dummy&sel_sess=dummy&sel_instr=dummy&sel_ptrm=dummy&sel_attr=dummy&sel_subj='+COURSE+'&sel_crse='+COURSENO+'&sel_title=&sel_schd=%25&sel_insm=%25&sel_from_cred=&sel_to_cred=&sel_camp=%25&sel_levl=%25&sel_ptrm=%25&sel_instr=%25&begin_hh=0&begin_mi=0&begin_ap=a&end_hh=0&end_mi=0&end_ap=a'
    page = urllib2.urlopen(url=url+exten, data=data).read()

    # Usually you would also close urlopen connection

    with open('c.html','w') as t:
        t.write(page)

# Main Program #

proto_Requests()
    
