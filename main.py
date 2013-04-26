import random
import epdb 

MAXMATCHSIZE=50
POOLSIZE=200
ACSUM=13
CCSUM=17
PNSUM=19
SEVENS=2
EIGHTS=0
NINES=1
ZEROES=0

FIRSTNUM=7
SECONDNUM=1
THIRDNUM=5
FOURTHNUM=6
FIFTHNUM=7
SIXTHNUM=4
EIGHTHNUM=9

GENERATIONS=4000
TC=0 
MUTATIONRATE=0.10




def number_count(searchnum,phone):
	count=0
	phone=str(phone)
	for letter in phone:
		if str(searchnum)==str(letter):
			count+=1
	return count
def check_places(number):
	number=str(number)
	RETCODE=0

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
#	if DISTANCE > 0 and DISTANCE < 999 :
#		DISTANCE=1
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
#	epdb.st()
	for num in NEWVALUES:
		NUMLIST[num]=0
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
		#epdb.st()
		if NUMLIST[row] > (MINDIST+1) and COUNT < MAXMATCHSIZE:
			rc+=1	
			if  random.random() < MUTATIONRATE:
				NEWVAL=mutate(NUMLIST,MATCHLIST,row)
				NEWVALUES.append(NEWVAL) 
			NEWVALUES=choose_swap_method(NUMLIST,MATCHLIST,row)
			OLDVALUES.append(row)
		else:
			COUNT+=1
	print str(rc) +" xbreed changes..."
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
#			DISTANCE=sum(phone,'PN')
			DISTANCE=number_count(7,phone)
#			DISTANCE+=number_count(0,phone)
#			DISTANCE+=number_count(8,phone)
			DISTANCE+=check_places(phone)
			NUMLIST[phone]=DISTANCE
			TOTDISTANCE+=DISTANCE
		else:
			DISTANCE=999
	return NUMLIST,TOTDISTANCE
def choose_to_add(MATCHLIST,row):
	INLIST=False
	for a in MATCHLIST:
		if a == row:
			INLIST=True
	if INLIST:
		pass
	else:
		MATCHLIST.append(row)

	return MATCHLIST
def find_best(NUMLIST,MINDIST,MATCHLIST):
	COUNT=0
	for row in NUMLIST:
		if COUNT > MAXMATCHSIZE :
			break
		if len(row)==10:
			if NUMLIST[row] < MINDIST:
				MATCHLIST=[]
				MINDIST=NUMLIST[row]
				MATCHLIST=choose_to_add(MATCHLIST,row)
				COUNT=1
			elif NUMLIST[row] == MINDIST:
				MATCHLIST=choose_to_add(MATCHLIST,row)
				COUNT+=1
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

NUMLIST={}
NUMLIST=gen_initial_numbers(TC)
NUMLIST,TOTDISTANCE=calc_distances(NUMLIST)
MINDIST=100
MATCHLIST=[]
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
		print "Generation "+str(generation)+" completed, average distance of "+str(TOTDISTANCE)+", MINDIST= "+str(MINDIST)+", Changes:"+str(CHANGETOTAL)
	

	


print "The best distance is "+str(MINDIST)+". "+str(COUNT)+" of these records exist."
show_close_matches(MATCHLIST)
print MATCHLIST
