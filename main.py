import random
import epdb 

MAXMATCHSIZE=50
POOLSIZE=200
ACSUM=15
CCSUM=15
PNSUM=6
SEVENS=0
EIGHTS=0
NINES=0
ONES=2
FIVES=6
ZEROES=0

FIRSTNUM=5
SECONDNUM=5
THIRDNUM=5
FOURTHNUM=5
FIFTHNUM=5
SIXTHNUM=5
EIGHTHNUM=2
PHONENUM="5555551212"
GENERATIONS=12000
TC=0 
MUTATIONRATE=0.0510
MINDIST=100
MATCHLIST={}




def number_count(searchnum,phone,numcount):
	count=0
	phone=str(phone)
	for letter in phone:
		if str(searchnum)==str(letter):
			count+=1
	return abs(numcount-count)
def check_places(number):
	number=str(number)
	RETCODE=0
#	epdb.st()
	if number[2]!=str(THIRDNUM):
		RETCODE+=1
	if number[1]!=str(SECONDNUM):
		RETCODE+=1
	if number[3]!=str(FOURTHNUM):
		RETCODE+=1
	if number[0]!=str(FIRSTNUM):
		RETCODE+=1
	if number[5]!=str(SIXTHNUM):
		RETCODE+=1
	if number[4]!=str(FIFTHNUM):
		RETCODE+=1
	if number[7]!=str(EIGHTHNUM):
		RETCODE+=1

	return RETCODE
def sum(numb,type):
	numb=str(numb)
	asum=0
	try:
		if type=='AC':
			asum=int(numb[0])+int(numb[1])+int(numb[2])
			DISTANCE=abs(asum-ACSUM)
		elif type=='CC':
			asum=int(numb[3])+int(numb[4])+int(numb[5])
			DISTANCE=abs(asum-CCSUM)
		elif type=='PN':
			asum=int(numb[6])+int(numb[7])+int(numb[8])+int(numb[9])
			DISTANCE=abs(asum-PNSUM)
	except IndexError:
		DISTANCE=999		
	except ValueError:
		DISTANCE=999			
	return DISTANCE

def perform_xbreed(NUMLIST,FIRST_VALUE,SECOND_VALUE):
	FIRST_VALUE=str(FIRST_VALUE)
	SECOND_VALUE=str(SECOND_VALUE)
	XOVERSPOT=random.randint(0,9)
	HEADER=str(FIRST_VALUE[0:XOVERSPOT])
	FOOTER=str(SECOND_VALUE[XOVERSPOT+1:10]).zfill(10-XOVERSPOT)
	return str(HEADER)+str(FOOTER)

def zero_numlist(NUMLIST):
	for a in NUMLIST:
		NUMLIST[a]=0
	return NUMLIST

def finalize_dchanges(NUMLIST,NEWVALUES,OLDVALUES):
	for val in OLDVALUES:
		try:
			del(NUMLIST[val])
		except KeyError:
			pass
	NUMLIST=zero_numlist(NUMLIST)
	return NUMLIST

def choose_swap_method(NUMLIST,MATCHLIST,row):
	try:
		SDEX=random.randint(0,len(MATCHLIST)-1)
	except :
		SDEX=0
	NEWVALUES=[]
	NEWSEED=SDEX
	if len(MATCHLIST) > 1:
		if random.random < MUTATIONRATE:
			NEWVALUES.append(mutate(NUMLIST,MATCHLIST,row))
		else:
			while NEWSEED==SDEX:
				NEWSEED=random.randint(0,len(MATCHLIST)-1)
			NEWVALUES.append(perform_xbreed(NUMLIST,MATCHLIST[SDEX],MATCHLIST[NEWSEED]))
	else:
		NEWVALUES.append(perform_xbreed(NUMLIST,MATCHLIST[SDEX],row))
	return NEWVALUES

def crossbreed(MINDIST,NUMLIST,MATCHLIST):
	NEWVALUES=[]
	OLDVALUES=[]
	COUNT=0
	rc=0
	for row in NUMLIST:
		if len(str(row)) > 10:
			OLDVALUES.append(row)
		elif len(str(row)) < 9:
			OLDVALUES.append(row)
		try:
			SDEX=random.randint(0,len(MATCHLIST)-1)
		except ValueError:
			SDEX=0
		if NUMLIST[row] > (MINDIST+1) and len(NEWVALUES)<len(MATCHLIST) :
			rc+=1	
			NEWVALUES=choose_swap_method(NUMLIST,MATCHLIST,row)
			OLDVALUES.append(row)
			if  random.random() < MUTATIONRATE:
				NEWVAL=mutate(NUMLIST,MATCHLIST,row)
				NEWVALUES.append(NEWVAL) 
		else:
			if random.random()<MUTATIONRATE:
				OLDVALUES.append(row)
				NEWVAL=mutate(NUMLIST,MATCHLIST,row)
				NEWVALUES.append(NEWVAL)
			COUNT+=1
#	print str(rc) +" xbreed changes..."
#	if rc==0:
#		epdb.st()
	#Now do actual list replacements
	NUMLIST=finalize_dchanges(NUMLIST,NEWVALUES,OLDVALUES)
	return NUMLIST

def mutate(NUMLIST,MATCHLIST,row):
	SEED=random.randint(0,len(MATCHLIST)-1)
	FIRST_VALUE=str(MATCHLIST[SEED])
	MUTATESPOT=random.randint(0,8)
	NEWSPOT=MUTATESPOT+1
	NEWVAL=random.randint(0,9)
	HEADER=FIRST_VALUE[0:MUTATESPOT]
	FOOTER=row[NEWSPOT:10].zfill(10-NEWSPOT)
	RETSTR=HEADER+str(NEWVAL)+FOOTER
	if len(HEADER+str(NEWVAL)+FOOTER) > 10:
		RETSTR=mutate(NUMLIST,MATCHLIST)
	elif len(HEADER+str(NEWVAL)+FOOTER)==9:
		LASTNUM=random.randint(0,9)
		RETSTR=HEADER+str(NEWVAL)+FOOTER+str(LASTNUM)
			
	return RETSTR

def calc_distances(NUMLIST):
	TOTDISTANCE=0
	DISTANCE=0
	NUMLIST=zero_numlist(NUMLIST)
	for phone in NUMLIST:
		DISTANCE=0
		if len(phone)>9:
			DISTANCE=sum(phone,'PN')
			DISTANCE+=sum(phone,'CC')
	#		DISTANCE+=sum(phone,'AC')
			DISTANCE+=number_count(7,phone,SEVENS)
			DISTANCE+=number_count(0,phone,ZEROES)
			DISTANCE+=number_count(8,phone,EIGHTS)
			DISTANCE+=number_count(5,phone,FIVES)
			DISTANCE+=number_count(1,phone,ONES)
			DISTANCE+=check_places(phone)
			NUMLIST[phone]=DISTANCE
			TOTDISTANCE+=DISTANCE
		else:
			DISTANCE=999
	return NUMLIST,TOTDISTANCE
def choose_to_add(MATCHLIST,row,COUNT):
	INLIST=False
	try:
		for a in MATCHLIST:
			if a == row:
				INLIST=True
	except TypeError:
		MATCHLIST=[]
	if INLIST:
		pass
	else:
		MATCHLIST.append(row)
		COUNT+=1

	return MATCHLIST,COUNT
def in_matchlist(MATCHLIST,row):
	found=False
	for a in MATCHLIST:
		if a==row:
			found=True
	return found 
def find_best(NUMLIST,MINDIST,MATCHLIST):
	COUNT=0
	for row in NUMLIST:
		if COUNT > MAXMATCHSIZE :
			break
		if len(row)==10:
			if NUMLIST[row] < MINDIST:
				MATCHLIST=[]
				MINDIST=NUMLIST[row]
				MATCHLIST.append(row)
				COUNT=1
			elif NUMLIST[row] == MINDIST:
				MATCHLIST,COUNT=choose_to_add(MATCHLIST,row,COUNT)
	return MINDIST,COUNT,MATCHLIST
	
def gen_initial_numbers(TC):
	for a in range(0,POOLSIZE+5):
		number=str(random.randint(1000000000,9999999999))
		ac="%03d" % (random.randint(100,999),)
		cc="%03d" % (random.randint(100,999),)
		nc="%04d" % (random.randint(0,9999),)
		TC+=1
		NUMLIST[str(ac)+str(cc)+str(nc)]=0

	return NUMLIST
def gen_new_members(NUMLIST,POOLSIZE,CURSIZE,MATCHLIST):
	TOTAL=0
	ml_LENGTH=len(MATCHLIST)
	ml_SPOT=random.randint(0,9)
	for a in range(CURSIZE,POOLSIZE+1):
		ml_SPOT=random.randint(0,9)
		ac="%03d" % (random.randint(100,999),)
		cc="%03d" % (random.randint(100,999),)
		pn="%04d" % (random.randint(0,9999),)
		number=str(ac)+str(cc)+str(pn)
		NUMLIST[number]=0
		TOTAL+=1
	return NUMLIST,TOTAL
def print_matches(NUMLIST,MINDIST):
	for row in NUMLIST:
		if NUMLIST[row]==MINDIST:
			print row+'\n'

	return
def show_close_matches(MATCHLIST):
	for row in MATCHLIST:
		if row[0]=='7':
			print row 
	return
def cheat_and_check(NUMLIST,PHONENUM):
	for row in NUMLIST:
		if row==PHONENUM:
			print "Match found!"
			epdb.st()
	return
NUMLIST={}
NUMLIST=gen_initial_numbers(TC)
NUMLIST,TOTDISTANCE=calc_distances(NUMLIST)
CHANGETOTAL=0
random.seed()
MINDIST,COUNT,MATCHLIST=find_best(NUMLIST,MINDIST,MATCHLIST)
print "Initially "+str(len(MATCHLIST))+" matches in MATCHLIST"
print MINDIST,COUNT
print NUMLIST
for generation in range(0,GENERATIONS):
	NUMLIST,TOTDISTANCE=calc_distances(NUMLIST)
	MINDIST,COUNT,MATCHLIST=find_best(NUMLIST,MINDIST,MATCHLIST)
	NUMLIST=crossbreed(MINDIST,NUMLIST,MATCHLIST)
	if len(NUMLIST) < POOLSIZE:
		NUMLIST,CHANGETOTAL=gen_new_members(NUMLIST,POOLSIZE,len(NUMLIST),MATCHLIST)
	if (generation % 200)==0:
		print "Generation "+str(generation)+" completed, ,length "+str(len(NUMLIST))+" average distance of "+str(TOTDISTANCE)+", MINDIST= "+str(MINDIST)+", Changes:"+str(CHANGETOTAL)
	cheat_and_check(NUMLIST,PHONENUM)	

	


print "The best distance is "+str(MINDIST)+". "+str(COUNT)+" of these records exist."
show_close_matches(MATCHLIST)
print MATCHLIST
