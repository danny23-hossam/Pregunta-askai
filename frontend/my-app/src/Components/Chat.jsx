import React, { useState, useRef, useEffect } from 'react'
import './Chat.css'
import axios from 'axios'

const Chat = () => {
  const [history, setHistory] = useState([])
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isTyping])

  const handleSend = async () => {
    const text = input.trim()
    if (!text || isTyping) return

    setMessages(prev => [...prev, { text, from: 'user' }])
    setHistory(prev => [...prev, { role: "user", content: text }])
    setInput('')
    setIsTyping(true)

    try {
      const res = await axios.post("http://localhost:8000/senddata", { text, history })
      const reply = res.data.reply

      setMessages(prev => [...prev, { text: reply, from: 'ai' }])
      setHistory(prev => [...prev, { role: "assistant", content: reply }])
    } catch (err) {
      console.log(err)
      setMessages(prev => [...prev, { text: "Something went wrong.", from: 'ai' }])
    } finally {
      setIsTyping(false)
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') handleSend()
  }

  return (
    <>
      <div className='chat-messages'>
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