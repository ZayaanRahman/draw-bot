import { useState } from 'react'
import './App.css'

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
      <>canvas goes here</>
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
    <form onSubmit={handleSubmit}>
      <label htmlFor="ip">Enter the pi IP address:</label>
      <input type="text" name="ip" id="ip" value={ip} onChange={handleIpInput}/>
      
      <label htmlFor="port">Enter the pi port number:</label>
      <input type="text" name="port" id="port" value={port} onChange={handlePortInput}/>
      
      <button type="submit">Submit</button>
    </form>
    {isValid === false && <p>{error}</p>}
    {isValid === true && <p>Loading...</p>}
    </div>
  )
}

export default App
