import React, { useState, useEffect } from 'react';
import useWebSocket, { ReadyState } from 'react-use-websocket';
import './App.css';

const Game = () => {
  const [requestStatus, setRequestStatus] = useState("unloaded");
  const [name, setName] = useState(null);
  const [sendMessage, lastMessage, readyState, getWebSocket] = useWebSocket("ws://localhost:8765");

  useEffect(() => {
    if (requestStatus === "unloaded") {
      sendMessage(JSON.stringify({"action": "join"}));
      setRequestStatus("loading");
      return;
    }

    const message = lastMessage && JSON.parse(lastMessage.data);

    console.log(message);

    if (message && message.name) {
      setRequestStatus("loaded");
      setName(message.name);
    }
  }, [lastMessage, sendMessage, requestStatus]);

  if (requestStatus !== "loaded") {
    return <div>loading . . . </div>;
  } else {
    return <div>{ name }</div>;
  }
}

function App() {
  return (
    <div className="App">
      <Game/>
    </div>
  );
}

export default App;
