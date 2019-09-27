import os
import subprocess

class  TransMover:
    """This is the trans mover class created by Kamaron Bickham that goes between directories and translates the spoken text by Hoshi"""
    def __init__(self,currentDir):
        self.dir=currentDir
        self.transDir='/home/morty/OpenNMT-py/'


    def translate(self,messages):
        #change to the correct directory

        try:
            os.chdir(self.transDir)

            print('successful')
        except:
            print('Unsuccessful')
            pass

        try:
            message_sheet=open("hoshi_sheet.txt",'x')
            print('creating file')

        except:
            message_sheet=open("hoshi_sheet.txt","w")
            print('opening file that is already made')
        #write messages to file

        for msg in messages.split():
            try:
                message_sheet.write(msg)
                message_sheet.write('\n')
                print('Is it correct '+ msg)
            except:
                print('didnt work' )

        #os call
        os.system('pwd')
        output= os.system('python3 translate.py -model hoshi-model_try_3_step_40000.pt  -src hoshi_sheet.txt -output hoshi_pred.txt -replace_unk -verbose')
        print(output)



        #open the prediction file


        p=open("/home/morty/OpenNMT-py/hoshi_pred.txt")

        p=p.read()


        ###split by newline and create empty array
        preds= p.split()
        print(preds)

        prediction=[]

        for word in preds:
            if word+ " " not in prediction:
                prediction.append(word+ " ")



        print(prediction)



        # join all the words to form a sentance
        sentance =''.join(prediction)


        # os.chdir(self.currentDir)
        print('sentance is ' +sentance)
        return(sentance)
