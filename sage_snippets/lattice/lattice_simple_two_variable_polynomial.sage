# Solving for A*X + B*Y + C = 0 (mod N)
realX =  2483783609372741844711796611409508953699150227339931594072532857775816861678519728760752822463578092283736545171202456223426718285300069942546085263317713
realY =  2578342571446984113541048796932135362815115268056911893692034275002671523714299396779284635829497518892218887966086302299015669296563109333386403132726687
A =  4303059957002004321941790193101528666937790547271284572383555945340214690210587885752407064053045333040742032334363414874531416689291357490651232727582502435972739083625805276833362041425587599713018104093902621899598099089796775574024082277982687481604590382276409386977035648391622719347371567853137953169
X =  4967567218745483689423593222819017907398300454679863188145065715551633723357039457521505644927156184567473090342404912446853436570600139885092170526635427
B =  84679852682478724753246807483052151120827839694152666749260709385408342260341769001150017451028607353253696389142005671565816045025717419861009809196788658857010337264224421123791227530538694817562727353357763351651972159116445581637412859977225703367199510920056354201608722411052985231254567948356737486389
Y =  5156685142893968227082097593864270725630230536113823787384068550005343047428598793558569271658995037784437775932172604598031338593126218666772806265453375
C =  126547475830076894578285022620959087998851648725063160636375370216642339449606325526346262036908044841593781342769325919347815785363875890301921976369432682140718161013996390562778314399543146374188417459430253608662856315901149392597267619590127696746812147332543260312056818809994702684062927946561306307252
N =  179769313486231590772930519078902473361797697894230657273430081157732675805500963132708477322407536021120113879871393357658789768814416622492847430639474124377767893424865485276302219601246094119453082952085005768838150682342462881473913110540827237163350510684586298239947245938479716304835356329624224137216

print '==== SHOULD BE 0 ===='
print (A*realX + B*realY + C) % N
print '====================='

M = matrix([
    [N, 0,   0],
    [0, X*N, 0],
    [0, 0,   Y*N],
    [C, A*X, B*Y]
])

result = M.LLL()
row = M.LLL()[1]
print result
#print
#print row
reducedC = row[0]
reducedA = row[1] // X
reducedB = row[2] // Y

assert reducedA != N # LLL failed

g = gcd(reducedA, reducedB)
assert (reducedC % g) == 0
reducedA = Integer(reducedA/g)
reducedB = Integer(reducedB/g)
reducedC = Integer(reducedC/g)
if reducedA < 0 :
    reducedA = -reducedA
    reducedB = -reducedB
    reducedC = -reducedC
#print 'Polynomial: %dx + %dy + %d = 0 (mod %d))' % ( reducedA, reducedB, reducedC, N)
#print (reducedA*realX + reducedB*realY + reducedC) % N

calculatedY = (-reducedC * reducedB.inverse_mod(reducedA)) % reducedA
print
print
print 'N           =', N
print
print 'calculatedY =', calculatedY
print 'realY       =', realY
print
calculatedX = (-reducedA.inverse_mod(N)*(reducedC + reducedB*calculatedY)) % N
print 'calculatedX =', calculatedX
print 'realX       =', realX

assert calculatedY == realY
assert calculatedX == realX