class Tree:
    __root_node = None
    level = 0

    def __init__(self, value=None):
        if value != None:
            self.__root_node = LeafNode(value)
        else:
            self.__root_node = Node()

    def preorder(self):
        level = 0
        self.__root_node.print(level)

    def set_root_node(self,node):
        self.__root_node = node



class Node:
    __decision_attribute = None
    __label = None
    __parent_node = None
    __parent_attribute_value = None
    __attribute = None
    __children = []

    def set_decision_attribute(self,decision_attribute):
        self.__decision_attribute = decision_attribute

    def set_label(self,label):
        self.__label = label

    def add_child(self,child_node):
        self.__children.append(child_node)

    def children(self):
        return self.__children

    def attribute(self):
        return self.__attribute

    def print(self,level):
        if self.__parent_node != None:
            print("|\t" * (level -1),end='')
            print(self.__parent_node.attribute() + " = " + self.__parent_attribute_value)
        if len(self.__children) != 0:
            level +=1
            for child in self.__children:
                child.print(level)

    def set_parent(self,parent):
        self.__parent_node = parent

    def set_parent_attribute_value(self,value):
        self.__parent_attribute_value = value

    def set_children(self,children):
        self.__children = children

    def set_attribute(self,attribute):
        self.__attribute = attribute



class LeafNode(Node):
    __parent_node = None
    __value = None
    __value_distribution = []
    __children = None

    def __init__(self, value):
        self.__value = value
        self.__parent_node = None

    def print(self,level):
        if self.__parent_node == None:
            print(self.__value + " (" + ",".join(self.__value_distribution) + ")")
        else:
            print("|\t" * (level-1),end='')
            print(self.__parent_node.attribute() + " = " + self.__parent_attribute_value
                  + " : " + self.__value + " (" + ",".join(self.__value_distribution) + ")")

    def set_parent(self,parent):
        self.__parent_node = parent

    def set_parent_attribute_value(self,value):
        self.__parent_attribute_value = value

    def set_children(self,children):
        self.__children = children

    def set_attribute(self,attribute):
        self.__attribute = attribute


# n1 = Node()
# n1.set_attribute("Attr1")
# n2 = Node()
# n2.set_attribute("Attr2")
# n2.set_parent(n1)
# n2.set_parent_attribute_value("High")
# n3 = Node()
# n3.set_attribute("Attr3")
# n3.set_parent(n1)
# n3.set_parent_attribute_value("Low")
# l1 = LeafNode("Yes")
# l1.set_parent(n2)
# l1.set_parent_attribute_value("Very High")
# l2 = LeafNode("No")
# l2.set_parent(n2)
# l2.set_parent_attribute_value("Kinda High")
# l3 = LeafNode("No")
# l3.set_parent(n3)
# l3.set_parent_attribute_value("Kinda Low")
# l4 = LeafNode("Yes")
# l4.set_parent(n3)
# l4.set_parent_attribute_value("Very Low")
# n1.set_children([n2,n3])
# n2.set_children([l1,l2])
# n3.set_children([l3,l4])
# t = Tree()
# t.set_root_node(n1)
# t.preorder()