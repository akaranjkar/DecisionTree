class Node:
    # decision_attribute = None
    # label = None
    # parent_decision_attribute_value = None
    # children = []

    def __init__(self):
        self.decision_attribute = None
        self.label = None
        self.parent_decision_attribute_value = None
        self.children = []

    def set_decision_attribute(self,decision_attribute):
        self.decision_attribute = decision_attribute

    def set_label(self,label):
        self.label = label

    def set_parent_decision_attribute_value(self,parent_decision_attribute_value):
        self.parent_decision_attribute_value = parent_decision_attribute_value

    def add_child(self,child_node):
        self.children.append(child_node)

    def get_children(self):
        return self.children

    def get_decision_attribute(self):
        return self.decision_attribute

    def get_label(self):
        return self.label

    def get_parent_decision_attribute_value(self):
        return self.parent_decision_attribute_value

    def print(self,level):
        if self.parent_decision_attribute_value != None:
            if level > 0:
                print("|\t" * (level - 1),end='')
            parent_decision_attribute = list(self.parent_decision_attribute_value.keys())[0]
            parent_decision_value = self.parent_decision_attribute_value[parent_decision_attribute]
            print(parent_decision_attribute + " = " + parent_decision_value,end='')
        if len(self.children) != 0:
            print()
            for child in self.children:
                child.print(level+1)
        if self.label != None:
            print(" : " + self.label)
