import arcade
import random
import math



right=1
stand=0
up=2
left=3
down=4
Height=700
Width=700

Game_over=False
#Difficulty
Hard=2
Medium=3
Easy=4
Zombie_speed=2
Bullet_speed=15

class Zombie(arcade.Sprite):
    def __init__(self,filename,scaling):
        super().__init__(filename,scaling)
        self.health=10
    """
    This class represents the coins on our screen. It is a child class of
    the arcade library's "Sprite" class.
    """

    def follow_sprite(self, player_sprite):
        """
        This function will move the current sprite towards whatever
        other sprite is specified as a parameter.

        We use the 'min' function here to get the sprite to line up with
        the target sprite, and not jump around if the sprite is not off
        an exact multiple of SPRITE_SPEED.
        """

        if self.center_y < player_sprite.center_y:
            self.center_y += min(Zombie_speed, player_sprite.center_y - self.center_y)
        elif self.center_y > player_sprite.center_y:
            self.center_y -= min(Zombie_speed, self.center_y - player_sprite.center_y)

        if self.center_x < player_sprite.center_x:
            self.center_x += min(Zombie_speed, player_sprite.center_x - self.center_x)
        elif self.center_x > player_sprite.center_x:
            self.center_x -= min(Zombie_speed, self.center_x - player_sprite.center_x)


class Bullet(arcade.Sprite):
    def __init__(self,filename,scaling):
        super().__init__(filename,scaling)
        self.Damage=8
        

class Player(arcade.Sprite):
    def __init__(self,filename,scaling):
        super().__init__(filename,scaling)
        self.change_x=0
        self.change_y=0
        self.center_x=100
        self.center_y=150
        self.lives=8
        self.Damage=4#use this for knifing
        
        
        
    def update(self):
        if self.center_x>=668:
            self.center_x=668
        if self.center_x<=32:
            self.center_x=32
        if self.center_y>=668:
            self.center_y=668
        if self.center_y<=32:
            self.center_y=32
        self.center_x+=self.change_x
        self.center_y+=self.change_y
        
class MyGame(arcade.Window):
    def __init__(self,width,height,title):
        super().__init__(width,height,title)
        self.ammo_count=10
        self.score=0
        self.Round=1
        self.Game_over=False
        self.Machine_Gun=False
        self.Mouse_x=0
        self.Mouse_y=0
        self.MachineGun_Bullets=50
        
        self.player_list=None
        self.zombie_list=None
        self.Bullet_list=None
        self.Ammo_list=None
        self.Machine_Gun_list=None
        
        self.player_sprite=None
        self.Bullet_sprite=None
        Machine_Gun_Sprite=None
        
        self.Gun_sound=arcade.load_sound("lmg_fire01.mp3")
        self.Reload_sound=arcade.load_sound("clipload2.wav")
        self.Dying_sound=arcade.load_sound("mutantdie.wav")
       
        arcade.set_background_color(arcade.color.AMAZON)
        self.physics_engine=None
        
    def on_draw(self):
        arcade.start_render()
        
        self.player_list.draw()
        self.Bullet_list.draw()
        self.zombie_list.draw()
        self.Ammo_list.draw()
        self.Machine_Gun_list.draw()
        
        arcade.draw_text("Lives: "+str(self.player_sprite.lives),10, 20, arcade.color.WHITE, 14)
        arcade.draw_text("Ammo: "+str(self.ammo_count),600,20,arcade.color.WHITE,14)
        arcade.draw_text("Round: "+str(self.Round),300,650,arcade.color.WHITE,14)
        arcade.draw_text("Score: "+str(self.score),600,35,arcade.color.WHITE,14)
    
        if self.Game_over==True:
            arcade.draw_text("Game Over",Height/2-75,Width/2,arcade.color.WHITE,20)#not sure why this is nor priting have alook after dinner
            
    def setup(self):
        if self.Round==1:
            self.player_list=arcade.SpriteList()
            self.zombie_list=arcade.SpriteList()
            self.Bullet_list=arcade.SpriteList()
            self.Ammo_list=arcade.SpriteList()
            self.Machine_Gun_list=arcade.SpriteList()
        
            self.player_sprite=Player("survivor1_gun.png",0.8)
            self.player_list.append(self.player_sprite)
        
        for no_zombies in range(int(40/(1+25*math.e**(-0.1*self.Round)))):
            zombie = Zombie('zoimbie1_stand.png',0.8)
            zombie.center_x=random.randrange(0,Width)
            zombie.center_y=random.randrange(0,Height)
            if zombie.center_x<=680 or zombie.center_x>20:
                zombie.center_y=random.randrange(0,100)
                if zombie.center_y>50:
                    zombie.center_y+=580
            if zombie.center_x>=680:
                zombie.center_y=random.randrange(Height)
            if zombie.center_x<=20:
                zombie.center_y=random.randrange(Height)
                
            self.zombie_list.append(zombie)
        
        for clips in range(1):
            chance=random.randrange(0,2)
            if chance==1:
                clip = arcade.Sprite('tile_269.png',0.8)
                clip.center_x=random.randrange(0,Width-5)
                clip.center_y=random.randrange(0,Height-5)
                clip.change_x=0
                clip.change_y=0
                self.Ammo_list.append(clip)
                
                
        chance_machine_gun= random.randrange(0,4)
        
        if chance_machine_gun==2:
            
            Machine_Gun_Sprite=arcade.Sprite('tile_499.png',0.6)
            Machine_Gun_Sprite.center_x=random.randrange(0,Width-5)
            Machine_Gun_Sprite.center_y=random.randrange(0,Height-5)
            self.Machine_Gun_list.append(Machine_Gun_Sprite)
            
        
    def update(self,t):
 
        self.player_list.update()
        self.Bullet_list.update()
        self.zombie_list.update()
        #self.Ammo_list.update()
        #self.Machine_Gun_list.update()
        
        for zombie in self.zombie_list:
            if zombie.center_x>650:
                zombie.angle=180
            if zombie.center_x<51:
                zombie.angle=0
            if zombie.center_y>620:
                if zombie.center_x<=680 or zombie.center_x>20:
                    zombie.angle=270
                zombie.angle=270
            if zombie.center_y<51:
                if zombie.center_x<=680 or zombie.center_x>20:
                    zombie.angle=90
                    
            diff_x=zombie.center_x-self.player_sprite.center_x
            diff_y=zombie.center_y-self.player_sprite.center_y
            ref_angle=math.atan2(diff_y,diff_x)
            ref_angle=math.degrees(ref_angle)
            zombie.angle=ref_angle+180
            
        for zombie in self.zombie_list:
            zombie.follow_sprite(self.player_sprite)
            
            
        if len(self.zombie_list)==0:
            self.Round+=1
            self.Ammo_list=arcade.SpriteList()#to remove the ammo crate at the end of the round
            self.Machine_Gun_list=arcade.SpriteList()
            self.setup()  
            
        for bullet in self.Bullet_list:
            if bullet.center_x>=705:
                bullet.remove_from_sprite_lists()
            if bullet.center_y>=705:
                bullet.remove_from_sprite_lists()
                
            hit_list = arcade.check_for_collision_with_list(bullet, self.zombie_list)
            
            if len(hit_list)>0:
                bullet.remove_from_sprite_lists()
            
                    
            for zombie in hit_list:
                zombie.health-=bullet.Damage
                if zombie.health<=0:
                    zombie.remove_from_sprite_lists()
                    chance=random.randrange(0,2)
                    if chance==1:
                        arcade.play_sound(self.Dying_sound)
                    self.score+=10
            
                
        for player in self.player_list:
            hit_list_zombie=arcade.check_for_collision_with_list(player, self.zombie_list)
            
            if len(hit_list_zombie)>0:
                if self.player_sprite.lives>0:
                    self.player_sprite.center_x=Width/2
                    self.player_sprite.center_y=Height/2
                    self.player_sprite.lives-=1
                if self.player_sprite.lives==0:
                    player.remove_from_sprite_lists()
                    self.Game_over=True
                
                
        for clip in self.Ammo_list:
            hit_list=arcade.check_for_collision_with_list(clip,self.player_list)
            
            if len(hit_list)>0:
                arcade.play_sound(self.Reload_sound)
                self.ammo_count+=10
                clip.remove_from_sprite_lists()
                
        for machine_gun in self.Machine_Gun_list:
            hit_list=arcade.check_for_collision_with_list(machine_gun,self.player_list)
            if len(hit_list)>0:
                machine_gun.remove_from_sprite_lists()
                self.Machine_Gun=True
                self.MachineGun_Bullets=50
        
        

    def on_mouse_motion(self,x,y,dx,dy):
        diff_x=x-self.player_sprite.center_x
        diff_y=y-self.player_sprite.center_y
        angle=math.atan2(diff_y,diff_x)
        angle=math.degrees(angle)
        self.player_sprite.angle=angle
        self.Mouse_x=x
        self.Mouse_y=y
        
    
    
    
    def create_bullets(self,dt):
        if self.MachineGun_Bullets<=0:
            
            self.Machine_Gun=False
            self.MachineGun_Bullets=0    
        else:
            
            Bullet_sprite=Bullet("weapon_gun.png",0.4)
            arcade.play_sound(self.Gun_sound)
            start_x = self.player_sprite.center_x
            start_y = self.player_sprite.center_y
            Bullet_sprite.center_x = start_x
            Bullet_sprite.center_y = start_y             
         
            dest_x = self.Mouse_x
            dest_y = self.Mouse_y
        
            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)
      
            Bullet_sprite.angle = math.degrees(angle)
        
       
            Bullet_sprite.center_x=self.player_sprite.center_x+8*math.sin(angle)
            Bullet_sprite.center_y=self.player_sprite.center_y-8*math.cos(angle)
    
        
            Bullet_sprite.change_x = math.cos(angle)*Bullet_speed
            Bullet_sprite.change_y = math.sin(angle)*Bullet_speed
            self.MachineGun_Bullets-=1
            self.Bullet_list.append(Bullet_sprite)
            
            
    def on_mouse_press(self,x,y,button,modifiers):
        if self.Machine_Gun==False:
            if self.ammo_count>0:
                Bullet_sprite=Bullet("weapon_gun.png",0.4)
                arcade.play_sound(self.Gun_sound)
                start_x = self.player_sprite.center_x
                start_y = self.player_sprite.center_y
                Bullet_sprite.center_x = start_x
                Bullet_sprite.center_y = start_y             
             
                dest_x = x
                dest_y = y
            
                x_diff = dest_x - start_x
                y_diff = dest_y - start_y
                angle = math.atan2(y_diff, x_diff)
          
                Bullet_sprite.angle = math.degrees(angle)
            
                Bullet_sprite.center_x=self.player_sprite.center_x+8*math.sin(angle)
                Bullet_sprite.center_y=self.player_sprite.center_y-8*math.cos(angle)
 
                Bullet_sprite.change_x = math.cos(angle)*Bullet_speed
                Bullet_sprite.change_y = math.sin(angle)*Bullet_speed
            
                self.ammo_count-=1       
                self.Bullet_list.append(Bullet_sprite)        
    
    
                
        if self.Machine_Gun==True:
            arcade.schedule(self.create_bullets,0.1)
                        
                       
    def on_mouse_release(self,x,y,button,modifiers):
        if self.Machine_Gun==True:
            arcade.unschedule(self.create_bullets)
            self.Machine_Gun=False
            
    def on_key_press(self,key,modifiers):
                
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y+=5
          
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y-=5
           
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x-=5
        
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x+=5
               
          
    def on_key_release(self,key,modifiers):
        if key == arcade.key.RIGHT or  key == arcade.key.D:
            self.player_sprite.change_x = 0  
       
        if key == arcade.key.LEFT or key==arcade.key.A:
          
            self.player_sprite.change_x=0
        if key == arcade.key.UP  or key == arcade.key.W:
            self.player_sprite.change_y = 0
           
        if key == arcade.key.DOWN or key == arcade.key.S:
    
            self.player_sprite.change_y=0
      
      
      
    
def main():
    Game=MyGame(Height, Width, "Zombies")
    Game.setup()
    arcade.run()
    
main()


# add some scores add an ammunition count by just making a variable and cheching 
#output the score