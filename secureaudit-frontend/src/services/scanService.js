import axios from 'axios'

const API_URL = 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_URL,
})

export const scanService = {
  /**
   * Launch a new security scan on a URL.
   * @param {string} url - the URL to scan
   * @param {string|null} token - JWT token (optional for anonymous scans)
   * @returns {Promise} scan result with score and findings
   */
  async createScan(url, token = null) {
    const headers = token
      ? { Authorization: `Bearer ${token}` }
      : {}

    const response = await api.post(
      '/scans',
      { url },
      { headers }
    )
    return response.data
  },

  /**
   * Get all scans for the logged-in user (scan history).
   * @param {string} token - JWT token (required)
   * @returns {Promise} list of scans
   */
  async getScans(token) {
    const response = await api.get('/scans', {
      headers: { Authorization: `Bearer ${token}` }
    })
    return response.data
  },

  /**
   * Get a specific scan with all its findings.
   * @param {number} scanId - ID of the scan
   * @param {string|null} token - JWT token (optional)
   * @returns {Promise} complete scan with findings
   */
  async getScan(scanId, token = null) {
    const headers = token
      ? { Authorization: `Bearer ${token}` }
      : {}

    const response = await api.get(`/scans/${scanId}`, { headers })
    return response.data
  },

  /**
   * Delete a scan.
   * @param {number} scanId - ID of the scan to delete
   * @param {string} token - JWT token (required)
   * @returns {Promise}
   */
  async deleteScan(scanId, token) {
    const response = await api.delete(`/scans/${scanId}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    return response.data
  }
}