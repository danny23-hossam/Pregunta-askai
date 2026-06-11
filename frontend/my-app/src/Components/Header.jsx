import React from 'react'
import './Header.css'


const Header = ({ user, onLogout }) => {
  return (
    <>
    <div id="" className='outdiv'>
              <div className='left'> <i className="bi bi-chat-dots conversationicon"></i> <p className='headerp1'>Pregunta</p></div>

              <div className='right'>
                <span className='username'><i className="bi bi-person-circle usericon"></i>{user ? user.username : 'Guest'}</span>
                {user && (
                  <button className='logout-btn' onClick={onLogout}>
                    <i className="bi bi-box-arrow-right"></i> Logout
                  </button>
                )}
              </div>

    </div>

    </>
  )
}

export default Header
