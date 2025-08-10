/**
 * Entry point for the web application. Creates a Three.js scene
 * with a rotating cube and simple mouse-based interaction
 * to demonstrate high-performance 3D rendering in the browser.
 */
import * as THREE from 'three';
import { greetFromWasm } from './wasm';

function init(): void {
  // -- Scene setup ---------------------------------------------------------
  // Create the scene that will hold all 3D objects.
  const scene = new THREE.Scene();

  // Configure a perspective camera with a 75° field of view.
  const camera = new THREE.PerspectiveCamera(
    75,
    window.innerWidth / window.innerHeight,
    0.1,
    1000
  );

  // Create the renderer and append its canvas to the document.
  const renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(window.innerWidth, window.innerHeight);
  document.body.appendChild(renderer.domElement);

  // Example call to a WebAssembly function. The result is logged to console
  // to demonstrate integration between TypeScript and Rust.
  greetFromWasm('ingeniero').then((message) => console.log(message));

  // -- Geometry -----------------------------------------------------------
  // A basic green cube serves as a placeholder for future structural models.
  const geometry = new THREE.BoxGeometry();
  const material = new THREE.MeshStandardMaterial({ color: 0x00ff00 });
  const cube = new THREE.Mesh(geometry, material);
  scene.add(cube);

  // Add a light so that the cube is illuminated.
  const light = new THREE.DirectionalLight(0xffffff, 1);
  light.position.set(5, 5, 5);
  scene.add(light);

  // Position the camera slightly away from the origin.
  camera.position.z = 5;

  // -- Interaction --------------------------------------------------------
  // Simple mouse-based orbit controls to rotate the cube and zoom in/out.
  let isDragging = false;
  const previous = { x: 0, y: 0 };

  renderer.domElement.addEventListener('mousedown', (event: MouseEvent) => {
    isDragging = true;
    previous.x = event.clientX;
    previous.y = event.clientY;
  });

  renderer.domElement.addEventListener('mousemove', (event: MouseEvent) => {
    if (!isDragging) return;
    const deltaX = event.clientX - previous.x;
    const deltaY = event.clientY - previous.y;
    cube.rotation.y += deltaX * 0.01;
    cube.rotation.x += deltaY * 0.01;
    previous.x = event.clientX;
    previous.y = event.clientY;
  });

  window.addEventListener('mouseup', () => {
    isDragging = false;
  });

  renderer.domElement.addEventListener('wheel', (event: WheelEvent) => {
    event.preventDefault();
    camera.position.z += event.deltaY * 0.01;
  });

  // -- Render loop --------------------------------------------------------
  // Continuously render the scene and update any animations.
  function animate(): void {
    requestAnimationFrame(animate);
    renderer.render(scene, camera);
  }

  animate();
}

// Initialize the scene once the module has been loaded.
init();
