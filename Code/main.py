import copy
import pickle
import sys
sys.setrecursionlimit(3000)
execfile("Utility.py")
execfile("ID3.py")
execfile("variables.py")
execfile("random_forest.py")
#Preprocessing
print "Preprocessing"
print "\tLoading Saved Tree"
with open(saved_tree) as f:
    Root_Node=pickle.load(f)


print "\tTree Loaded with depth",depth(Root_Node)," and Nodes count:",nodes_count(Root_Node);

print "\tLoading Training Data from location",saved_training_data

training_data=extract_saved_training_data(saved_training_data)

print "\tTraining Data Loaded"

print "\tCreating Feature List of 5000 of top 2500 negative and positive reviews"

feature_list=get_top_Feature(input_sentiment_location,5000)

print "\tFeature List created"

print "\tDeleting words from Training data that are not present in Feature List"

feature_list_copy=copy.deepcopy(feature_list)

delete_useless_words(training_data,feature_list_copy)

Root_Node=ID3(training_data,feature_list)

#with open(saved_tree,"w") as f:
#    pickle.dump(Root_Node,f)


print "\tUseless words deleted"

print "\tCreating Test data of 1000"

input_test_data=extract_training_data(input_test_location,1000)
validation=extract_training_data(input_test_location,1000) 

print "Test Data created"

#DEFINE THE INDEX OF EXPERIMENT

experiment_no=int(sys.argv[1])

if (experiment_no==2):
    print "##########################EXPERIMENT 2"
    input_test_data=extract_training_data(input_test_location,1000) 
    
    acc=accuracy(Root_Node,input_test_data)
    
    print "Accuracy of Tree on Random 1000 Test Data is",acc
    
    ig_thresh_list=[0.00051,0.00052,0.00052,0.00053,0.00054,0.00055,0.00056,0.00057,0.00058,0.00059]
    
    depth_thresh_list=[10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170]
    
    ig_thresh = raw_input("Enter the information gain threshold you want to use:")
    
    ig_thresh=float(ig_thresh)
    
    print "Producing Average Accuracy of Decision Tree after Early Stopping over 10 different Test Sets of I.G=",ig_thresh
    
    root_node_early_stopped=ID3(training_data,feature_list,True,ig_thresh,0,90,1)
    
    print "Creating Random test data of 1000 and finding average accuracy of 10 datasets"
    total=0
    for i in range(10):
        input_test_data=extract_training_data(input_test_location,1000)
        acc=accuracy(root_node_early_stopped,input_test_data)
        total=total+acc
        
    print "Average Accuracy of early stopping at IG=",ig_thresh,"is",total/10
    
    depth_thresh=raw_input("Enter the depth threshold you want to use:")
    
    depth_thresh=int(depth_thresh)
    
    print "Producing Average Accuracy of Decision Tree after Early Stopping over 10 different Test Sets of Depth=",depth_thresh
    
    root_node_early_stopped=ID3(training_data,feature_list,True,ig_thresh,0,depth_thresh,2)
    
    print "Creating Random test data of 1000 and finding average accuracy of 10 datasets"
    total=0
    for i in range(10):
        input_test_data=extract_training_data(input_test_location,1000)
        acc=accuracy(root_node_early_stopped,input_test_data)
        total=total+acc
        
    print "Average Accuracy of early stopping at Depth=",depth_thresh,"is",total/10

elif  (experiment_no==3):
    print "##########################EXPERIMENT 3(For only Single Change  Noise file)"
#    noise_set=[ 0.5, 1, 5, 10]
#    for i in range(4):
#        print "Creating Noisy Data",i
#        noisy_test_data=add_random_noise(training_data,noise_set[i])
#        file_name="my_data_noisy"+str(i)+".txt"
#        store_dataset(noisy_test_data,file_name)
    choice=raw_input("Enter 1 for 0.5% Noise,2 for 1% Noise,3 for 5 and 4 for 10% Noise")
    
    choice=int(choice)
    
    if (choice==1):
        noise_set=noise1
    elif (choice==2):
        noise_set=noise2
    elif (choice==3):
        noise_set=noise3
    else:
        noise_set=noise4
    print "Creating Noisy Data Set"
    
    noisy_set=extract_saved_training_data(noise_set)
    
    print "Creating Decision Tree"
    
    noisy_node=ID3(noisy_set,feature_list)
    
    print "Node Created"
    
    acc=accuracy(noisy_node,input_test_data)
    
    print "Accuracy on Tree created from Noisy Data Set is",acc
    
    print "Depth of Tree created from Noisy Data Set is",depth(noisy_node),"and number of nodes is",nodes_count(noisy_node)
    
elif (experiment_no==4):
    print "##########################EXPERIMENT 4"
    
    acc=accuracy(Root_Node,input_test_data)
    
    print "Initial Accuracy:",acc
    
    print "Pruning"
    
    prune(Root_Node,validation)
    
    acc=accuracy(Root_Node,input_test_data)
    
    print "Final Accuracy",acc


elif (experiment_no==5):
    print "##########################EXPERIMENT 5"
    
    tree_count=raw_input("Enter the Number of Trees in the Forest:")
    
    tree_count=int(tree_count)
    
    print "Creating Forest of size",tree_count, "with Pruning"
    
    do_pruning=False
    
    choice = raw_input("Enter 1 to do pruning as well in random forest Else Enter 0:")
    choice=int(choice)
    if (choice==1):
        do_pruning=True
    
    random_forst=getRandomForest(training_data,feature_list,tree_count,input_test_data,do_pruning)
    
    print "Forest Created"
    
    print "\t\tAccuract of Random Forest is",accuracy_random_forst(random_forst,input_test_data)
        
else:
    print "Please Enter a valid experiment number"


