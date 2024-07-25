import { useRef, useState, useEffect} from 'react'
import { ReactSketchCanvas } from 'react-sketch-canvas';
import './App.css'

// FOR NOW: CANVAS SIZE SET IN PIXELS
// the mouse math depends on this
const CANVAS_SIDE_LEN = 450

function App() {

  const [ip, setIp] = useState('')
  const [port, setPort] = useState('')
  const [isValid, setIsValid] = useState(false)

  if (!isValid) {
    return (
      <IpInput ip={ip} setIp={setIp} port={port} setPort={setPort} isValid={isValid} setIsValid={setIsValid}/>
    )
  } else {
    return (
      <div style={{display: 'flex', justifyContent: "flex-start"}}>
      <DrawScreen ip={ip} setIp={setIp} port={port} setPort={setPort}/>
      </div>
    )
  }
}

function IpInput({ip, setIp, port, setPort, isValid, setIsValid}) {

  const [error, setError] = useState('Enter the ip address and port number of the pi');

  const handleIpInput = (event) => {
    setIp(event.target.value)
  }

  const handlePortInput = (event) => {
    setPort(event.target.value)
  }

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await fetch(`http://${ip}:${port}/ping`)
      
      if (response.ok) {
        setIsValid(true)
        setError("Loading...")
      } else {
        setIsValid(false)
        setError("Response was not ok")
      }

    } catch (error) {
      setIsValid(false)
      setError("Could not connect")
    }
  }


  return(
    <div className='form-container'>
    <form className='login-form' onSubmit={handleSubmit}>
      <label htmlFor="ip">IP address:</label>
      <input type="text" name="ip" id="ip" value={ip} onChange={handleIpInput}/>
      
      <label htmlFor="port">Port number:</label>
      <input type="text" name="port" id="port" value={port} onChange={handlePortInput}/>
      
      <button type="submit" style={{marginTop: 15}}>Verify</button>
    </form>
    {isValid === false && <p>{error}</p>}
    {isValid === true && <p>Loading...</p>}
    </div>
  )
}

function DrawScreen({ip, setIp, port, setPort}) {

  const address = `${ip}:${port}`
  const [running, setRunning] = useState(false)

  const [points, setPoints] = useState([])
  const reactSketchCanvas = useRef(null)

  const handleStart = async (event) => {
    event.preventDefault();
      
    // Handle starting/pausing

    const endpoint = running ? 'end_run' : 'start_run'

    try {
      const response = await fetch(`http://${address}/${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      })
      
      if (response.ok) {
        const json = await response.json()
        setRunning(!running)
        console.log(json.message)
      } else {
        console.log("something is wrong")
      }

    } catch (error) {
      console.log(error)
    }
    
  }

  const handleSend = async (event) => {
    event.preventDefault();

    // Handle sending data
    try {
      const response = await fetch(`http://${address}/add_points`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({points: points}),


      })
      
      if (response.ok) {
        console.log("points sent")
      } else {
        console.log("something is wrong")
      }

    } catch (error) {
      console.log(error)
    }


    reactSketchCanvas.current.clearCanvas()
    setPoints([])
  }

  function handleClear(event) {
    event.preventDefault();
    reactSketchCanvas.current.clearCanvas()
    setPoints([])
  }

  return (
    <div className='canvas-container'>
      <div className='canvas'>
        <Canvas points={points} setPoints={setPoints} reactSketchCanvas={reactSketchCanvas}/>
      </div>
      <form className='canvas-inputs'>
      
      <button
          style={{
            margin: '4px',
            backgroundColor: '#748CED',
            width: '8vw',
            height: '6vh'
          }} 
          onClick={handleStart}>
          {running ? 'Pause' : 'Start'}
        </button>
        <button
          style={{
            margin: '4px',
            width: '8vw',
            height: '6vh'
          }} 
          onClick={handleSend}>
          Send
        </button>
        <button 
          style={{
            margin: '4px',
            backgroundColor: '#f47373',
            width: '8vw',
            height: '6vh'
          }} 
          onClick={handleClear}>

          Clear
        </button>
        
      </form>

    </div>
  )
}

function Canvas({points, setPoints, reactSketchCanvas}) {

  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });

  // get mouse position
  useEffect(() => {
    const handleMouseMoveInternal = (event) => {
      setMousePosition({
        x: event.clientX,
        y: event.clientY,
      });
    };

    window.addEventListener('mousemove', handleMouseMoveInternal);

    // Cleanup event listener on component unmount
    return () => {
      window.removeEventListener('mousemove', handleMouseMoveInternal);
    };
  }, []);

  // canvas surrounding div size and location, only used to get top and left.
  const componentRef = useRef(null);
  const [dimensions, setDimensions] = useState({ top: 0, left: 0});

  // get canvas div dimensions
  useEffect(() => {
    console.log("effect ran")
    if (componentRef.current) {
      if (componentRef.current) {
        const rect = componentRef.current.getBoundingClientRect();
        const top = rect.top;
        const left = rect.left;
        setDimensions({ top, left});
      }
      

    }
  }, []); // Empty dependency array means this runs once after the initial render

  // using a state machine to manage drawing state: outside, inside, outsidedraw, insidedraw
  // handlers for enter, leave, mouse down, and mouse up are used to transition between
  const [drawState, setDrawState] = useState("inside")

  // handle point collection based on draw state
  function handleMouseMove() {

    if (drawState === "insidedraw") {

      addPoints()

    }
  }

  // handle dot drawing
  function handleMouseClick() {

    if (drawState === "inside") {

      addPoints()

    }
  }

  function handleMouseEnter() {

    if (drawState === "outside") {
      setDrawState("inside")
    } else if (drawState === "outsidedraw") {
      setDrawState("insidedraw")
    }
  }

  function handleMouseLeave() {

    if (drawState === "inside") {
      setDrawState("outside")
    } else if (drawState === "insidedraw") {
      setDrawState("outsidedraw")
    }
  }

  function handleMouseDown() {
    if (drawState === "inside") {
      setDrawState("insidedraw")
    }
  }

  function handleMouseUp() {
    if (drawState === "insidedraw") {
      setDrawState("inside")
    } else if (drawState === "outsidedraw") {
      setDrawState("outside")
    }
  }

  function addPoints() {

    const [x, y] = realCoords(mousePosition.x, mousePosition.y)

      if (isFarEnough(x, y)) {
        const newPoint = [x, y]
        setPoints((prevPoints) => [...prevPoints, newPoint]);
      }
  }

  // function to calc if new point is far enough from last to add to array
  function isFarEnough(x, y) {

    if (points.length === 0) {
      return true
    }

    const lastx = points[points.length - 1][0]
    const lasty = points[points.length - 1][1]

    const dist = Math.sqrt(Math.pow(lastx - x, 2) + Math.pow(lasty - y, 2));
    return (dist > 0.02)
  }

  // function to get point coords mapped to real distance
  function realCoords(mouseX, mouseY) {
    // restrict to 2 decimal places
    const factor = 100

    const realX = Math.round((((mouseX-dimensions.left)-(CANVAS_SIDE_LEN/2))/CANVAS_SIDE_LEN) * factor) / factor
    const realY = Math.round((((dimensions.top-mouseY)+(CANVAS_SIDE_LEN/2))/CANVAS_SIDE_LEN) * factor) / factor
    
    return [realX, realY]
  }

  const styles = {
    border: '0.0625rem solid #9c9c9c',
    margin: '4px'
  };

  return (
    <div>
      <div className='canvasWrapper'
        ref={componentRef}
        onMouseMove={handleMouseMove}
        onClick={handleMouseClick}
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
        onMouseDown={handleMouseDown}
        onMouseUp={handleMouseUp}
      >
      <ReactSketchCanvas
        ref={reactSketchCanvas}
        style={styles}
        width={String(CANVAS_SIDE_LEN) + 'px'}
        height={String(CANVAS_SIDE_LEN) + 'px'}
        strokeWidth={8}
        strokeColor="black"
        backgroundImage='../assets/cartesian_grid.svg'
      />
      </div>
      <div className='canvas-info'>
      <div style={{  maxWidth: String(CANVAS_SIDE_LEN) + 'px', overflowWrap: 'break-word', hyphens: 'auto', color: '#c9c9c7'}}>
        Points: {JSON.stringify([...points].reverse())}
      </div>
      </div>
    </div>
  );
}

export default App
