from collections import OrderedDict


class Predictor:
    def __init__(self, attributes_file):
        self.test_data = []
        self.attributes = []
        fhandle = open("resource/" + attributes_file, 'r')
        lines = []
        for line in fhandle:
            stripped_line = line.strip()
            if stripped_line != "":
                lines.append(stripped_line)
        fhandle.close()

        for line in lines:
            self.attributes.append(line.split(" ")[0])

    def load_test_data(self, test_file):
        fhandle = open("resource/" + test_file, 'r')
        lines = []
        for line in fhandle:
            stripped_line = line.strip()
            if stripped_line != "":
                lines.append(stripped_line)
        for i in range(0, len(lines)):
            test = OrderedDict()
            split_line = lines[i].split(" ")
            for j in range(0, len(split_line)):
                test[self.attributes[j]] = split_line[j]
            self.test_data.append(test)

    def get_test_data(self):
        return self.test_data

    def get_attributes(self):
        return self.attributes

    def print_test(self, test):
        test_data, test_result = self.test_data_result(test)
        data = []
        for key in test_data.keys():
            data.append(key + " = " + test_data[key])
        print(" ^ ".join(data) + " => " + test_result)

    def test_data_result(self, test):
        test_result = test[self.attributes[-1]]
        test_data = OrderedDict()
        for i in range(0, len(self.attributes) - 1):
            test_data[self.attributes[i]] = test[self.attributes[i]]
        return test_data, test_result

    def test_ruleset(self, ruleset, test):
        test_data, test_result = self.test_data_result(test)
        for rule in ruleset.get_rules():
            flag = True  # flag to check if rule antecedents match test data
            rule_antecedent = rule.get_antecedent()
            if (rule_antecedent == None) or (rule_antecedent == {}):
                break
            for key in rule_antecedent.keys():
                if rule_antecedent[key] != test[key]:
                    flag = False
            if flag == True:
                # print("Found matching rule:", end='')
                # rule.print()
                if rule.get_consequent() == test_result:
                    # print("Valid")
                    return True
                else:
                    # print("Invalid")
                    return False

    def all_tests_ruleset(self, ruleset):
        valid_tests = 0
        total_tests = 0
        for test in self.get_test_data():
            # print("Test: ", end='')
            # self.print_test(test)
            valid = self.test_ruleset(ruleset, test)
            # print()
            total_tests += 1
            if valid:
                valid_tests += 1
        accuracy = valid_tests / total_tests * 100
        print("Tests passed: " + str(valid_tests) + "/" + str(total_tests))
        print("Ruleset accuracy: " + str(accuracy) + "%")

    def test_tree(self, root_node, test):
        test_data,test_result = self.test_data_result(test)
        if root_node.get_parent_decision_attribute_value() == None: # Root of tree
            if (len(root_node.get_children()) == 0) and (root_node.get_label() != None): # No children, only a label
                if root_node.get_label() == test_result:
                    return True
                else:
                    return False
            elif (len(root_node.get_children()) != 0) and (root_node.get_label() == None): # Has children
                for child in root_node.get_children():
                    attribute = child.get_parent_decision_attribute_value()
                    flag = True
                    for key in attribute.keys():
                        if attribute[key] != test_data[key]:
                            flag = False
                    if flag == True:
                        return self.test_tree(child,test)
        elif (len(root_node.get_children()) != 0) and (root_node.get_label() == None): # Internal node
            # Proceed if we are on the right branch
            for child in root_node.get_children():
                attribute = child.get_parent_decision_attribute_value()
                flag = True
                for key in attribute.keys():
                    if attribute[key] != test_data[key]:
                        flag = False
                if flag == True:
                    return self.test_tree(child,test)
        elif (len(root_node.get_children()) == 0) and (root_node.get_label() != None): # Leaf node
            if root_node.get_label() == test_result:
                return True
            else:
                return False

    def all_tests_tree(self, root_node):
        valid_tests = 0
        total_tests = 0
        for test in self.get_test_data():
            print("Test: ", end='')
            self.print_test(test)
            valid = self.test_tree(root_node, test)
            print()
            total_tests += 1
            if valid:
                valid_tests += 1
        accuracy = valid_tests / total_tests * 100
        print("Tests passed: " + str(valid_tests) + "/" + str(total_tests))
        print("Tree accuracy: " + str(accuracy) + "%")