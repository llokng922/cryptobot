<!-- Conversational: -->

## greet
* greet
  - utter_greet
  - utter_bot_intro
  - utter_bot_function

## builder
* builder
  - utter_builder

## thank
* thank
  - utter_thank

## react_positive
* react_positive
  - utter_react_positive

## affirm
* affirm
  - utter_affirm

## deny
* canthelp
  - utter_canthelp

## out_of_scope
* out_of_scope
  - utter_out_of_scope

## bye
* bye
  - utter_bye

<!-- Task Oriented: -->

<!-- Prices without Crypto -->



<!-- Crypto Prices: -->

## crypto_price
* crypto_price{"crypto": "ripple"}
  - crypto_form
  - form{"name": "crypto_form"}
  - form{"name": "null"}
  - action_query_price

## crypto_historical_price + bitcoin
* crypto_historical_price{"crypto": "bitcoin"}
  - action_query_price_date

## crypto_historical_price + eth
* crypto_historical_price{"crypto": "ethereum"}
  - action_query_price_date

<!-- Crypto Market Performance -->

## crypto_marketcap
* crypto_marketcap{"crypto": "bitcoin"}
  - crypto_form
  - form{"name": "crypto_form"}
  - form{"name": "null"}
  - action_query_marketcap

## crypto_volume
* crypto_volume
  - action_query_volume

## crypto_percent_change_1h
* crypto_percent_change_1h{"crypto": "bitcoin"}
  - action_query_percent_change_1h

## crypto_percent_change_24h
* crypto_percent_change_24h{"crypto": "bitcoin"}
  - action_query_percent_change_24h

## highest_trading_volume
* highest_trade_volume
  - action_crypto_highest_trade_volume

## lowest_trading_volume
* lowest_trade_volume
  - action_crypto_lowest_trade_volume

## crypto_lowest_profit
* crypto_lowest_profit{"crypto":"bitcoin"}
  - action_crypto_lowest_profit

## crypto_highest_profit
* crypto_highest_profit{"crypto":"bitcoin"}
  - action_crypto_highest_profit
    
<!-- Crypto General Details: -->

## crypto_coin_symbol
* crypto_coin_symbol
  - action_query_coin_symbol

## crypto_description
* crypto_description
  - action_query_description

## crypto_feature
* crypto_feature
  - action_query_feature

## crypto_rank
* crypto_rank
  - action_query_rank

## crypto_creator
* crypto_creator
  - action_query_creator