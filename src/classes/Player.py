import pygame
from src.config.settings import *
from src.functions.helper import import_folder
from src.debug.debugging_tool import debug


class Player(pygame.sprite.Sprite):

    def __init__(self, pos, groups, obstacle_sprites, create_attack,
                 destroy_attack, create_spell, destroy_spell):
        super().__init__(groups)
        self.image = pygame.image.load(
            'src/graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)

        # graphics setup
        self.import_player_assets()
        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = 0.1

        # movement
        self.direction = pygame.math.Vector2()
        self.attacking = False
        self.attack_cd = 250
        self.attack_time = 0
        self.obstacle_sprites = obstacle_sprites

        # weapon
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(WEAPON_DATA.keys())[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_duration = None
        self.weapon_switch_cd = 200

        # spells
        self.create_spell = create_spell
        self.destroy_spell = destroy_spell
        self.spell_index = 0
        self.spell = list(SPELL_DATA.keys())[self.spell_index]
        self.can_switch_spell = True
        self.spell_switch_duration = None
        self.spell_switch_cd = 0

        # stats
        self.base_stats = PLAYER_DATA
        self.hp = self.base_stats['hp']
        self.sta = self.base_stats['sta']
        self.mp = self.base_stats['mp']
        self.exp = 10
        self.spd = self.base_stats['dex'] * 0.8

    def import_player_assets(self):
        self.animations = {
            'up': [],
            'down': [],
            'left': [],
            'right': [],
            'right_idle': [],
            'left_idle': [],
            'up_idle': [],
            'down_idle': [],
            'right_attack': [],
            'left_attack': [],
            'up_attack': [],
            'down_attack': [],
        }

        for animation in self.animations.keys():
            self.animations[animation] = import_folder(
                PLAYER_DATA['graphics'] + animation)

    def input(self):
        if not self.attacking:
            keys = pygame.key.get_pressed()

            # move up and down
            if keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_s]:
                self.direction.y = +1
                self.status = 'down'
            else:
                self.direction.y = 0

            # move left and right
            if keys[pygame.K_a]:
                self.direction.x = -1
                self.status = 'left'
            elif keys[pygame.K_d]:
                self.direction.x = +1
                self.status = 'right'
            else:
                self.direction.x = 0

            # atack
            if keys[pygame.K_e] and not self.attacking:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()

            # spell
            if keys[pygame.K_r] and not self.attacking:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_spell(pow=SPELL_DATA[self.spell]['pow'] *
                                  self.base_stats['int'],
                                  mp=SPELL_DATA[self.spell]['mp'],
                                  style=self.spell)

            # switch weapons
            if self.can_switch_weapon:
                for weapon_index in range(len(WEAPON_DATA)):
                    if keys[pygame.K_1 + weapon_index]:
                        self.can_switch_weapon = False
                        self.weapon_switch_duration = pygame.time.get_ticks()
                        self.weapon_index = weapon_index
                        self.weapon = list(
                            WEAPON_DATA.keys())[self.weapon_index]

            # switch spells
            if self.can_switch_spell:
                for spell_index in range(len(SPELL_DATA)):
                    if keys[pygame.K_6 + spell_index]:
                        self.can_switch_spell = False
                        self.spell_switch_duration = pygame.time.get_ticks()
                        self.spell_index = spell_index
                        self.spell = list(SPELL_DATA.keys())[self.spell_index]

    def get_status(self):
        # idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'

        # attack staus
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed * (
            1 + self.base_stats['dex'] / 10)
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed * (
            1 + self.base_stats['dex'] / 10)
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                # if obstacle collides with player horizontally
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:  # mov right
                        self.hitbox.right = sprite.hitbox.left

                    if self.direction.x < 0:  # mov left
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                # if obstacle collides with player vertically
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:  # mov down
                        self.hitbox.bottom = sprite.hitbox.top

                    if self.direction.y < 0:  # mov up
                        self.hitbox.top = sprite.hitbox.bottom

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cd:
                self.attacking = False
                self.destroy_attack()

        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_duration >= self.weapon_switch_cd:
                self.can_switch_weapon = True

        if not self.can_switch_spell:
            if current_time - self.spell_switch_duration >= self.spell_switch_cd:
                self.can_switch_spell = True

    def animate(self):
        animation = self.animations[self.status]

        # loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation): self.frame_index = 0

        # set image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def update(self):
        self.input()
        self.move(self.spd)
        self.cooldowns()
        self.get_status()
        self.animate()