#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 18:49:24 2026

@author: russ
"""




a_dict    = { "key_0": "value_0",
                  "key_1": "value_1",
                  "key_2": "value_2",
                  "key_3": "value_3",
                  }






ix_to_key     = { ix: i_key for ix, i_key in enumerate( a_dict.keys() ) }

key_to_ix     = { i_key: ix for ix, i_key in enumerate( a_dict.keys() ) }

print( ix_to_key )

print( f"{ key_to_ix = }" )