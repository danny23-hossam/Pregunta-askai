import React from 'react'
import './Sidebar.css'

const Sidebar = ({ conversations, activeId, onSelect, onNew, onDelete }) => {
  return (
    <div className="sidebar">
      <button className="new-chat" onClick={onNew}>
        <i className="bi bi-plus-lg"></i> New chat
      </button>

      <div className="conv-list">
        {conversations.length === 0 && (
          <p className="conv-empty">No conversations yet</p>
        )}
        {conversations.map((c) => (
          <div
            key={c.id}
            className={`conv-item ${c.id === activeId ? 'active' : ''}`}
            onClick={() => onSelect(c.id)}
          >
            <i className="bi bi-chat-left-text"></i>
            <span className="conv-title">{c.title}</span>
            <i
              className="bi bi-trash conv-delete"
              onClick={(e) => {
                e.stopPropagation()
                onDelete(c.id)
              }}
            ></i>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Sidebar
