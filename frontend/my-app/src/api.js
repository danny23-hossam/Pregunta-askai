import axios from 'axios'

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({ baseURL: BASE_URL })

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

export const authApi = {
  register: (data) => api.post('/register', data).then((r) => r.data),
  login: (data) => api.post('/login', data).then((r) => r.data),
  me: () => api.get('/me').then((r) => r.data),
}

export const chatApi = {
  listConversations: () => api.get('/conversations').then((r) => r.data),
  createConversation: (title) =>
    api.post('/conversations', { title }).then((r) => r.data),
  getConversation: (id) => api.get(`/conversations/${id}`).then((r) => r.data),
  deleteConversation: (id) =>
    api.delete(`/conversations/${id}`).then((r) => r.data),
  send: (text, conversationId) =>
    api.post('/senddata', { text, conversation_id: conversationId }).then((r) => r.data),
}

export default api
