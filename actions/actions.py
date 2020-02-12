# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

import pandas as pd 

from typing import Text, Any, Dict, List
from rasa_core_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# def get_entity_type(tracker: Tracker) -> Text:
#      """
#      Get the entity type mentioned by the user. As the user may speak of an
#      entity type in plural, we need to map the mentioned entity type to the
#      type used in the knowledge base.
#      :param tracker: tracker
#      :return: entity type (same type as used in the knowledge base)
#      """
#      graph_database = GraphDatabase()
#      entity_type = tracker.get_slot("entity_type")
#      graph_database.map("entity-type-mapping", entity_type)
#      return entity_type

# def get_attribute(tracker: Tracker) -> Text:
#     """
#     Get the attribute mentioned by the user. As the user may use a synonym for
#     an attribute, we need to map the mentioned attribute to the
#     attribute name used in the knowledge base.
#     :param tracker: tracker
#     :return: attribute (same type as used in the knowledge base)
#     """
# #    graph_database = GraphDatabase()
#     attribute = tracker.get_slot("attribute")
# #    graph_database.map("attribute-mapping", attribute)
    
#     return attribute

# def get_entity_name(tracker: Tracker, entity_type: Text) -> Text:
#     """
#     Get the name of the entity the user referred to. Either the NER detected the
#     entity and stored its name in the corresponding slot or the user referred to
#     the entity by an ordinal number, such as first or last, or the user refers to
#     an entity by its attributes.
#     :param tracker: Tracker
#     :param entity_type: the entity type
#     :return: the name of the actual entity (value of key attribute in the knowledge base)
#     """

#     # user referred to an entity by an ordinal number
# #    mention = tracker.get_slot("mention")
# #    if mention is not None:
# #        return resolve_mention(tracker)

#     # user named the entity
#     entity_name = tracker.get_slot(entity_type)
#     if entity_name:
#         return entity_name

#     user referred to an entity by its attributes
#    listed_items = tracker.get_slot("listed_items")
#    attributes = get_attributes_of_entity(entity_type, tracker)

#    if listed_items and attributes:
        # filter the listed_items by the set attributes
#        graph_database = GraphDatabase()
#        for entity in listed_items:
#            key_attr = schema[entity_type]["key"]
#            result = graph_database.validate_entity(
#                entity_type, entity, key_attr, attributes
#            )
#            if result is not None:
#                return to_str(result, key_attr)

#    return None

def pandasclean(csv):
    df = pd.read_csv('cryptodata/'+ csv +'usd.csv',usecols=[1,2,3,4,5],parse_dates=['Date'])
    df = df.set_index('Date').sort_index(ascending=True)
    df.dropna(inplace=True)
    return df

class ActionBTCprice(Action):

    def name(self) -> Text:
         return "action_bitcoin_price"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text,Any]) -> List[Dict[Text,Any]]:
         entity_value = tracker.latest_message['entities'][0]['value']
         df = pandasclean(entity_value)
         current_price = df.tail(1)['Close'][0]
         dispatcher.utter_message("This is the current {} price today.".format(entity_value))
         dispatcher.utter_message("{}".format(current_price))
         return []
        # first need to know the entity type, attribute, and entity name we are looking for
#         entity_type = get_entity_type(tracker)
#         attribute = get_attribute(tracker)
#         entity_name = get_entity_name(tracker, entity_type)
         
#        if entity_type is None:
#             dispatcher.utter_template("utter_ask_again", tracker)
#             return []
         
#         else: 
             #dispatcher.utter_message("Entity Type: {}".format(entity_type) + "Attribute: {}".format(attribute) + "Entity name: {}".format(entity_name), tracker)
 ##            dispatcher.utter_message("hello",tracker)
#             return []
