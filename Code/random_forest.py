import copy
execfile("Utility.py")
execfile("ID3.py")
execfile("variables.py")

print "Loading Saved DataSet"
training_data=extract_saved_training_data(saved_training_data)
print "Creating Top 2500 positive and 2500 negative features"
feature_list=get_top_Feature(input_sentiment_location,5000)
print "\tCreating Test data of 1000"
input_test_data=extract_training_data(input_test_location,1000) 
print "\tTest Data Created"

################################################## FUNCTIONS
#A function that returns list of trees
def getRandomForest(training_data,feature_list_total,count,tmp12,do_pruning=False):
    output=list()
    validation=extract_training_data(input_test_location,1000) 
    #maximum count of features
    max_feature_count=2000
    for i in range(count):
        feature_list=get_random_feature(feature_list_total,max_feature_count)
        training_data_for_this_feature=copy.deepcopy(training_data)
        delete_useless_words(training_data_for_this_feature,feature_list)
        tmp_root_node=ID3(training_data_for_this_feature,feature_list)
        if (do_pruning):
            prune(tmp_root_node,validation,False)
        output.append(tmp_root_node)
        print "\tForest length ",i+1,accuracy_random_forst(output,tmp12)
    return output

#A function to predict label of a data in random forest
def find_class_in_random_forest(root_list,review):
    positive=0
    negative=0
    for root in root_list:
        label_found=int(find_class(root,review))
        if (label_found==1):
            positive=positive+1
        else:
            negative=negative+1
    if (positive>negative):
        return 1
    else:
        return -1
#A Function to find accuracy of random forest
def accuracy_random_forst(root_list,dataset):
    correct=0
    total=0
    for data in dataset:
        if (find_class_in_random_forest(root_list,data)==data[0]):
            correct=correct+1
        total=total+1
    correct=float(correct)
    return ((correct*100)/total)

############################################################### SCRIPT


