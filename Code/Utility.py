import random
#Generates a sorted list of random numbers between a,b of count 
def getRandom(a,b,count):
    output=list()
    if (count>b-a+1):
        print count, " numbers needed between ",a," and ",b,", However only ",b-a+1,possible,"Returning Empty List"
        return output
    while (len(output)!=count):
        tmp=random.randint(a,b)
        if tmp not in output:
            output.append(tmp)
    output.sort()
    return output
#A function to extract training data
def extract_training_data(input_location,count1):
    with open (input_location) as dic:
        content=dic.readlines()
    content = [x.strip() for x in content]
    output=list()
    positive_select=getRandom(1,len(content)/2,count1/2)
    negative_select=getRandom(len(content)/2+1,len(content),count1/2)
    i=1
    for line in content:
        #each line is a dataset
        if ((len(negative_select)==0) and (len(positive_select))==0):
            return output
        if i not in positive_select and i not in negative_select:
            i=i+1
            continue
        elif i in positive_select:
            positive_select.remove(i)
            i=i+1
        elif i in negative_select:
            negative_select.remove(i)
            i=i+1
        #Selection done,Put the current review in data
        line=line.split(" ")
        if (int(line[0])>=7):
            rating=1
        else:
            rating=-1
        line=line[1:]
        rating_list=list()
        for word in line:
            word=word.split(":")
            word_index=int(word[0])
            word_freq=int(word[1])
            rating_list.append(word_index)
        output.append([rating,rating_list])
    return output
    
    
#A function to extract training data from a saved dataset
def extract_saved_training_data(input_location):
    with open (input_location) as dic:
        content=dic.readlines()
    content = [x.strip() for x in content]
    output=list()
    for line in content:
        if (int(line[0])>=7):
            rating=1
        else:
            rating=-1
        
        line=line.split(" ")
        line=line[1:]
        rating_list=list()
        for word in line:
            word=word.split(":")
            word_index=int(word[0])
            rating_list.append(word_index)
        output.append([rating,rating_list]) 
    return output
    
def compare(item1, item2):
    if (item2[1]>item1[1]):
        return 1
    else:
        return -1
    
    
def get_top_Feature(input_polarity_file,count):
    with open (input_polarity_file) as dic:
        content=dic.readlines()
    content = [x.strip() for x in content]
    output=list()
    i=0
    for word in content:
        output.append([i,float(word)])
        i=i+1
    output.sort(cmp=compare)
    output=output[0:count/2]+output[-count/2:]
    final_output=list()
    for data in output:
        final_output.append(data[0])
    return final_output

def delete_useless_words(training_data,feature_list):
    for data in training_data:
        new_review=list()
        review=data[1]
        for word in review:
            if word in feature_list:
                new_review.append(word)
        data[1]=new_review
        
def get_random_feature(top_feature_list,count):
    rand_list=getRandom(0,len(top_feature_list)-1,count)
    output=list()
    for i in range(len(top_feature_list)):
        if i in rand_list:
            output.append(copy.deepcopy(top_feature_list[i]))
    return output
def store_dataset(input_dataset,file_name):
    file=open("./"+file_name, "w")
    for data in input_dataset:
        if (data[0]==1):
            rating=9
        else:
            rating=2
        file.write(str(rating)+" ")
        review=data[1]
        for i in review:
            file.write(str(i)+":1 ")
        file.write("\n")
def print_neg_pos(training_set):
    pos=0
    neg=0
    for data in training_set:
        if (data[0]==1):
            pos=pos+1
        else:
            neg=neg+1
    print "Positive :",pos,"Negative :",neg

def compare1(item1,item2):
    return item1[0]<item2[0]
    
def add_random_noise(input_data_set,per):
    n=len(input_data_set)
    noise_count=int((float(per)/100)*n)            #10%
    random_list=getRandom(0,n,noise_count)
    output=list()
    for i in range(n):
        data=copy.deepcopy(input_data_set[i])
        if i in random_list:
            #ADD NOISE
            if data[0]==1:
                data[0]=-1
            else:
                data[0]=1
        output.append(data)
    output.sort(cmp=compare1)
    return output
        
