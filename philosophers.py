import pykka
import time
class Philsopher(pykka.ThreadingActor):
    def __init__(self, ID, leftfork, rightfork, state, length):
        super().__init__()
        self.ID = ID
        self.leftfork = leftfork
        self.rightfork = rightfork
        self.state = state
        self.length=length

    def on_receive(self, message):
        if message=='process':
            if self.state==None:
                self.state = 'thinking'
                print('philosopher'+str(self.ID)+':'+self.state)
            time.sleep(5)
            while self.state!='eating':
                if self.state=='thinking'or self.state=='ask for leftfork':
                    if self.leftfork=='dirty':
                        break
                    if self.leftfork==None:
                        if self.state!='ask for leftfork':
                            self.state = 'ask for leftfork'
                            print('philosopher'+str(self.ID)+':'+self.state)
                        self.leftfork = l[self.ID%self.length].ask('rightfork')
                    if self.leftfork=='clean':
                        self.state= 'ask for rightfork'
                if self.state=='ask for rightfork':
                    if self.rightfork=='dirty':
                        break
                    if self.rightfork==None:
                        print('philosopher'+str(self.ID)+':'+self.state)
                        self.rightfork = l[(self.ID-2)%self.length].ask('leftfork')
                    if self.rightfork=='clean':
                        self.state= 'eating'
                        print('philosopher'+str(self.ID)+':'+self.state)
            if self.state=='eating':
                time.sleep(5)
                self.leftfork='dirty'
                self.rightfork='dirty'
                self.state='thinking'
                print('philosopher'+str(self.ID)+':'+self.state)
            else:
                return

        if message=='rightfork':
            if self.rightfork=='dirty':
                self.rightfork = None
                l[self.ID-1].tell('process')
                return 'clean'
            else:
                return None
        elif message=='leftfork':
            if self.leftfork=='dirty':
                self.leftfork=None
                l[self.ID-1].tell('process')
                return 'clean'
            else:
                return None   
        

l=[]
length=3
for i in range(length):
    if (i+1)%length!=0 and i!=0:
        l.append(Philsopher.start(i+1,'dirty', None, None,length))
    elif i==0:
        l.append(Philsopher.start(i+1, 'dirty', 'dirty', None,length))
    else:
        l.append(Philsopher.start(i+1, None, None, None,length))

for i in range(length):
    l[i].tell('process')


    

        
    
