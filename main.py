import random
import epdb 

MAXMATCHSIZE=20
POOLSIZE=300
APPENDS=POOLSIZE
ACSUM=14
CCSUM=12
PNSUM=23
SEVENS=0
EIGHTS=1
NINES=1
ONES=0
TWOS=0
FIVES=0
ZEROES=1

FIRSTNUM=6
SECONDNUM=0
THIRDNUM=8
FOURTHNUM=4
FIFTHNUM=4
SIXTHNUM=4
EIGHTHNUM=4
TENTHNUM=6
GENERATIONS=1000
TC=0 
MUTATIONRATE=0.150
MINDIST=100
MATCHLIST={}

CROSSLIMIT=3


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
	if number[9]!=str(TENTHNUM):
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
#DON'T REMOVE BELOW FOR LOOP IF YOURE GETTING THAT IDEA! 
	for a in NEWVALUES:
		NUMLIST[a]=0
	NUMLIST=zero_numlist(NUMLIST)
	return NUMLIST

def choose_swap_method(NUMLIST,MATCHLIST,row,APPENDS,NEWVALUES):
	try:
		SDEX=random.randint(0,len(MATCHLIST)-1)
	except :
		SDEX=0
	NEWSEED=SDEX
	if len(MATCHLIST) > 1:
		if random.random < MUTATIONRATE:
			NEWVALUES.append(mutate(NUMLIST,MATCHLIST,row))
			APPENDS+=1
		else:
			while NEWSEED==SDEX:
				NEWSEED=random.randint(0,len(MATCHLIST)-1)
			NEWVALUES.append(perform_xbreed(NUMLIST,row,MATCHLIST[NEWSEED]))
			APPENDS+=1
	else:
		NEWVALUES.append(perform_xbreed(NUMLIST,MATCHLIST[SDEX],row))
		APPENDS+=1
	return NEWVALUES,APPENDS

def crossbreed(MINDIST,NUMLIST,MATCHLIST,APPENDS):
	NEWVALUES=[]
	OLDVALUES=[]
	for row in NUMLIST:
		if len(str(row)) > 10:
			OLDVALUES.append(row)
			epdb.st()
		elif len(str(row)) < 9:
			OLDVALUES.append(row)
			epdb.st()
		try:
			SDEX=random.randint(0,len(MATCHLIST)-1)
		except ValueError:
			SDEX=0
		if NUMLIST[row] > (MINDIST+CROSSLIMIT) :
			NEWVALUES,APPENDS=choose_swap_method(NUMLIST,MATCHLIST,row,APPENDS,NEWVALUES)
			OLDVALUES.append(row)
			APPENDS+=1 
		else:
			if random.random()<MUTATIONRATE:
				if in_matchlist(MATCHLIST,row):
					pass
				else:
					OLDVALUES.append(row)
					NEWVAL=mutate(NUMLIST,MATCHLIST,row)
					NEWVALUES.append(NEWVAL)
					APPENDS+=1
	NUMLIST=finalize_dchanges(NUMLIST,NEWVALUES,OLDVALUES)
	return NUMLIST,APPENDS,len(NEWVALUES),len(OLDVALUES)

def mutate(NUMLIST,MATCHLIST,row):
	SEED=random.randint(0,len(MATCHLIST)-1)
	FIRST_VALUE=str(MATCHLIST[SEED])
	MUTATESPOT=random.randint(0,8)
	NEWSPOT=MUTATESPOT+1
	NEWVAL=random.randint(0,9)
	HEADER=FIRST_VALUE[0:MUTATESPOT]
	FOOTER=row[NEWSPOT:10].zfill(10-NEWSPOT)
	RETSTR=HEADER+str(NEWVAL)+FOOTER
			
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
			DISTANCE+=sum(phone,'AC')
			DISTANCE+=number_count(7,phone,SEVENS)
			DISTANCE+=number_count(0,phone,ZEROES)
			DISTANCE+=number_count(8,phone,EIGHTS)
			DISTANCE+=number_count(5,phone,FIVES)
			DISTANCE+=number_count(2,phone,TWOS)
			DISTANCE+=number_count(1,phone,ONES)
			DISTANCE+=number_count(9,phone,NINES)
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

def trim_matchlist(NUMLIST,MATCHLIST,newlow):
	limit=newlow+2
	newlist=[]
	for a in MATCHLIST:
		try:
			if NUMLIST[a] < limit:
				newlist.append(a)			 
		except KeyError:
			pass
	return newlist
def find_best(NUMLIST,MINDIST,MATCHLIST,OLDLOW):
	COUNT=0
	for row in NUMLIST:
		if COUNT > MAXMATCHSIZE :
			break
		if len(row)==10:
			if NUMLIST[row] < MINDIST:
				MATCHLIST=trim_matchlist(NUMLIST,MATCHLIST,NUMLIST[row])
				OLDLOW=MINDIST
				MINDIST=NUMLIST[row]
				MATCHLIST.append(row)
				COUNT=1
			elif NUMLIST[row] <= MINDIST+1:
				MATCHLIST,COUNT=choose_to_add(MATCHLIST,row,COUNT)
	return MINDIST,COUNT,MATCHLIST,OLDLOW
	
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
		if ml_LENGTH>1:
			SDEX2=random.randint(0,len(MATCHLIST)-1)
			NEWVAL=mutate(NUMLIST,MATCHLIST,MATCHLIST[SDEX2])
			NUMLIST[NEWVAL]=0
			TOTAL+=1
		else:
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
NUMLIST={}
NUMLIST=gen_initial_numbers(TC)
NUMLIST,TOTDISTANCE=calc_distances(NUMLIST)
CHANGETOTAL=0
OLDLOW=0
random.seed()
MINDIST,COUNT,MATCHLIST,OLDLOW=find_best(NUMLIST,MINDIST,MATCHLIST,OLDLOW)
print "Initially "+str(len(MATCHLIST))+" matches in MATCHLIST"
print MINDIST,COUNT
for generation in range(0,GENERATIONS):
	NUMLIST,TOTDISTANCE=calc_distances(NUMLIST)
	MINDIST,COUNT,MATCHLIST,OLDLOW=find_best(NUMLIST,MINDIST,MATCHLIST,OLDLOW)
	NUMLIST,APPENDS,LENNEW,LENOLD=crossbreed(MINDIST,NUMLIST,MATCHLIST,APPENDS)
	if len(NUMLIST) < POOLSIZE:
		NUMLIST,CHANGETOTAL=gen_new_members(NUMLIST,POOLSIZE,len(NUMLIST),MATCHLIST)
	if (generation % 200)==0:
		print "Generation "+str(generation)+", "+str(APPENDS)+" numbers ,NEWVALUES "+str(LENNEW)+" OLDVALUES "+str(LENOLD)+" length "+str(len(NUMLIST))+", matchlist of "+str(len(MATCHLIST))+", OLDLOW= "+str(OLDLOW)+" MINDIST= "+str(MINDIST)+", random children added:"+str(CHANGETOTAL)
#	if str(MINDIST)=='0':
#		print "Generation "+str(generation)+", "+str(APPENDS)+" numbers ,length "+str(len(NUMLIST))+", matchlist of "+str(len(MATCHLIST))+", OLDLOW= "+str(OLDLOW)+" MINDIST= "+str(MINDIST)+", random children added:"+str(CHANGETOTAL)
#		break
		
	


print "The best distance is "+str(MINDIST)+". "+str(len(MATCHLIST))+" of these records exist."
print MATCHLIST
