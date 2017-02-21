import copy
from collections import OrderedDict

class RuleSet:

    def __init__(self):
        self.rules = []

    def add_rule(self, rule):
        self.rules.append(rule)

    def get_rules(self):
        return self.rules

    def get_rules_from_tree(self, root_node, antecedent, consequent):
        if root_node.parent_decision_attribute_value() == None: # Root of tree
            if (len(root_node.children()) == 0) and (root_node.label() != None): # No children, only a label
                rule = Rule()
                rule.set_consequent(root_node.label())
                rule.print()
                self.add_rule(rule)
            elif (len(root_node.children()) != 0) and (root_node.label() == None): # Has children
                for child in root_node.children():
                    child_antecedent = OrderedDict()
                    self.get_rules_from_tree(child, child_antecedent, consequent)
        elif (len(root_node.children()) != 0) and (root_node.label() == None): # Internal node
            parent_decision_attribute = list(root_node.parent_decision_attribute_value().keys())[0]
            parent_decision_value = root_node.parent_decision_attribute_value()[parent_decision_attribute]
            child_antecedent = copy.deepcopy(antecedent)
            child_antecedent[parent_decision_attribute] = parent_decision_value
            for child in root_node.children():
                self.get_rules_from_tree(child, child_antecedent, consequent)
        elif (len(root_node.children()) == 0) and (root_node.label() != None): # Leaf node
            parent_decision_attribute = list(root_node.parent_decision_attribute_value().keys())[0]
            parent_decision_value = root_node.parent_decision_attribute_value()[parent_decision_attribute]
            child_antecedent = copy.deepcopy(antecedent)
            child_antecedent[parent_decision_attribute] = parent_decision_value
            rule = Rule()
            rule.set_antecedent(child_antecedent)
            rule.set_consequent(root_node.label())
            rule.print()
            self.add_rule(rule)

    def print_rules(self):
        for rule in self.rules:
            rule.print()

class Rule:

    def __init__(self):
        self.antecedent = OrderedDict()
        self.consequent = None

    def set_consequent(self,consequent):
        self.consequent = consequent

    def set_antecedent(self,antecedent):
        self.antecedent = antecedent

    # def add_antecedent(self,antecedent):
    #     key = list(antecedent.keys())[0]
    #     value = antecedent[key]
    #     self.antecedent[key] = value

    def get_consequent(self):
        return self.consequent

    def get_antecedent(self):
        return self.antecedent

    def print(self):
        conditions = []
        if (self.antecedent != None) or (self.antecedent != {}):
            for key in self.antecedent.keys():
                conditions.append(key + " = " + str(self.antecedent[key]))
            print (" ^ ".join(conditions) + " => ",end='')
        if (self.consequent != None):
            print(self.consequent)