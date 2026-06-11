import { useState, useEffect, useCallback } from 'react'
import './App.css'
import Header from './Components/Header'
import Footer from './Components/Footer'
import Chat from './Components/Chat'
import Sidebar from './Components/Sidebar'
import Auth from './Components/Auth'
import { authApi, chatApi } from './api'

const toUiMessages = (conversation) =>
  (conversation?.messages || []).map((m) => ({
    text: m.content,
    from: m.role === 'assistant' ? 'ai' : 'user',
  }))

function App() {
  const [user, setUser] = useState(null)
  const [booting, setBooting] = useState(true)

  const [conversations, setConversations] = useState([])
  const [activeId, setActiveId] = useState(null)
  const [messages, setMessages] = useState([])
  const [isTyping, setIsTyping] = useState(false)

  // Restore session on load.
  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) {
      setBooting(false)
      return
    }
    authApi
      .me()
      .then(setUser)
      .catch(() => localStorage.removeItem('token'))
      .finally(() => setBooting(false))
  }, [])

  const refreshConversations = useCallback(async () => {
    const list = await chatApi.listConversations()
    setConversations(list)
    return list
  }, [])

  // Load conversations after auth.
  useEffect(() => {
    if (!user) return
    refreshConversations().then((list) => {
      if (list.length > 0) {
        setActiveId(list[0].id)
      }
    })
  }, [user, refreshConversations])

  // Load messages for the active conversation (dynamic, from MongoDB).
  useEffect(() => {
    if (!activeId) {
      setMessages([])
      return
    }
    chatApi
      .getConversation(activeId)
      .then((conv) => setMessages(toUiMessages(conv)))
      .catch(() => setMessages([]))
  }, [activeId])

  const handleAuth = (u) => setUser(u)

  const handleLogout = () => {
    localStorage.removeItem('token')
    setUser(null)
    setConversations([])
    setActiveId(null)
    setMessages([])
  }

  const handleNewChat = () => {
    setActiveId(null)
    setMessages([])
  }

  const handleDelete = async (id) => {
    await chatApi.deleteConversation(id)
    const list = await refreshConversations()
    if (id === activeId) {
      setActiveId(list[0]?.id || null)
    }
  }

  const handleSend = async (text) => {
    setMessages((prev) => [...prev, { text, from: 'user' }])
    setIsTyping(true)
    try {
      const res = await chatApi.send(text, activeId)
      setMessages((prev) => [...prev, { text: res.reply, from: 'ai' }])
      if (!activeId) setActiveId(res.conversation_id)
      await refreshConversations()
    } catch (err) {
      console.log(err)
      setMessages((prev) => [...prev, { text: 'Something went wrong.', from: 'ai' }])
    } finally {
      setIsTyping(false)
    }
  }

  if (booting) {
    return <div className="boot-screen">Loading…</div>
  }

  if (!user) {
    return <Auth onAuth={handleAuth} />
  }

  return (
    <>
      <Header user={user} onLogout={handleLogout} />
      <div className="layout">
        <Sidebar
          conversations={conversations}
          activeId={activeId}
          onSelect={setActiveId}
          onNew={handleNewChat}
          onDelete={handleDelete}
        />
        <div className="chatcontainer">
          <Chat messages={messages} isTyping={isTyping} onSend={handleSend} />
        </div>
      </div>
      <Footer />
    </>
  )
}

export default App
