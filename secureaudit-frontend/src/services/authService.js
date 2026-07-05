import axios from 'axios'

const API_URL = 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_URL,
})

export const authService = {
  async register(email, password) {
    const response = await api.post('/auth/register', { email, password })
    return response.data
  },

  async login(email, password) {
    const response = await api.post('/auth/login', { email, password })
    return response.data
  },

  async getMe(token) {
    const response = await api.get('/auth/me', {
      headers: { Authorization: `Bearer ${token}` },
    })
    return response.data
  },
}