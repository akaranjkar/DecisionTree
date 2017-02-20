class Node:
    __decision_attribute = None
    __label = None
    __parent_decision_attribute_value = None
    __children = []

    def __init__(self):
        self.__decision_attribute = None
        self.__label = None
        self.__parent_decision_attribute_value = None
        self.__children = []

    def set_decision_attribute(self,decision_attribute):
        self.__decision_attribute = decision_attribute

    def set_label(self,label):
        self.__label = label

    def set_parent_decision_attribute_value(self,parent_decision_attribute_value):
        self.__parent_decision_attribute_value = parent_decision_attribute_value

    def add_child(self,child_node):
        self.__children.append(child_node)

    def children(self):
        return self.__children

    def decision_attribute(self):
        return self.__decision_attribute

    def label(self):
        return self.__label

    def parent_decision_attribute_value(self):
        return self.__parent_decision_attribute_value

    def print(self,level):
        if self.__parent_decision_attribute_value != None:
            if level > 0:
                print("|\t" * (level - 1),end='')
            parent_decision_attribute = list(self.__parent_decision_attribute_value.keys())[0]
            parent_decision_value = self.__parent_decision_attribute_value[parent_decision_attribute]
            print(parent_decision_attribute + " = " + parent_decision_value,end='')
        if len(self.__children) != 0:
            print()
            for child in self.__children:
                child.print(level+1)
        if self.__label != None:
            print(" : " + self.__label)
