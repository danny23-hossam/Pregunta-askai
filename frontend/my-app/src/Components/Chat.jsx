import React, { useState, useRef, useEffect } from 'react'
import './Chat.css'

const Chat = ({ messages, isTyping, onSend }) => {
  const [input, setInput] = useState('')
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isTyping])

  const handleSend = () => {
    const text = input.trim()
    if (!text || isTyping) return
    setInput('')
    onSend(text)
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') handleSend()
  }

  return (
    <>
      <div className='chat-messages'>
        {messages.length === 0 && !isTyping && (
          <div className='chat-empty'>Ask me anything to start the conversation.</div>
        )}
        {messages.map((msg, i) => (
          <div key={i} className={`msg-row ${msg.from}`}>
            {msg.from === 'ai' && <div className='avatar'><i className="bi bi-robot robot"></i></div>}
            <div className={`bubble ${msg.from}`}>{msg.text}</div>
          </div>
        ))}

        {isTyping && (
          <div className='msg-row ai'>
            <div className='avatar'><i className="bi bi-robot robot"></i></div>
            <div className='bubble ai typing'>
              <span /><span /><span />
            </div>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      <div className='textdiv'>
        <input
          type='text'
          className='text'
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder='Type a message…'
        />
        <button className='button' onClick={handleSend} disabled={isTyping}>↑</button>
      </div>
    </>
  )
}

export default Chat
