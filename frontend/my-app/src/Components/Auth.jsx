import React, { useState } from 'react'
import './Auth.css'
import { authApi } from '../api'

const Auth = ({ onAuth }) => {
  const [mode, setMode] = useState('login')
  const [form, setForm] = useState({ username: '', email: '', password: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const isLogin = mode === 'login'

  const update = (field) => (e) => setForm({ ...form, [field]: e.target.value })

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const data = isLogin
        ? await authApi.login({ username: form.username, password: form.password })
        : await authApi.register(form)
      localStorage.setItem('token', data.token)
      onAuth(data.user)
    } catch (err) {
      setError(err.response?.data?.detail || 'Something went wrong')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-wrap">
      <form className="auth-card" onSubmit={handleSubmit}>
        <div className="auth-logo">
          <i className="bi bi-chat-dots"></i>
          <span>Pregunta</span>
        </div>
        <h2 className="auth-title">{isLogin ? 'Welcome back' : 'Create account'}</h2>

        <input
          className="auth-input"
          placeholder="Username"
          value={form.username}
          onChange={update('username')}
          required
        />
        {!isLogin && (
          <input
            className="auth-input"
            type="email"
            placeholder="Email"
            value={form.email}
            onChange={update('email')}
            required
          />
        )}
        <input
          className="auth-input"
          type="password"
          placeholder="Password"
          value={form.password}
          onChange={update('password')}
          required
        />

        {error && <div className="auth-error">{error}</div>}

        <button className="auth-button" type="submit" disabled={loading}>
          {loading ? 'Please wait…' : isLogin ? 'Log in' : 'Sign up'}
        </button>

        <div className="auth-switch">
          {isLogin ? "Don't have an account?" : 'Already have an account?'}{' '}
          <span
            onClick={() => {
              setError('')
              setMode(isLogin ? 'register' : 'login')
            }}
          >
            {isLogin ? 'Sign up' : 'Log in'}
          </span>
        </div>
      </form>
    </div>
  )
}

export default Auth
