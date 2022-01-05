include image 

include reactors

include color

 
#Constants
BACKGROUND = square(800, "solid", gray)

BULLET = rectangle(10, 30, "solid", blue)

BALL = triangle(50, "solid", red)

ENEMY = square(50, "solid", green) 

#Game data type
data Game:

    game(position :: Point, bullets :: List<Point>, EPos :: Point)

end

 
#Player actions, movement and firing
fun action(g :: Game, x :: Number, y :: Number, string :: String) -> Game:
  
  if string == "button-down":

  
    if g.bullets.length() < 5:
      
      game(point(x, y), link(point(x, y), g.bullets), g.EPos)
      
     
    else:
      
      g
      
    end

  else if string == "move":

    if (g.position.x < 750) and (g.position.y < 750):

      game(point(x, y), g.bullets, g.EPos)

    else if (x < 740) and (y < 730):

      game(point(x, y), g.bullets, g.EPos)
      

    else:

        g

    end
   
  else if (string == "move") and (string == "button-down"):
    
     if g.bullets.length() < 5:
      
      
      
      game(point(x, y), link(point(x, y), g.bullets), g.EPos)
      
    else:
      g
     
    end
    


  else:

    g

  end

end

 


fun tickBullet(bullet :: Point) -> Point:

  if bullet.y > 17.5:

    point(bullet.x, bullet.y - 20)

  else:

    point(0, 0)

  end

end

 

fun keepBullet(bullet :: Point) -> Boolean:

    not((bullet.x == 0) and (bullet.y == 0))

end


fun spawnEnemy(OnScreen :: Boolean, EPos :: Point) -> Point:
  
  if OnScreen == false:
    
    x = num-random(700)
    y = num-random(300)
    
    point(x, y)
    
  else:
   
    point(EPos.x, EPos.y)
    
  end
end


fun isEnemyOnScreen(g :: Game) -> Boolean:
  
  if not((g.EPos.x == 0) and (g.EPos.y == 0)):
    true
  else:
    false
  end
end


fun ticky(g :: Game) -> Game:

  # map over the bullets and either move them or set them to point(0,0)

  bullets = map(tickBullet, g.bullets)

  # filter out the point(0,0) bullets

  nonzero_bullets = filter(keepBullet, bullets)

  game(g.position, nonzero_bullets, spawnEnemy(isEnemyOnScreen(g), g.EPos))
  

end


fun draw-bullet-on-image(image :: Image, bullet :: Point) -> Image:

    underlay-xy(image, bullet.x, bullet.y, BULLET)

end



fun draw-this(g :: Game) -> Image:

  img = fold(draw-bullet-on-image, BACKGROUND, g.bullets)
  img2 = underlay-xy(img, g.EPos.x, g.EPos.y, ENEMY)

  underlay-xy(img2, g.position.x, g.position.y, BALL)  

end
 

r = reactor:

  init : game(point(10, 20), [list:], point(0,0)),

  on-mouse : action,

  to-draw : draw-this,

  on-tick : ticky

end

 

interact(r)
  
