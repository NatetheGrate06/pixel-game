from Items.inventory import Inventory

import pygame

STATS = {

}

class Item :
    def __init__(self, name, type_, quant, effect=None, value=0) :
        self.name = name
        self.type = type_
        self.quant = quant
        self.items = []
        self.effect = effect
        self.value = value
        
    def use_item(self, item, selected_space) :
        self.remove_item(selected_space)
        self.apply_effect(item)

    def remove_item(self, index) :
        self.items.remove(index)
        print(f"Item removed at {index}")
    
    def apply_effect(self, player) :

        match effect :
            case "freeze" :
                pass
            case "flame" :
                pass
            case "poison" :
                pass
            case "warp" :
                pass
            case "heal" :
                pass
            case "ammo" :
                if player.weapon:
                    player.weapon.ammo += self.value
                    print(f"+{self.value} ammo")
                
            