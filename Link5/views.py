from django.shortcuts import render
from django.shortcuts import HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import pandas as pd
import pickle
import os
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import LabelEncoder,OneHotEncoder
from django.http import JsonResponse
from django.forms.models import model_to_dict
num=0
lstt=[]
train_lstt=[]
test_lstt=[]
data = [['tom', 10], ['nick', 15], ['juli', 14]] 
df = pd.DataFrame(data, columns = ['Name', 'Age'])
test_df = pd.DataFrame(data, columns = ['Name', 'Age'])
train_df = pd.DataFrame(data, columns = ['Name', 'Age'])
indexes1=[]

from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVC
regressor=0
regList=[]
regnames=[]

def Link5(request):
    if request.user.is_authenticated and request.user.profile.ifTeacher:
        return render(request, 'Link5.html', {})
    return redirect('login_T')

def rowcol(request):
    if request.method == 'POST':
        try:
            global train_lstt
            global test_lstt
            global test_df
            global train_df
            train_file = request.FILES['train']
            test_file = request.FILES['test']
            train_dataset=pd.read_csv(train_file)
            test_dataset=pd.read_csv(test_file)
            count_row_train, count_col_train = train_dataset.shape
            count_row_test, count_col_test = test_dataset.shape
            train_df=train_dataset
            test_df=test_dataset
            
            train_lst=list(train_dataset)
            test_lst=list(test_dataset)
            
            train_lstt=train_lst
            test_lstt=test_lst
            #lst1=lst[:-1]
            train_df1=train_df[:10]
            test_df1=test_df[:10]
            #dictionary = { lst[i] : i for i in range(0, len(lst) ) }
            return render(request, 'Link5_rc.html', {'train_arr':train_lst,'train_cols':count_col_train,'train_rows':count_row_train,'train_data1':train_df1.to_html(classes=["table table-bordered"]),  'test_arr':test_lst,'test_cols':count_col_test,'test_rows':count_row_test,'test_data1':test_df1.to_html(classes=["table table-bordered"])})
        except:
            return HttpResponse('ERROR')
    else:
        return redirect('Link5')
            
def prec(request):
    if request.method == 'POST':
        checks = request.POST.getlist('checks[]')
        target = request.POST['target']
        algo=request.POST.getlist('algo[]')
        checks = list(map(int, checks))
        target=int(target)
        global train_df
        x=train_df.iloc[:,checks].values
        y=train_df.iloc[:,target].values
        #preprocessing:
        dtypes_list= list(train_df.dtypes)
        categorical_lst=[]
        for i in range(0,len(checks)):
            if(dtypes_list[checks[i]]=='object'):
                categorical_lst.append(i)
        
        labelencoder = LabelEncoder()
        for i in categorical_lst:
            x[:,i]=labelencoder.fit_transform(x[:,i])
            
        if len(categorical_lst)!=0:
            oneh=OneHotEncoder(categorical_features=categorical_lst)
            x=oneh.fit_transform(x).toarray()
        '''
        avoid dummy variable
        '''
        sc=StandardScaler()
        x=sc.fit_transform(x)
        #for y:-
        if dtypes_list[target]=='object':
            y=labelencoder.fit_transform(y)
        
        #global regressor
        global regList
        global regnames
        regnames=[]
        regList=[]
        for i in algo:
            if i=='dt':
                regressor=DecisionTreeRegressor(random_state=0)
                regressor.fit(x,y)
                regList.append(regressor)
                regnames.append('Decision Tree')
            elif i=='knn':
                regressor=KNeighborsClassifier(n_neighbors=5,metric='minkowski',p=2)
                regressor.fit(x,y)
                regList.append(regressor)
                regnames.append('KNN')
            elif i=='rf':
                regressor=RandomForestRegressor(n_estimators=10,random_state=0)
                regressor.fit(x,y)
                regList.append(regressor)
                regnames.append('Random Forest')
            elif i=='svm':
                regressor=SVC(kernel='rbf',random_state=0)
                regressor.fit(x,y)
                regList.append(regressor)
                regnames.append('SVM')
            #regressor.fit(x,y)

        return HttpResponse('')
    else:
        return redirect('Link5')

def prec_(request):
    if request.method == 'POST':
        checks = request.POST.getlist('checks_[]')
        target = request.POST['target_']
        checks = list(map(int, checks))
        target=int(target)
        global test_df
        x=test_df.iloc[:,checks].values
        y=test_df.iloc[:,target].values.astype('int64')

        #preprocessing:
        dtypes_list= list(test_df.dtypes)
        categorical_lst=[]
        for i in range(0,len(checks)):
            if(dtypes_list[checks[i]]=='object'):
                categorical_lst.append(i)
        
        labelencoder = LabelEncoder()
        for i in categorical_lst:
            x[:,i]=labelencoder.fit_transform(x[:,i])
            
        if len(categorical_lst)!=0:
            oneh=OneHotEncoder(categorical_features=categorical_lst)
            x=oneh.fit_transform(x).toarray()
        '''
        avoid dummy variable
        '''
        sc=StandardScaler()
        x=sc.fit_transform(x)
        
        if dtypes_list[target]=='object':
            y=labelencoder.fit_transform(y)
        
        sc=StandardScaler()
        x=sc.fit_transform(x)
        
        global regressor
        global regList
        global regnames
        #lsstt=[1,2,3]
        resultDict={'regs':len(regList),'regnames':regnames,'tp':[],'tn':[],'fn':[],'fp':[],'accuracy':[],'recall':[],'precision':[],'f1':[]}
        #resultDict['abc']=lsstt
        for i in range(0,len(regList)):
            y_pred=regList[i].predict(x)
            cm=confusion_matrix(y,y_pred.round())
            resultDict['tp'].append(int(cm[0][0]))
            resultDict['tn'].append(int(cm[1][1]))
            resultDict['fn'].append(int(cm[0][1]))
            resultDict['fp'].append(int(cm[1][0]))
            resultDict['accuracy'].append((cm[0][0]+cm[1][1])/(cm[0][0]+cm[1][0]+cm[0][1]+cm[1][1]))
            recall=cm[0][0]/(cm[0][0]+cm[0][1])
            precision=cm[0][0]/(cm[0][0]+cm[1][0])
            resultDict['recall'].append(round(recall,4))
            resultDict['precision'].append(round(precision,4))
            resultDict['f1'].append(round((2*(recall * precision) / (recall + precision)),4))
        #resultDict={'tp':int(cm[0][0]),'tn':int(cm[1][1]),'fn':int(cm[0][1]),'fp':int(cm[1][0]),'accuracy':accuracy,'recall':recall,'precision':precision,'f1':f1}
        return JsonResponse(resultDict,status=200)        
    else:
        return redirect('Link5')

    

def classification(request):
    if request.method == 'POST':
        return HttpResponse('')
    else:
        return redirect('Link5')
    '''
        try:
            global lstt
            global df
            global indexes1
            count_row, count_col = df.shape
            target=request.POST.get("submit")
            colno=0
            for i in range(0,len(lstt)):
                if lstt[i]==target:
                    colno=i
                    break
            allcol=df.iloc[:,:].values
            labelencoder = LabelEncoder()
            allcol[:,1] = labelencoder.fit_transform(allcol[:,1])
            sc=StandardScaler()
            allcol[:,[0,2,3]]=sc.fit_transform(allcol[:,[0,2,3]])
            x=allcol[:,indexes1]
            y=allcol[:,colno].astype('int64')
            ''''''
            if len(indexes1)==4:
                decision_tree_model_pkl=open(os.path.dirname(os.path.realpath(__file__)) + '\classifiers\decision_tree_classifier_4col.pkl', "rb")
                decision_tree_model = pickle.load(decision_tree_model_pkl)
            elif len(indexes1)==3:
                if indexes1[0]==0 and indexes1[1]==1 and indexes1[2]==2:
                    decision_tree_model_pkl=open(os.path.dirname(os.path.realpath(__file__)) + '\classifiers\decision_tree_classifier_3col(userid,gender,age).pkl', "rb")
                    decision_tree_model = pickle.load(decision_tree_model_pkl)
                elif indexes1[0]==0 and indexes1[1]==1 and indexes1[2]==3:
                    decision_tree_model_pkl=open(os.path.dirname(os.path.realpath(__file__)) + '\classifiers\decision_tree_classifier_3col(userid,gender,sal).pkl', "rb")
                    decision_tree_model = pickle.load(decision_tree_model_pkl)
                elif indexes1[0]==0 and indexes1[1]==2 and indexes1[2]==3:
                    decision_tree_model_pkl=open(os.path.dirname(os.path.realpath(__file__)) + '\classifiers\decision_tree_classifier_3col(userid,age,sal).pkl', "rb")
                    decision_tree_model = pickle.load(decision_tree_model_pkl)
                elif indexes1[0]==1 and indexes1[1]==2 and indexes1[2]==3:
                    decision_tree_model_pkl=open(os.path.dirname(os.path.realpath(__file__)) + '\classifiers\decision_tree_classifier_3col(gender,age,salary).pkl', "rb")
                    decision_tree_model = pickle.load(decision_tree_model_pkl)                    
            elif len(indexes1)==2:
                if indexes1[0]==0 and indexes1[1]==1:
                    decision_tree_model_pkl=open(os.path.dirname(os.path.realpath(__file__)) + '\classifiers\decision_tree_classifier_2col(userid,gender).pkl', "rb")
                    decision_tree_model = pickle.load(decision_tree_model_pkl)
                elif indexes1[0]==0 and indexes1[1]==2:
                    decision_tree_model_pkl=open(os.path.dirname(os.path.realpath(__file__)) + '\classifiers\decision_tree_classifier_2col(userid,age).pkl', "rb")
                    decision_tree_model = pickle.load(decision_tree_model_pkl)
                elif indexes1[0]==0 and indexes1[1]==3:
                    decision_tree_model_pkl=open(os.path.dirname(os.path.realpath(__file__)) + '\classifiers\decision_tree_classifier_2col(userid,salary).pkl', "rb")
                    decision_tree_model = pickle.load(decision_tree_model_pkl)
                elif indexes1[0]==1 and indexes1[1]==2:
                    decision_tree_model_pkl=open(os.path.dirname(os.path.realpath(__file__)) + '\classifiers\decision_tree_classifier_2col(gender,age).pkl', "rb")
                    decision_tree_model = pickle.load(decision_tree_model_pkl)
                elif indexes1[0]==1 and indexes1[1]==3:
                    decision_tree_model_pkl=open(os.path.dirname(os.path.realpath(__file__)) + '\classifiers\decision_tree_classifier_2col(gender,sal).pkl', "rb")
                    decision_tree_model = pickle.load(decision_tree_model_pkl)
                elif indexes1[0]==2 and indexes1[1]==3:
                    decision_tree_model_pkl=open(os.path.dirname(os.path.realpath(__file__)) + '\classifiers\decision_tree_classifier.pkl', "rb")
                    decision_tree_model = pickle.load(decision_tree_model_pkl)
            elif len(indexes1)==1:
                if indexes1[0]==0:
                    decision_tree_model_pkl=open(os.path.dirname(os.path.realpath(__file__)) + '\classifiers\decision_tree_classifier_1col(userid).pkl', "rb")
                    decision_tree_model = pickle.load(decision_tree_model_pkl)
                elif indexes1[0]==1:
                    decision_tree_model_pkl=open(os.path.dirname(os.path.realpath(__file__)) + '\classifiers\decision_tree_classifier_1col(gender).pkl', "rb")
                    decision_tree_model = pickle.load(decision_tree_model_pkl)
                elif indexes1[0]==2:
                    decision_tree_model_pkl=open(os.path.dirname(os.path.realpath(__file__)) + '\classifiers\decision_tree_classifier_1col(age).pkl', "rb")
                    decision_tree_model = pickle.load(decision_tree_model_pkl)
                elif indexes1[0]==3:
                    decision_tree_model_pkl=open(os.path.dirname(os.path.realpath(__file__)) + '\classifiers\decision_tree_classifier_1col(salary).pkl', "rb")
                    decision_tree_model = pickle.load(decision_tree_model_pkl)
            else:
                return HttpResponse('ERROR: no column selected')
            y_pred = decision_tree_model.predict(x)
            cm=confusion_matrix(y,y_pred)
            accuracy = (cm[0][0]+cm[1][1])/(cm[0][0]+cm[1][0]+cm[0][1]+cm[1][1])
            recall=cm[0][0]/(cm[0][0]+cm[0][1])
            precision=cm[0][0]/(cm[0][0]+cm[1][0])
            f1= 2*(recall * precision) / (recall + precision)
            return render(request, 'Link5_1.html', {'row':count_row,'col':count_col,'tp':cm[0][0],'tn':cm[1][1],'fn':cm[0][1],'fp':cm[1][0],'accuracy':accuracy,'recall':recall,'precision':precision,'f1':f1})
        except:
            return HttpResponse('ERROR')'''
    
