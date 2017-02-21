import math
from db import DB
from tree import Node
from rules import RuleSet,Rule
from predictor import Predictor

class DecisionTree:

    def __init__(self, selection):
        self.root_node = Node()
        self.ruleset = RuleSet()
        if selection == "tennis":
            self.collection = selection
            self.collection_type = "discrete"
            self.db = DB("tennis", "tennis-attr.txt",self.collection_type)
            self.db.load_initial_data("tennis", "tennis-train.txt")
        elif selection == "iris":
            self.collection = selection
            self.collection_type = "real"
            self.db = DB("iris", "iris-attr.txt",self.collection_type)
            self.db.load_initial_data("iris", "iris-train.txt")

    def entropy(self, table):
        finalattr = self.db.last_column(table)
        finalvalues = self.db.possible_attribute_values(table, finalattr)
        finalvaluecounts = []
        for value in finalvalues:
            finalvaluecounts.append(len(self.db.fetch_matching_rows(table, finalattr, value)))
        total_examples = sum(finalvaluecounts)
        entropy = 0
        for value in finalvaluecounts:
            entropy += -((value / total_examples) * math.log2(value / total_examples))
        return entropy

    def information_gain(self, table, attribute):
        samples_entropy = self.entropy(table)  # Entropy of the sample
        possible_attribute_values = self.db.possible_attribute_values(table, attribute)
        samples_per_attribute_value = []  # Number of samples per attribute value
        for value in possible_attribute_values:
            samples_per_attribute_value.append(len(self.db.fetch_matching_rows(table, attribute, value)))
        total_attribute_samples = sum(samples_per_attribute_value)  # Total samples for the attribute

        finalattr = self.db.last_column(table)
        finalvalues = self.db.possible_attribute_values(table, finalattr)  # Possible final values

        attribute_value_entropies = []
        for value in possible_attribute_values:
            d = {attribute: value}
            temp_view = self.db.create_view(table, d)  # Create a view temporarily
            finalvaluecounts = []
            for finalvalue in finalvalues:
                finalvaluecounts.append(len(self.db.fetch_matching_rows(temp_view, finalattr, finalvalue)))
            self.db.drop_view(temp_view)
            total_examples = sum(finalvaluecounts)
            entropy = 0
            for finalvalue in finalvaluecounts:
                if finalvalue != 0:
                    entropy += -((finalvalue / total_examples) * math.log2(finalvalue / total_examples))
            attribute_value_entropies.append(entropy)

        information_gain = samples_entropy
        for i in range(0, len(possible_attribute_values)):
            information_gain -= (samples_per_attribute_value[i] / total_attribute_samples) \
                                * attribute_value_entropies[i]

        return information_gain

    def id3(self, table, root_node):
        # Create root node
        # If all examples are +ve return single node tree Root with label = +
        # If all examples are +ve return single node tree Root with label = -
        finalattr = self.db.last_column(table)
        finalvalues = self.db.possible_attribute_values(table, finalattr)  # Possible final values
        attributes = self.db.column_names(table)
        attributes.remove(finalattr)

        if len(finalvalues) == 1:  # All examples are of same type
            # Return single node tree Root with label = same final value
            root_node.set_label(finalvalues[0])
        # If attributes is empty, return single node tree Root with label = most common value of target_attr in examples
        elif len(attributes) == 0:
            common = {}
            for value in finalvalues:
                common[value] = len(self.db.fetch_matching_rows(table, finalattr, value))
            most_common_value = max(common, key=common.get)
            # Return single node tree Root with label = most common value
            root_node.set_label(most_common_value)
        else:
            # a = attribute that best classifies examples
            best_attribute = None
            max_gain = 0
            for attribute in attributes:
                attribute_gain = self.information_gain(table, attribute)
                if attribute_gain > max_gain:
                    max_gain = attribute_gain
                    best_attribute = attribute
            # decision attribute for root = a
            root_node.set_decision_attribute(best_attribute)
            possible_values = self.db.possible_attribute_values(table, best_attribute)
            # for each possible value vi of a
            for value in possible_values:
                # add a new tree branch below root corresponding to test a = vi
                # let examples be subset of examples that have value vi for a
                new_view = self.db.create_view(table, {best_attribute: value})
                examples_value = self.db.fetch_all_rows(new_view)
                # if examples is empty
                if len(examples_value) == 0:
                    # below this new branch add a leaf node with label = most common value of target attributes in examples
                    common = {}
                    for value in finalvalues:
                        common[value] = len(self.db.fetch_matching_rows(table, finalattr, value))
                    most_common_value = max(common, key=common.get)
                    child_node = Node()
                    child_node.set_label(most_common_value)
                    root_node.add_child(child_node)
                else:
                    # else below this new branch add the subtree id3(examples, target attribute, attributes - a)
                    child_node = Node()
                    child_node.set_parent_decision_attribute_value({best_attribute:value})
                    root_node.add_child(child_node)
                    self.id3(new_view, child_node)
        return root_node

    def build_tree(self, table):
        self.root_node = self.id3(table, self.root_node)
        self.root_node.print(0)
        print()
        self.ruleset.get_rules_from_tree(self.root_node, {}, '')
        self.ruleset.print_rules()


dt = DecisionTree("tennis")
# dt.information_gain("tennis","Wind")
dt.build_tree("tennis")
print()
p = Predictor("tennis-attr.txt")
p.load_test_data("tennis-train.txt")
p.all_tests_ruleset(dt.ruleset)
print("-" * 20)
p.all_tests_tree(dt.root_node)