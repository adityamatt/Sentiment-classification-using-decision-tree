import math
#ID3 Algorithm
class node:
    feature_word=-1
    left=None
    right=None
    label=0
    def __init__(self, splitting_word_used):
        self.feature_word=splitting_word_used

#A function to find depth of a tree
def depth(root):
    if root==None:
        return 0
    if (root.right==None and root.left==None):
        return 1
    return 1+max(depth(root.left),depth(root.right))

#A functio nto find the number of nodes in a tree
def nodes_count(root):
    if root==None:
        return 0
    return 1+nodes_count(root.right)+nodes_count(root.left)

def entropy(input_training_data):
    if len(input_training_data)==0:
        return 0
    positive=0
    negative=0
    for data in input_training_data:
        if (data[0]==1):
            positive=positive+1
        else:
            negative=negative+1
    positive=float(positive)
    negative=float(negative)
    total=positive+negative
    if (positive==0 or negative==0):
        entropy=0
    else:
        entropy=-float((positive/total)*(math.log(positive/total,2)))-float((negative/total)*(math.log(negative/total,2)))
    return entropy

def information_gain(extracted_data,feature_index):
    tmp1=entropy(extracted_data)
    if (tmp1==0):
        return 0
    is_present1_list=list()
    is_absent1_list=list()
    for data in extracted_data:
        if (feature_index in data[1]):
            is_present1_list.append(data)
        else:
            is_absent1_list.append(data)
    #Now calculating I.G
    total=len(is_present1_list)+len(is_absent1_list)
#    print len(is_present1_list),len(is_absent1_list)
    #for is_present_list
    tmp=((float(len(is_present1_list))/total)*(entropy(is_present1_list)))+((float(len(is_absent1_list))/total)*(entropy(is_absent1_list)))
    return tmp1-tmp

#A function to find the most commone class of input_set
def most_common_class(input_set):
    positive=0
    negative=0
    for data in input_set:
        if data[0]==1:
            positive=positive+1
        else:
            negative=negative+1
    if positive>negative:
        return 1
    else:
        return -1
#A function that returns true if dataset is positive pure     
def is_all_positive(input_set):
    for data in input_set:
        if int(data[0])!=1:
            return False
    return True
#A function that returns true if dataset is negative pure   
def is_all_negative(input_set):
    for data in input_set:
        if int(data[0])!=-1:
            return False
    return True
    
#ID3 algo
def ID3(input_training_data,feature_list,do_early_stopping=False,ig_threshold=0.00056,depth=0,depth_thresh=100,choose_thresh=3):
#    print "ID3 Function Called with input ",len(input_training_data),len(feature_list)
    #if feature_list is empty
    if len(feature_list)==0:
        tmp_node=node(-1)
        common_label=most_common_class(input_training_data)
        tmp_node.label=common_label
        return tmp_node
    #IF ALL ARE POSITIVE PURE
    if (is_all_positive(input_training_data)):
        tmp= node(-1)
        tmp.label=1
        return tmp
    #IF ALL ARE NEGATIVE PURE
    if (is_all_negative(input_training_data)):
        tmp= node(-1)
        tmp.label=-1
        return tmp
    #Data isn't pure
#    print "Data isn't Pure"
    split_index=feature_list[0]
    max_IG=information_gain(input_training_data,split_index)
    for feature in feature_list[1:]:
        tmp=information_gain(input_training_data,feature)
        if (tmp>max_IG):
            split_index=feature
            max_IG=tmp
    tmp_node=node(split_index)
#    tmp_node.label=most_common_class(input_training_data)
#    print "Using Split_index ",split_index,max_IG
    #EARLY STOPPING
    if (do_early_stopping and choose_thresh==1):
        if ( max_IG<ig_threshold):
            common_label=most_common_class(input_training_data)
            tmp_node=node(-1)
            tmp_node.label=common_label
            return tmp_node
    if (do_early_stopping and choose_thresh==2):
        if (depth>=depth_thresh):
            common_label=most_common_class(input_training_data)
            tmp_node=node(-1)
            tmp_node.label=common_label
            return tmp_node
            
    is_present_list=list()
    is_absent_list=list()
    
    for data in input_training_data:
        if (split_index in data[1]):
            is_present_list.append(data)
        else:
            is_absent_list.append(data)
           
#    print("******************") 
#    print len(is_present_list),len(is_absent_list)
    if (max_IG==0):
        tmp_node=node(-1)
        tmp_node.label=most_common_class(input_training_data)
        return tmp_node
    if len(is_present_list)==0:
        common_label=most_common_class(input_training_data)
        tmp_tmp_node=node(-1)
        tmp_tmp_node.label=common_label
        tmp_node.right=tmp_tmp_node
    else:
        if do_early_stopping:
            tmp_node.right=ID3(is_present_list,feature_list,True,ig_threshold,depth+1,depth_thresh,choose_thresh)
        else:
            tmp_node.right=ID3(is_present_list,feature_list,False)
    if len(is_absent_list)==0:
        common_label=most_common_class(input_training_data)
        tmp_tmp_node=node(-1)
        tmp_tmp_node.label=common_label
        tmp_node.left=tmp_tmp_node
    else:
        if do_early_stopping:
            tmp_node.left=ID3(is_absent_list,feature_list,True,ig_threshold,depth+1,depth_thresh,choose_thresh)
        else:
            tmp_node.left=ID3(is_absent_list,feature_list,False)
    tmp_node.label=most_common_class(input_training_data)
    return tmp_node
    
#A function to predict the class of a test_data
def find_class(root_node,test_data):
    if (root_node==None):
        return -1
    tmp_node=root_node
    while(tmp_node.right!=None and tmp_node.left!=None):
        if (tmp_node.feature_word in test_data[1]):
            tmp_node=tmp_node.right
        else:
            tmp_node=tmp_node.left
    if (int(tmp_node.label)!=-1 and int(tmp_node.label)!=1):
        print "Wrong class Found",tmp_node.label
    return int(tmp_node.label)
#A functiion to find accuracy of model
def accuracy(root_node,data_set):
    correct=0
    total=0
    for data in data_set:
        if (find_class(root_node,data))==data[0]:
            correct=correct+1
        total=total+1
    return (float(correct)/total)*100

#A recursion function for pruning
def rec(root,current_node,test_set,max_accuracy,to_print=True):
    if current_node==None:
        return max_accuracy
    if root==None:
        return max_accuracy;
    if len(test_set)==0:
        return max_accuracy
    store_left=current_node.left;
    store_right=current_node.right
    if (store_left==None and store_right==None):
        return max_accuracy
    current_node.left=None
    current_node.right=None
    tmp_acc=accuracy(root,test_set)
    if (tmp_acc>max_accuracy):
        max_accuracy=tmp_acc
        if to_print:
            print tmp_acc,"\t",nodes_count(root),"\t",depth(root)
        return max_accuracy;
    else:
        current_node.left=store_left
        current_node.right=store_right
        rec(root,current_node.left,test_set,max_accuracy,to_print)
        rec(root,current_node.right,test_set,max_accuracy,to_print)
    
#A function to Prune a Tree
def prune(root,test_set,do_print=True):
    if root==None:
        return root
    if (root.right==None and root.left==None):
        return root_node
    max_accuracy=accuracy(root,test_set)
    if do_print:
        print "Accuracy","\t","No. of Nodes","\t","depth"
    rec(root,root.left,test_set,max_accuracy,do_print)
    rec(root,root.right,test_set,max_accuracy,do_print)

