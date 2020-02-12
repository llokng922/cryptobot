## greet
* greet
  - utter_greet

## bye1
* bye
  - utter_bye

## thank
* thank
  - utter_thank

## bitcoin_all
* bitcoin_price{"crypto": "bitcoin"}
  - retrieval_bitcoin_price
* bitcoin_open_high_low_close{"crypto": "bitcoin"}
  - utter_bitcoin_open_high_low_close
* bitcoin_description{"crypto": "bitcoin"}
  - utter_bitcoin_description
* bitcoin_features{"crypto": "bitcoin"}
  - utter_bitcoin_features
* bitcoin_create{"crypto": "bitcoin"}
  - utter_bitcoin_create
* bitcoin_rank{"crypto": "bitcoin"}
  - utter_bitcoin_rank
* bitcoin_marketcap{"crypto": "bitcoin"}
  - utter_bitcoin_marketcap

## bitcoin_price
* bitcoin_price{"crypto": "bitcoin"}
  - retrieval_bitcoin_price
* bitcoin_open_high_low_close{"crypto": "bitcoin"}
  - utter_bitcoin_open_high_low_close

## bitcoin_feat_description
* bitcoin_description{"crypto": "bitcoin"}
  - utter_bitcoin_description
* bitcoin_features{"crypto": "bitcoin"}
  - utter_bitcoin_features

## bitcoin_other
* bitcoin_create{"crypto": "bitcoin"}
  - utter_bitcoin_create
* bitcoin_rank{"crypto": "bitcoin"}
  - utter_bitcoin_rank
* bitcoin_marketcap{"crypto": "bitcoin"}
  - utter_bitcoin_marketcap

## bitcoin_price
* bitcoin_price{"crypto": "bitcoin"} OR bitcoin_open_high_low_close{"crypto": "bitcoin"}
  - utter_bitcoin_open_high_low_close

## deny
* canthelp
  - utter_canthelp
