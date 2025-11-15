from Items.inventory import Inventory
from Dungeon.dungeon_generator import DungeonGenerator


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
    
    def apply_effect(self, player, enemy) :

        match self.effect :
            case "freeze" :
                enemy.frozen = 1.5
            case "flame" :
                enemy.flamed = 3.0
            case "poison" :
                enemy.poison_timer = 5.0
            case "warp" :
                new_room = DungeonGenerator.get_random_room(exclude=player.current_room)

                if new_room :
                    player.current_room = new_room
                    player.position = pygame.Vector2(new_room.spawn_x, new_room.spawn_y)
                    print(f"Warped to room {new_room}")
            case "heal" :
                player.hp = min(player.max_hp, player.hp + self.value)
                print(f"Healed for {self.value}")
            case "ammo" :
                if player.weapon:
                    player.weapon.ammo += self.value
                    print(f"+{self.value} ammo")
                
            