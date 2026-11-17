import os,json,urllib.request as U
N,E,S,W=-10,1,10,-1
D={'P':(N,N+N,N+W,N+E),'N':(2*N+E,2*N+W,2*S+E,2*S+W,2*E+N,2*E+S,2*W+N,2*W+S),'B':(N+E,N+W,S+E,S+W),'R':(N,E,S,W)}
D['Q']=D['K']=D['B']+D['R']
KC=99999;MT=KC//4;BP=30
V={'P':100,'N':310,'B':330,'R':520,'Q':960,'K':KC}
def mkt(g):
 T={}
 for k in V:
  t=[0]*120
  for q in range(120):
   r=9-q//10;f=q%10-1
   if not(0<=r<8 and 0<=f<8):continue
   c=abs(2*f-7)+abs(2*r-7)
   if k=='P':v=r*r*(2+5*g)+(f in(3,4))*(r in(2,3,4))*12*(1-g)+(r==1)*(f in(3,4))*-8
   elif k=='N':v=-4*c+(r==0)*-12
   elif k=='B':v=-2*c+(r==0)*-8
   elif k=='R':v=(r==6)*18+(f in(3,4))*4*(1-g)
   elif k=='Q':v=-c*(1+g)
   else:v=((r==0)*(20,30,10,0,0,10,30,20)[f]-r*12)*(1-g)+(14-2*c)*3*g
   t[q]=V[k]+round(v)
  T[k]=t
 return T
T=mkt(0)
def att(b,i):
 for d in D['N']:
  if b[i+d]=='n':return 1
 for d in D['K']:
  j=i+d
  if b[j]=='k':return 1
  while b[j]=='.':j+=d
  if b[j]=='q' or b[j]==('b' if d in D['B'] else 'r'):return 1
 return b[i-11]=='p' or b[i-9]=='p'
def gen(p,qc=0):
 b,s,r,e=p
 for i in range(21,99):
  c=b[i]
  if c not in'PNBRQK':continue
  for d in D[c]:
   j=i+d
   while 1:
    q=b[j]
    if q in' PNBRQK':break
    if c=='P':
     if d in(N,N+N)and q!='.'or d==N+N and(i<81 or b[i+N]!='.')or d in(N+W,N+E)and q=='.'and j!=e:break
     if qc and q=='.'and j>28 and j!=e:break
    if not qc or q!='.'or c=='P':yield i,j
    if c in'PNK'or q!='.':break
    j+=d
  if c=='K'and not qc:
   for x in r:
    if x>90:
     d=1 if x>i else -1
     if all(b[k]=='.' for k in range(min(i,x)+1,max(i,x))) and not(att(b,i) or att(b,i+d) or att(b,i+2*d)):yield i,i+2*d
def val(p,m):
 b=p[0];i,j=m;c=b[i];q=b[j]
 v=T[c][j]-T[c][i]
 if q!='.':v+=T[q.upper()][119-j]+(q=='b'and b.count('b')==2)*BP
 if c=='P':
  if j<29:v+=T['Q'][j]-T['P'][j]
  if j==p[3]:v+=T['P'][109-j]
 if c=='K'and abs(j-i)==2:x=91 if j<i else 98;v+=T['R'][(i+j)//2]-T['R'][x]
 return v
def mk(p,m):
 b,s,r,e=p;i,j=m;c=b[i];s+=val(p,m)
 b=list(b);b[j]=c;b[i]='.'
 r=tuple(x for x in r if x not in(i,j)and not(c=='K'and x>90))
 ne=0
 if c=='P':
  if j<29:b[j]='Q'
  if j==e:b[j+10]='.'
  if j==i+2*N:ne=119-(i+N)
 if c=='K'and abs(j-i)==2:x=91 if j<i else 98;b[x]='.';b[(i+j)//2]='R'
 return(''.join(b)[::-1].swapcase(),-s,tuple(119-x for x in r),ne)
def nul(p):return(p[0][::-1].swapcase(),-p[1],tuple(119-x for x in p[2]),0)
def ok(q):b=q[0][::-1].swapcase();return not att(b,b.index('K'))
class Stop(Exception):pass
RB=[0];TT={};KL={};HH={};REP={};nodes=0;LIM=0;PH=-1
def qs(p,a,bb):
 global nodes
 nodes+=1
 if nodes>LIM:raise Stop
 s=p[1]
 if s>=bb:return s
 if s>a:a=s
 b=p[0];best=s
 ms=sorted(((val(p,m),m)for m in gen(p,1)),reverse=True)
 for v,m in ms:
  if s+v+150<a:break
  q=mk(p,m)
  if not ok(q):continue
  t=-qs(q,-bb,-a)
  if t>best:
   best=t
   if t>a:
    a=t
    if a>=bb:break
 return best
def srch(p,d,a,bb,ply,nm=1):
 global nodes
 if d<=0:return qs(p,a,bb)
 nodes+=1
 if nodes>LIM:raise Stop
 b=p[0];key=(b,p[2],p[3])
 if ply and REP.get(b):return 0
 en=TT.get(key);tm=None
 if en:
  ed,ef,es,tm=en
  if ply and ed>=d and(ef==0 or ef>0 and es>=bb or ef<0 and es<=a):return es
 chk=att(b,b.index('K'))
 if chk:d+=1
 s=p[1];pv=bb-a>1
 if not chk and not pv and ply:
  if d<=3 and s-90*d>=bb:return s
  if nm and d>=2 and s>=bb and any(c in b for c in'NBRQ'):
   t=-srch(nul(p),d-3-(d>6),-bb,-bb+1,ply+1,0)
   if t>=bb:return t if t<MT else bb
 a0=a;kl=KL.get(ply)
 ms=sorted(((v+(KC if m==tm else 9000 if b[m[1]]!='.' else 5000 if m==kl else HH.get(m,0)),v,m)for v,m in((val(p,m),m)for m in gen(p))),reverse=True)
 best=-KC;bm=None;REP[b]=REP.get(b,0)+1;n=0
 fut=not chk and d<=2 and s+120*d<=a
 try:
  for o,v,m in ms:
   cap=o>=8000
   if fut and n and not cap:continue
   q=mk(p,m)
   if not ok(q):continue
   if n==0:t=-srch(q,d-1,-bb,-a,ply+1)
   else:
    rd=1 if n>=3 and d>=3 and not cap and not chk else 0
    if rd and n>=8 and d>=5:rd=2
    t=-srch(q,d-1-rd,-a-1,-a,ply+1)
    if t>a and(rd or pv and t<bb):t=-srch(q,d-1,-bb,-a,ply+1)
   n+=1
   if t>best:
    best=t;bm=m
    if ply==0:RB[0]=m
    if t>a:
     a=t
     if a>=bb:
      if not cap:KL[ply]=m;HH[m]=min(HH.get(m,0)+d*d,4000)
      break
 finally:REP[b]-=1
 if not n:return -KC//2+ply if chk else 0
 TT[key]=(d,0 if a0<best<bb else 1 if best>=bb else -1,best,bm)
 return best
def sc(b):return sum((T[c][i]if c.isupper()else -T[c.upper()][119-i])for i,c in enumerate(b)if c.isalpha())+BP*((b.count('B')>1)-(b.count('b')>1))
def think(p,soft,hard):
 global nodes,LIM,T,PH
 g=sum(V[c.upper()]for c in p[0]if c in'NBRQnbrq')
 h=max(0,min(1,(6000-g)/4000))
 if h!=PH:PH=h;TT.clear()
 T=mkt(h)
 p=(p[0],sc(p[0]),p[2],p[3])
 nodes=0;LIM=hard;RB[0]=None;HH.clear();KL.clear()
 try:
  for d in range(1,40):
   t=srch(p,d,-KC,KC,0)
   if nodes>soft or t>=MT:break
 except Stop:pass
 return RB[0],d
def sq(i,w):
 if not w:i=119-i
 return'abcdefgh'[i%10-1]+str(10-i//10)
def isq(s,w):
 i=(10-int(s[1]))*10+ord(s[0])-96
 return i if w else 119-i
def fen(f):
 bd,sd,cs,ep=f.split()[:4];b=' '*20
 for row in bd.split('/'):
  b+=' '
  for ch in row:b+='.'*int(ch)if ch.isdigit()else ch
  b+=' '
 b+=' '*20;r=tuple(x for c,x in zip('KQkq',(98,91,28,21))if c in cs)
 e=isq(ep,1)if ep!='-'else 0
 p=(b,0,r,e)
 if sd=='b':p=nul(p);p=(p[0],0,p[2],119-e if e else 0)
 return p,sd=='w'
def uci(p,m,w):return sq(m[0],w)+sq(m[1],w)+('q'if p[0][m[0]]=='P'and m[1]<29 else'')
def post(u,d):return json.load(U.urlopen(U.Request(EU+u,json.dumps(d).encode(),{'content-type':'application/json'})))
def play():
 global TT
 gi=None
 while 1:
  g=post('/game',{})
  if g['status']=='done':break
  if g['game']!=gi:gi=g['game'];TT={}
  while g['status']=='your_move':
   p,w=fen(g['start_fen']);REP.clear();REP[p[0]]=1
   for u in g['moves']:
    p=mk(p,(isq(u[:2],w),isq(u[2:4],w)));w=not w;REP[p[0]]=REP.get(p[0],0)+1
   p,w=fen(g['fen']);REP[p[0]]=REP.get(p[0],1)-1
   if len(TT)>4e5:TT={}
   lg=g['legal_moves']
   k=1 if g['plies']<120 else .6;m,d=think(p,int(SOFT*k),int(HARD*k));u=uci(p,m,w)if m else lg[0]
   if u not in lg:u=lg[0]
   g=post('/move',{'game':g['game'],'move':u})
EU=os.environ.get('MAKEFUN_ENV_URL');SOFT=30000;HARD=90000
play()
