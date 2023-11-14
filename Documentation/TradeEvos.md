# Converting Trade Evolutions


- Find your desired item in the pml/ItemTables.json
- Replace everything under "iconid" with 
```
      "price": 1000,
      "bp_price": 0,
      "eqp": 0,
      "atc": 0,
      "nage_atc": 30,
      "sizen_atc": 0,
      "sizen_type": 31,
      "tuibamu_eff": 0,
      "sort": 67,
      "group": 0,
      "group_id": 0,
      "fld_pocket": 4,
      "field_func": 6,
      "battle_func": 0,
      "wk_cmn": 0,
      "wk_critical_up": 0,
      "wk_atc_up": 0,
      "wk_def_up": 0,
      "wk_agi_up": 0,
      "wk_hit_up": 0,
      "wk_spa_up": 0,
      "wk_spd_up": 0,
      "wk_prm_pp_rcv": 0,
      "wk_prm_hp_exp": 0,
      "wk_prm_pow_exp": 0,
      "wk_prm_def_exp": 0,
      "wk_prm_agi_exp": 0,
      "wk_prm_spa_exp": 0,
      "wk_prm_spd_exp": 0,
      "wk_friend1": 0,
      "wk_friend2": 0,
      "wk_friend3": 0,
      "wk_prm_hp_rcv": 0,
      "flags0": 16777408
    },
```

- Go into your EvolveTables.json
- Find your desired Pokemon and change ar to `[8, itemId, desiredEvolution, 0, 0]`
- For example for Rhyperior with Protect it is `[8, 321, 464, 0, 0]`

Then repack your files and boom, done.
