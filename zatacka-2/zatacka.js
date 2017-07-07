// Possible keys for players
var count = 5;

var keys = [
  ['ArrowLeft', 'ArrowRight'], ['q', 'w'], [',','.'], ['z','x'], ['v','b']
];
var colors = ['red', 'green', 'blue', 'white', 'yellow'];

var width = 400, height = 400;

var players = []
var deg = 0.03, speed = 0.5;

function random(x){
  return Math.random()*x;
}

function Player(keys, color){
  this.x = random(width);
  this.y = random(height);

  this.points = [[this.x,this.y]];

  this.keys = keys;
  this.color = color;

  this.dir = random(2*Math.PI);
}

function init(){
  for(var i = 0; i< count; i++)
    players[i] = new Player(keys[i], colors[i]);

  canvas = document.getElementById('screen');
  ctx = canvas.getContext('2d');

  canvas.width = width;
  canvas.height = height;

  interval = setInterval(loop, 10);
}

function loop(){

  move();
  draw();
}

function det(p0,p1,p2){
  return p0[0]*p1[1] + p1[0]*p2[1] + p2[0]*p0[1] - p0[1]*p1[0] - p1[1]*p2[0] - p2[1]*p0[0];
}

// check if p0--p1 intersect p2--p3
function intersect(p0, p1, p2, p3){
  if(Math.sign(det(p0,p1,p2))!= Math.sign(det(p0,p1,p3)) && Math.sign(det(p2,p3,p0)) != Math.sign(det(p2,p3,p1)))
    return true;
  return false;
}


function move(){
  // check for collisions
  var destroy = new Array(count);

  // Adjust movement
  for(var i=0;i<count;i++){
    // rotate left
    if(is_key_down(players[i].keys[1])){
      console.log('left key down', i);
      players[i].dir = (players[i].dir - deg + 2*Math.PI) % (2*Math.PI);
    }
    // rotate right
    if(is_key_down(players[i].keys[0]))
      players[i].dir = (players[i].dir + deg) % (2*Math.PI);
  }

  // Move players
  for(var i=0;i<count;i++){
    players[i].x += Math.sin(players[i].dir)*speed;
    players[i].y += Math.cos(players[i].dir)*speed;

    // check board bounderies
    if(players[i].x < 0 || players[i].x >= width || players[i].y < 0 || players[i].y >= height)
      destroy[i] = true;

    players[i].points.push([players[i].x, players[i].y]);
  }


  for(var i=0;i<count;i++)
    for(var j=0;j<count;j++)
      if(i!=j){// check if i collides with j
        var p0 = players[i].points[players[i].points.length-1],
            p1 = players[i].points[players[i].points.length-2];

        for(var p = 1; p < players[j].points.length; p++)
          if(intersect(p0, p1, players[j].points[p-1], players[j].points[p]))
            destroy[i] = true;
      }

  // Destroy snakes
  for(var i = count-1;i>=0;i--)
    if(destroy[i]){
      console.log(destroy);
      players.splice(i,1);
      count--;
    }

  if(count == 1){
    clearInterval(interval);
    alert('And the winner is ...');
  }
  if(count == 0){
    clearInterval(interval);
    alert('Total destruction!');
  }

}

function draw(){
  // Fill white
  ctx.fillStyle = 'black';
  ctx.fillRect(0, 0, width, height);

  for(var i=0;i<count;i++){
    ctx.strokeStyle = players[i].color;
    // console.log(i);
    ctx.beginPath();
    ctx.moveTo(players[i].points[0][0], players[i].points[0][1]);
    for(var j=1;j<players[i].points.length;j++)
      ctx.lineTo(players[i].points[j][0], players[i].points[j][1]);
    ctx.stroke();
  }

}
/* Keyboard routines */

var keys_down = [];

function is_key_down(key){
  return keys_down.indexOf(key) != -1;
}

function keydown(event){
  console.log('down', event);

  if(!is_key_down(event.key))
    keys_down.push(event.key);
}

function keyup(event){
  console.log('up', event);

  if(is_key_down(event.key))
    keys_down.splice(keys_down.indexOf(event.key), 1);
}
