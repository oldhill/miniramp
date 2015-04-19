// Color changing animated ellipse thing

// initial ellipse position
int x = window.innerWidth / 2;
int y = window.innerHeight / 2;

// initial ellipse size
int w = 0;
int h = 0;

/*
 * Setup
*/
void setup() {
  // 0_0 js window object
  size(window.innerWidth, window.innerHeight);

  smooth();
}

/*
 * Render loop
*/
void draw() {
  background(51);

  // Configure ellipse stroke
  stroke(color(random(255), random(255), random(255), random(255)));
  strokeWeight(5);
  noFill();

  // Increment width and height of ellipse
  w++;
  h++;

  // Render ellipse
  ellipse(x, y, w, h);

  // Reset effect if the ellipse reaches edge of window
  if (w == window.innerWidth || h == window.innerHeight) {
    w = 0;
    h = 0;
  }
}
